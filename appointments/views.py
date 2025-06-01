from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from .models import Appointment, AppointmentType, Prescription, LabOrder, FollowUp
from .forms import (
    AppointmentForm, AppointmentTypeForm, PrescriptionForm, 
    LabOrderForm, FollowUpForm, AppointmentFilterForm
)
from patients.models import Patient, VitalSigns
from authentication.decorators import medical_staff_required

@login_required
def appointment_list(request):
    """View for listing all appointments with filtering capabilities."""
    
    # Base queryset
    appointments = Appointment.objects.all()
    
    # Initialize filter form
    filter_form = AppointmentFilterForm(request.GET)
    
    if filter_form.is_valid():
        # Apply filters
        provider = filter_form.cleaned_data.get('provider')
        if provider:
            appointments = appointments.filter(provider=provider)
        
        status = filter_form.cleaned_data.get('status')
        if status:
            appointments = appointments.filter(status=status)
        
        appointment_type = filter_form.cleaned_data.get('appointment_type')
        if appointment_type:
            appointments = appointments.filter(appointment_type=appointment_type)
        
        date_from = filter_form.cleaned_data.get('date_from')
        if date_from:
            appointments = appointments.filter(start_time__date__gte=date_from)
        
        date_to = filter_form.cleaned_data.get('date_to')
        if date_to:
            appointments = appointments.filter(start_time__date__lte=date_to)
        
        patient_search = filter_form.cleaned_data.get('patient_search')
        if patient_search:
            appointments = appointments.filter(
                Q(patient__first_name__icontains=patient_search) |
                Q(patient__last_name__icontains=patient_search) |
                Q(patient__medical_record_number__icontains=patient_search)
            )
    
    # Default order: upcoming appointments first, then by start time
    appointments = appointments.order_by('start_time')
    
    # Get today's appointments
    today = timezone.now().date()
    todays_appointments = appointments.filter(start_time__date=today)
    
    # Get upcoming appointments (excluding today)
    upcoming_appointments = appointments.filter(start_time__date__gt=today, status__in=['scheduled', 'confirmed'])
    
    # Get past appointments
    past_appointments = appointments.filter(start_time__date__lt=today)
    
    # Pagination for past appointments
    paginator = Paginator(past_appointments, 15)
    page_number = request.GET.get('page', 1)
    past_page_obj = paginator.get_page(page_number)
    
    context = {
        'filter_form': filter_form,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'past_page_obj': past_page_obj,
    }
    
    return render(request, 'appointments/appointment_list.html', context)

@login_required
@medical_staff_required
def appointment_create(request, patient_id=None):
    """View for creating a new appointment."""
    
    patient = None
    if patient_id:
        patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            
            # Calculate end time based on appointment type duration
            duration = appointment.appointment_type.duration_minutes
            appointment.end_time = appointment.start_time + timedelta(minutes=duration)
            
            appointment.save()
            messages.success(request, f"Appointment for {appointment.patient.full_name} created successfully.")
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        initial = {}
        if patient:
            initial['patient'] = patient
        
        form = AppointmentForm(initial=initial)
    
    context = {
        'form': form,
        'patient': patient,
        'appointment_types': AppointmentType.objects.filter(is_active=True),
    }
    
    return render(request, 'appointments/appointment_form.html', context)

@login_required
def appointment_detail(request, pk):
    """View for displaying appointment details."""
    
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Get related data
    prescriptions = appointment.prescriptions.all()
    lab_orders = appointment.lab_orders.all()
    follow_ups = appointment.follow_ups.all()
    
    # Get latest vital signs for the patient
    latest_vitals = VitalSigns.objects.filter(patient=appointment.patient).order_by('-date_recorded').first()
    
    context = {
        'appointment': appointment,
        'prescriptions': prescriptions,
        'lab_orders': lab_orders,
        'follow_ups': follow_ups,
        'latest_vitals': latest_vitals,
        'prescription_form': PrescriptionForm(),
        'lab_order_form': LabOrderForm(),
        'follow_up_form': FollowUpForm(),
    }
    
    return render(request, 'appointments/appointment_detail.html', context)

@login_required
@medical_staff_required
def appointment_edit(request, pk):
    """View for editing appointment information."""
    
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # Calculate end time based on appointment type duration
            duration = appointment.appointment_type.duration_minutes
            appointment.end_time = appointment.start_time + timedelta(minutes=duration)
            
            appointment.save()
            messages.success(request, f"Appointment for {appointment.patient.full_name} updated successfully.")
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
        'appointment_types': AppointmentType.objects.filter(is_active=True),
    }
    
    return render(request, 'appointments/appointment_form.html', context)

@login_required
@medical_staff_required
def appointment_status_update(request, pk, status):
    """View for updating appointment status."""
    
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Validate status
    valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
    if status not in valid_statuses:
        messages.error(request, "Invalid appointment status.")
        return redirect('appointment_detail', pk=pk)
    
    appointment.status = status
    appointment.save()
    
    status_display = dict(Appointment.STATUS_CHOICES)[status]
    messages.success(request, f"Appointment status updated to {status_display}.")
    
    return redirect('appointment_detail', pk=pk)

@login_required
@medical_staff_required
def add_prescription(request, appointment_pk):
    """View for adding a prescription to an appointment."""
    
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.prescribed_by = request.user
            prescription.save()
            
            # Also add to patient's medications
            patient = appointment.patient
            patient.medications.create(
                medication_name=prescription.medication_name,
                dosage=prescription.dosage,
                frequency=prescription.frequency,
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=prescription.duration_days) if prescription.duration_days else None,
                prescribing_doctor=request.user.get_full_name(),
                reason=prescription.instructions,
                notes=prescription.notes,
                is_active=True
            )
            
            messages.success(request, f"Prescription added to appointment.")
    
    return redirect('appointment_detail', pk=appointment_pk)

@login_required
@medical_staff_required
def add_lab_order(request, appointment_pk):
    """View for adding a lab order to an appointment."""
    
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    
    if request.method == 'POST':
        form = LabOrderForm(request.POST)
        if form.is_valid():
            lab_order = form.save(commit=False)
            lab_order.appointment = appointment
            lab_order.ordered_by = request.user
            lab_order.save()
            messages.success(request, f"Lab order added to appointment.")
    
    return redirect('appointment_detail', pk=appointment_pk)

@login_required
@medical_staff_required
def add_follow_up(request, appointment_pk):
    """View for adding a follow-up to an appointment."""
    
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    
    if request.method == 'POST':
        form = FollowUpForm(request.POST)
        if form.is_valid():
            follow_up = form.save(commit=False)
            follow_up.appointment = appointment
            follow_up.save()
            messages.success(request, f"Follow-up added to appointment.")
    
    return redirect('appointment_detail', pk=appointment_pk)

@login_required
@medical_staff_required
def schedule_follow_up(request, follow_up_pk):
    """View for scheduling a follow-up appointment."""
    
    follow_up = get_object_or_404(FollowUp, pk=follow_up_pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            
            # Calculate end time based on appointment type duration
            duration = appointment.appointment_type.duration_minutes
            appointment.end_time = appointment.start_time + timedelta(minutes=duration)
            
            appointment.save()
            
            # Link to follow-up
            follow_up.is_scheduled = True
            follow_up.follow_up_appointment = appointment
            follow_up.save()
            
            messages.success(request, f"Follow-up appointment scheduled successfully.")
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        initial = {
            'patient': follow_up.appointment.patient,
            'reason': follow_up.reason,
        }
        form = AppointmentForm(initial=initial)
    
    context = {
        'form': form,
        'follow_up': follow_up,
        'appointment_types': AppointmentType.objects.filter(is_active=True),
    }
    
    return render(request, 'appointments/schedule_follow_up.html', context)

@login_required
@medical_staff_required
def appointment_type_list(request):
    """View for listing appointment types."""
    
    appointment_types = AppointmentType.objects.all()
    
    if request.method == 'POST':
        form = AppointmentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment type created successfully.")
            return redirect('appointment_type_list')
    else:
        form = AppointmentTypeForm()
    
    context = {
        'appointment_types': appointment_types,
        'form': form,
    }
    
    return render(request, 'appointments/appointment_type_list.html', context)

@login_required
@medical_staff_required
def appointment_type_edit(request, pk):
    """View for editing appointment type."""
    
    appointment_type = get_object_or_404(AppointmentType, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentTypeForm(request.POST, instance=appointment_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment type updated successfully.")
            return redirect('appointment_type_list')
    else:
        form = AppointmentTypeForm(instance=appointment_type)
    
    context = {
        'form': form,
        'appointment_type': appointment_type,
    }
    
    return render(request, 'appointments/appointment_type_form.html', context)

@login_required
@medical_staff_required
def toggle_appointment_type_status(request, pk):
    """View for toggling appointment type active/inactive status."""
    
    appointment_type = get_object_or_404(AppointmentType, pk=pk)
    appointment_type.is_active = not appointment_type.is_active
    appointment_type.save()
    
    status = "activated" if appointment_type.is_active else "deactivated"
    messages.success(request, f"Appointment type {appointment_type.name} {status} successfully.")
    
    return redirect('appointment_type_list')

@login_required
def calendar_view(request):
    """View for displaying appointments in a calendar format."""
    
    # This would be extended in a real app with AJAX to load appointments dynamically
    return render(request, 'appointments/calendar.html')

@login_required
def get_calendar_events(request):
    """API endpoint for getting appointments as calendar events."""
    
    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)
    
    appointments = Appointment.objects.all()
    
    if start_date:
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        appointments = appointments.filter(start_time__gte=start_date)
    
    if end_date:
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        appointments = appointments.filter(end_time__lte=end_date)
    
    events = []
    for appointment in appointments:
        status_colors = {
            'scheduled': '#305F6D',
            'confirmed': '#698C8E',
            'in_progress': '#BF6E15',
            'completed': '#C1884E',
            'cancelled': '#263037',
            'no_show': '#263037',
        }
        
        events.append({
            'id': appointment.id,
            'title': f"{appointment.patient.full_name} - {appointment.appointment_type.name}",
            'start': appointment.start_time.isoformat(),
            'end': appointment.end_time.isoformat(),
            'color': status_colors.get(appointment.status, '#305F6D'),
            'url': f"/appointments/{appointment.id}/",
        })
    
    return JsonResponse(events, safe=False)