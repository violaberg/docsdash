from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Appointment, AppointmentType, Prescription, LabOrder, FollowUp

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class AppointmentFilterForm(forms.Form):
    """Form for filtering appointments."""
    
    provider = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=[('', '-- All Statuses --')] + list(Appointment.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    appointment_type = forms.ModelChoiceField(
        queryset=AppointmentType.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=DateInput(attrs={'class': 'form-control'})
    )
    
    date_to = forms.DateField(
        required=False,
        widget=DateInput(attrs={'class': 'form-control'})
    )
    
    patient_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search patients...'})
    )

class AppointmentForm(forms.ModelForm):
    """Form for creating and editing appointments."""
    
    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_type', 'provider', 'start_time', 'reason', 'notes']
        widgets = {
            'start_time': DateTimeInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs.update({'class': 'form-control'})
        self.fields['appointment_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['provider'].widget.attrs.update({'class': 'form-control'})
        self.fields['appointment_type'].queryset = AppointmentType.objects.filter(is_active=True)
        self.fields['provider'].queryset = User.objects.filter(is_active=True, role__in=['doctor', 'nurse'])

class AppointmentTypeForm(forms.ModelForm):
    """Form for creating and editing appointment types."""
    
    class Meta:
        model = AppointmentType
        fields = ['name', 'duration_minutes', 'description', 'default_notes', 'color_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'default_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'color_code': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }

class PrescriptionForm(forms.ModelForm):
    """Form for creating prescriptions."""
    
    class Meta:
        model = Prescription
        exclude = ['appointment', 'prescribed_by', 'date_prescribed']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'refills': forms.NumberInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class LabOrderForm(forms.ModelForm):
    """Form for creating lab orders."""
    
    class Meta:
        model = LabOrder
        exclude = ['appointment', 'ordered_by', 'ordered_date', 'results_date']
        widgets = {
            'lab_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'results': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class FollowUpForm(forms.ModelForm):
    """Form for creating follow-ups."""
    
    class Meta:
        model = FollowUp
        exclude = ['appointment', 'is_scheduled', 'follow_up_appointment']
        widgets = {
            'recommended_time_frame': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
