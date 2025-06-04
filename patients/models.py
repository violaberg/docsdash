from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
import uuid

class Patient(models.Model):
    """Model for patient records."""
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('unknown', 'Unknown'),
    )
    
    # Unique identifier
    medical_record_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    
    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Contact information
    email = models.EmailField(blank=True, null=True)
    phone_primary = models.CharField(max_length=15)
    phone_emergency = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_relation = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=15)
    
    # Insurance information
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_member_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Medical information
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPE_CHOICES, default='unknown')
    height_cm = models.PositiveIntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Record management
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (MRN: {self.medical_record_number})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        import datetime
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age
    
    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(float(self.weight_kg) / (height_m * height_m), 2)
        return None

class Allergy(models.Model):
    """Model for patient allergies."""
    
    SEVERITY_CHOICES = (
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('life_threatening', 'Life-threatening'),
    )
    
    ALLERGY_TYPES = (
        ('medication', 'Medication'),
        ('food', 'Food'),
        ('environmental', 'Environmental'),
        ('other', 'Other'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergy_type = models.CharField(max_length=20, choices=ALLERGY_TYPES)
    allergen = models.CharField(max_length=100)
    reaction = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    date_identified = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.allergen} ({self.get_severity_display()})"
    
    class Meta:
        verbose_name_plural = "Allergies"

class ChronicCondition(models.Model):
    """Model for patient chronic conditions."""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chronic_conditions')
    condition_name = models.CharField(max_length=100)
    diagnosis_date = models.DateField()
    treating_physician = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        status = "Active" if self.is_active else "Resolved"
        return f"{self.patient.full_name} - {self.condition_name} ({status})"

class Medication(models.Model):
    """Model for patient medications."""
    
    FREQUENCY_CHOICES = (
        ('once_daily', 'Once Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times_daily', 'Three Times Daily'),
        ('four_times_daily', 'Four Times Daily'),
        ('as_needed', 'As Needed'),
        ('other', 'Other (See Notes)'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    prescribing_doctor = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.medication_name} {self.dosage}"

class MedicalHistory(models.Model):
    """Model for patient medical history."""
    
    ENTRY_TYPES = (
        ('surgery', 'Surgery'),
        ('hospitalization', 'Hospitalization'),
        ('procedure', 'Procedure'),
        ('illness', 'Significant Illness'),
        ('other', 'Other'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)
    description = models.CharField(max_length=200)
    date = models.DateField()
    facility = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.get_entry_type_display()}: {self.description}"
    
    class Meta:
        verbose_name_plural = "Medical histories"

class FamilyHistory(models.Model):
    """Model for patient family medical history."""
    
    RELATIONSHIP_CHOICES = (
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('sister', 'Sister'),
        ('brother', 'Brother'),
        ('grandmother_maternal', 'Grandmother (Maternal)'),
        ('grandmother_paternal', 'Grandmother (Paternal)'),
        ('grandfather_maternal', 'Grandfather (Maternal)'),
        ('grandfather_paternal', 'Grandfather (Paternal)'),
        ('aunt', 'Aunt'),
        ('uncle', 'Uncle'),
        ('other', 'Other'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='family_history')
    relationship = models.CharField(max_length=25, choices=RELATIONSHIP_CHOICES)
    condition = models.CharField(max_length=100)
    age_at_diagnosis = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.get_relationship_display()}: {self.condition}"
    
    class Meta:
        verbose_name_plural = "Family histories"

class Immunization(models.Model):
    """Model for patient immunizations."""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='immunizations')
    vaccine_name = models.CharField(max_length=100)
    date_administered = models.DateField()
    administered_by = models.CharField(max_length=100, blank=True, null=True)
    lot_number = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.vaccine_name} ({self.date_administered})"

class VitalSigns(models.Model):
    """Model for patient vital signs."""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    date_recorded = models.DateTimeField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    heart_rate = models.PositiveIntegerField(blank=True, null=True)
    blood_pressure_systolic = models.PositiveIntegerField(blank=True, null=True)
    blood_pressure_diastolic = models.PositiveIntegerField(blank=True, null=True)
    respiratory_rate = models.PositiveIntegerField(blank=True, null=True)
    oxygen_saturation = models.PositiveIntegerField(blank=True, null=True)
    height_cm = models.PositiveIntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - Vitals on {self.date_recorded}"
    
    @property
    def blood_pressure(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return None
    
    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(float(self.weight_kg) / (height_m * height_m), 2)
        return None
    
    class Meta:
        verbose_name_plural = "Vital signs"

class PatientNote(models.Model):
    """Model for general notes about patients."""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notes')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField()
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"Note for {self.patient.full_name} by {self.created_by.full_name} on {self.created_at}"

class RecentPatient(models.Model):
    """Model to track recently viewed patients by users."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'patient')
        ordering = ['-last_viewed']
    
    def __str__(self):
        return f"{self.user.full_name} viewed {self.patient.full_name} on {self.last_viewed}"

class FavoritePatient(models.Model):
    """Model for bookmarking/favoriting patients."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'patient')
    
    def __str__(self):
        return f"{self.user.full_name} favorited {self.patient.full_name}"
