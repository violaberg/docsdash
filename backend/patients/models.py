from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # Core Demographics
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    medical_record_number = models.CharField(max_length=50, unique=True)
    
    # Contact Information
    phone_primary = models.CharField(max_length=20)
    phone_emergency = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    mailing_address = models.TextField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=20)
    
    # Insurance Information
    insurance_provider = models.CharField(max_length=100)
    insurance_id = models.CharField(max_length=50)
    
    # Medical Information
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # Physical Characteristics
    height = models.DecimalField(max_digits=5, decimal_places=2)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (MRN: {self.medical_record_number})"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    notes = models.TextField(blank=True)
    medications_prescribed = models.TextField(blank=True)
    follow_up_needed = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    vital_signs = models.JSONField(default=dict)  # Store BP, pulse, temp, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f"{self.patient} - {self.date_time}"