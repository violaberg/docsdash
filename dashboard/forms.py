from django import forms

class DrugInteractionForm(forms.Form):
    """Form for checking drug interactions."""
    
    drugs = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter medications separated by commas (e.g., aspirin, lisinopril, metformin)'
            }
        )
    )

class MedicalCalculatorForm(forms.Form):
    """Form for medical calculators."""
    
    CALCULATOR_CHOICES = (
        ('bmi', 'Body Mass Index (BMI)'),
        ('bsa', 'Body Surface Area (BSA)'),
        ('egfr', 'Estimated GFR'),
        ('creatinine_clearance', 'Creatinine Clearance'),
    )
    
    calculator_type = forms.ChoiceField(
        choices=CALCULATOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # BMI fields
    height = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Height (cm)',
                'step': '0.1'
            }
        )
    )
    
    weight = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Weight (kg)',
                'step': '0.1'
            }
        )
    )
    
    # Other calculator fields would be added here
    
    def clean(self):
        cleaned_data = super().clean()
        calculator_type = cleaned_data.get('calculator_type')
        
        if calculator_type == 'bmi':
            height = cleaned_data.get('height')
            weight = cleaned_data.get('weight')
            
            if not height:
                self.add_error('height', 'Height is required for BMI calculation')
            
            if not weight:
                self.add_error('weight', 'Weight is required for BMI calculation')
        
        # Validation for other calculator types would be added here
        
        return cleaned_data
