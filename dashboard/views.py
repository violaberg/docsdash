from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from patients.models import Patient, RecentPatient
from appointments.models import Appointment
from .forms import DrugInteractionForm, MedicalCalculatorForm

@login_required
def dashboard(request):
    """Main dashboard view."""
    
    # Get current date
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Today's appointments
    todays_appointments = Appointment.objects.filter(
        start_time__date=today
    ).order_by('start_time')
    
    # Tomorrow's appointments
    tomorrows_appointments = Appointment.objects.filter(
        start_time__date=tomorrow
    ).order_by('start_time')
    
    # Recent patients for this user
    recent_patients = RecentPatient.objects.filter(user=request.user)[:5]
    
    # Stats for quick view
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(is_active=True).count()
    
    appointments_today = todays_appointments.count()
    appointments_tomorrow = tomorrows_appointments.count()
    
    upcoming_appointments = Appointment.objects.filter(
        start_time__date__gt=today,
        start_time__date__lte=today + timedelta(days=7),
        status__in=['scheduled', 'confirmed']
    ).count()
    
    # Get alerts (in a real app, this would include overdue follow-ups, critical lab results, etc.)
    alerts = []
    
    context = {
        'todays_appointments': todays_appointments,
        'tomorrows_appointments': tomorrows_appointments,
        'recent_patients': recent_patients,
        'total_patients': total_patients,
        'active_patients': active_patients,
        'appointments_today': appointments_today,
        'appointments_tomorrow': appointments_tomorrow,
        'upcoming_appointments': upcoming_appointments,
        'alerts': alerts,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def medical_references(request):
    """View for medical reference tools."""
    
    drug_interaction_form = DrugInteractionForm()
    medical_calculator_form = MedicalCalculatorForm()
    
    context = {
        'drug_interaction_form': drug_interaction_form,
        'medical_calculator_form': medical_calculator_form,
    }
    
    return render(request, 'dashboard/medical_references.html', context)

@login_required
def check_drug_interaction(request):
    """View for checking drug interactions."""
    
    result = None
    
    if request.method == 'POST':
        form = DrugInteractionForm(request.POST)
        if form.is_valid():
            # In a real app, this would query a drug interaction API
            # For this demo, we'll return a sample result
            drugs = form.cleaned_data['drugs'].split(',')
            if len(drugs) > 1:
                result = {
                    'interactions': [
                        {
                            'drugs': f"{drugs[0].strip()} & {drugs[1].strip()}",
                            'severity': 'Moderate',
                            'description': 'These medications may interact with each other. Monitor for side effects.',
                        }
                    ]
                }
            else:
                result = {'interactions': []}
    else:
        form = DrugInteractionForm()
    
    context = {
        'form': form,
        'result': result,
    }
    
    return render(request, 'dashboard/drug_interaction.html', context)

@login_required
def medical_calculator(request):
    """View for medical calculators."""
    
    result = None
    
    if request.method == 'POST':
        form = MedicalCalculatorForm(request.POST)
        if form.is_valid():
            calculator_type = form.cleaned_data['calculator_type']
            
            if calculator_type == 'bmi':
                height = form.cleaned_data['height']
                weight = form.cleaned_data['weight']
                
                # BMI calculation
                bmi = weight / ((height / 100) ** 2)
                
                if bmi < 18.5:
                    category = 'Underweight'
                elif 18.5 <= bmi < 25:
                    category = 'Normal weight'
                elif 25 <= bmi < 30:
                    category = 'Overweight'
                else:
                    category = 'Obese'
                
                result = {
                    'calculator': 'BMI',
                    'result': round(bmi, 2),
                    'interpretation': f'Category: {category}',
                }
    else:
        form = MedicalCalculatorForm()
    
    context = {
        'form': form,
        'result': result,
    }
    
    return render(request, 'dashboard/medical_calculator.html', context)
