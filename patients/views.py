from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import (
    Patient, Allergy, ChronicCondition, Medication, 
    MedicalHistory, FamilyHistory, Immunization, 
    VitalSigns, PatientNote, RecentPatient, FavoritePatient
)
from .forms import (
    PatientForm, AllergyForm, ChronicConditionForm, 
    MedicationForm, MedicalHistoryForm, FamilyHistoryForm,
    ImmunizationForm, VitalSignsForm, PatientNoteForm
)
from authentication.decorators import medical_staff_required

@login_required
def patient_list(request):
    """View for listing all patients with search and filter capabilities."""
    
    query = request.GET.get('q', '')
    status = request.GET.get('status', 'active')
    
    # Base queryset
    patients = Patient.objects.all()
    
    # Filter by status
    if status == 'active':
        patients = patients.filter(is_active=True)
    elif status == 'inactive':
        patients = patients.filter(is_active=False)
    
    # Apply search query
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(medical_record_number__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_primary__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(patients.order_by('last_name', 'first_name'), 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get recently viewed patients
    recent_patients = RecentPatient.objects.filter(user=request.user)[:5]
    
    # Get favorite patients
    favorite_patients = FavoritePatient.objects.filter(user=request.user)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status': status,
        'recent_patients': recent_patients,
        'favorite_patients': favorite_patients,
        'total_count': patients.count(),
        'active_count': Patient.objects.filter(is_active=True).count(),
        'inactive_count': Patient.objects.filter(is_active=False).count(),
    }
    
    return render(request, 'patients/patient_list.html', context)

@login_required
@medical_staff_required
def patient_create(request):
    """View for creating a new patient."""
    
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            
            # Check for duplicates
            potential_duplicates = Patient.objects.filter(
                Q(first_name__iexact=patient.first_name, last_name__iexact=patient.last_name) |
                Q(email__iexact=patient.email) if patient.email else Q()
            ).exclude(id=patient.id)
            
            if potential_duplicates.exists():
                messages.warning(request, "Potential duplicate patient records detected. Please verify.")
            
            messages.success(request, f"Patient {patient.full_name} created successfully.")
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {'form': form, 'is_create': True})

@login_required
def patient_detail(request, pk):
    """View for displaying patient details."""
    
    patient = get_object_or_404(Patient, pk=pk)
    
    # Record this view in recent patients
    RecentPatient.objects.update_or_create(
        user=request.user,
        patient=patient,
        defaults={'last_viewed': timezone.now()}
    )
    
    # Check if patient is a favorite
    is_favorite = FavoritePatient.objects.filter(user=request.user, patient=patient).exists()
    
    # Get related data
    allergies = patient.allergies.all().order_by('-severity')
    chronic_conditions = patient.chronic_conditions.all().order_by('-is_active', 'condition_name')
    medications = patient.medications.all().order_by('-is_active', 'medication_name')
    medical_history = patient.medical_history.all().order_by('-date')
    family_history = patient.family_history.all().order_by('relationship')
    immunizations = patient.immunizations.all().order_by('-date_administered')
    
    # Get latest vital signs
    latest_vitals = patient.vital_signs.order_by('-date_recorded').first()
    
    # Get notes
    notes = patient.notes.all().order_by('-created_at')
    
    context = {
        'patient': patient,
        'is_favorite': is_favorite,
        'allergies': allergies,
        'chronic_conditions': chronic_conditions,
        'medications': medications,
        'medical_history': medical_history,
        'family_history': family_history,
        'immunizations': immunizations,
        'latest_vitals': latest_vitals,
        'notes': notes,
        'allergy_form': AllergyForm(),
        'chronic_condition_form': ChronicConditionForm(),
        'medication_form': MedicationForm(),
        'medical_history_form': MedicalHistoryForm(),
        'family_history_form': FamilyHistoryForm(),
        'immunization_form': ImmunizationForm(),
        'vital_signs_form': VitalSignsForm(),
        'note_form': PatientNoteForm(),
    }
    
    return render(request, 'patients/patient_detail.html', context)

@login_required
@medical_staff_required
def patient_edit(request, pk):
    """View for editing patient information."""
    
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f"Patient {patient.full_name} updated successfully.")
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {'form': form, 'patient': patient, 'is_create': False})

@login_required
@medical_staff_required
def toggle_patient_status(request, pk):
    """View for toggling patient active/inactive status."""
    
    patient = get_object_or_404(Patient, pk=pk)
    patient.is_active = not patient.is_active
    patient.save()
    
    status = "activated" if patient.is_active else "deactivated"
    messages.success(request, f"Patient {patient.full_name} {status} successfully.")
    
    return redirect('patient_detail', pk=patient.pk)

@login_required
def toggle_favorite(request, pk):
    """View for toggling favorite status of a patient."""
    
    patient = get_object_or_404(Patient, pk=pk)
    favorite, created = FavoritePatient.objects.get_or_create(user=request.user, patient=patient)
    
    if not created:
        favorite.delete()
        is_favorite = False
        message = f"Removed {patient.full_name} from favorites."
    else:
        is_favorite = True
        message = f"Added {patient.full_name} to favorites."
    
    if request.is_ajax():
        return JsonResponse({'is_favorite': is_favorite, 'message': message})
    
    messages.success(request, message)
    return redirect('patient_detail', pk=patient.pk)

@login_required
@medical_staff_required
def add_allergy(request, patient_pk):
    """View for adding an allergy to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.patient = patient
            allergy.save()
            messages.success(request, f"Allergy added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_chronic_condition(request, patient_pk):
    """View for adding a chronic condition to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = ChronicConditionForm(request.POST)
        if form.is_valid():
            condition = form.save(commit=False)
            condition.patient = patient
            condition.save()
            messages.success(request, f"Chronic condition added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_medication(request, patient_pk):
    """View for adding a medication to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.patient = patient
            medication.save()
            messages.success(request, f"Medication added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_medical_history(request, patient_pk):
    """View for adding medical history to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = patient
            history.save()
            messages.success(request, f"Medical history entry added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_family_history(request, patient_pk):
    """View for adding family history to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = FamilyHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = patient
            history.save()
            messages.success(request, f"Family history entry added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_immunization(request, patient_pk):
    """View for adding an immunization to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = ImmunizationForm(request.POST)
        if form.is_valid():
            immunization = form.save(commit=False)
            immunization.patient = patient
            immunization.save()
            messages.success(request, f"Immunization added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_vital_signs(request, patient_pk):
    """View for adding vital signs to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.patient = patient
            vitals.recorded_by = request.user
            vitals.save()
            
            # Update patient height and weight
            if vitals.height_cm:
                patient.height_cm = vitals.height_cm
            if vitals.weight_kg:
                patient.weight_kg = vitals.weight_kg
            patient.save()
            
            messages.success(request, f"Vital signs added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@medical_staff_required
def add_note(request, patient_pk):
    """View for adding a note to a patient."""
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = PatientNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.patient = patient
            note.created_by = request.user
            note.save()
            messages.success(request, f"Note added to {patient.full_name}.")
    
    return redirect('patient_detail', pk=patient_pk)

@login_required
@require_POST
def bulk_action(request):
    """View for performing bulk actions on selected patients."""
    
    action = request.POST.get('action')
    patient_ids = request.POST.getlist('patient_ids')
    
    if not patient_ids:
        messages.warning(request, "No patients selected.")
        return redirect('patient_list')
    
    patients = Patient.objects.filter(id__in=patient_ids)
    count = patients.count()
    
    if action == 'activate':
        patients.update(is_active=True)
        messages.success(request, f"{count} patients activated.")
    elif action == 'deactivate':
        patients.update(is_active=False)
        messages.success(request, f"{count} patients deactivated.")
    elif action == 'export':
        # In a real app, this would generate an export file
        messages.success(request, f"Export of {count} patients initiated.")
    else:
        messages.error(request, "Invalid action.")
    
    return redirect('patient_list')