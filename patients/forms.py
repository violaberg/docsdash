from django import forms
from django.utils import timezone
from .models import (
    Patient, Allergy, ChronicCondition, Medication, 
    MedicalHistory, FamilyHistory, Immunization, 
    VitalSigns, PatientNote
)

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class PatientForm(forms.ModelForm):
    """Form for creating and editing patients."""
    
    class Meta:
        model = Patient
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date_of_birth': DateInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class AllergyForm(forms.ModelForm):
    """Form for patient allergies."""
    
    class Meta:
        model = Allergy
        exclude = ['patient', 'date_identified']
        widgets = {
            'reaction': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class ChronicConditionForm(forms.ModelForm):
    """Form for patient chronic conditions."""
    
    class Meta:
        model = ChronicCondition
        exclude = ['patient']
        widgets = {
            'diagnosis_date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class MedicationForm(forms.ModelForm):
    """Form for patient medications."""
    
    class Meta:
        model = Medication
        exclude = ['patient']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'reason': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class MedicalHistoryForm(forms.ModelForm):
    """Form for patient medical history."""
    
    class Meta:
        model = MedicalHistory
        exclude = ['patient']
        widgets = {
            'date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class FamilyHistoryForm(forms.ModelForm):
    """Form for patient family history."""
    
    class Meta:
        model = FamilyHistory
        exclude = ['patient']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class ImmunizationForm(forms.ModelForm):
    """Form for patient immunizations."""
    
    class Meta:
        model = Immunization
        exclude = ['patient']
        widgets = {
            'date_administered': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class VitalSignsForm(forms.ModelForm):
    """Form for patient vital signs."""
    
    class Meta:
        model = VitalSigns
        exclude = ['patient', 'recorded_by']
        widgets = {
            'date_recorded': DateTimeInput(attrs={'value': timezone.now().strftime('%Y-%m-%dT%H:%M')}),
        }
    
    def __init__(self, *args, **kwargs):
        super(VitalSignsForm, self).__init__(*args, **kwargs)
        self.fields['date_recorded'].initial = timezone.now()

class PatientNoteForm(forms.ModelForm):
    """Form for patient notes."""
    
    class Meta:
        model = PatientNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }