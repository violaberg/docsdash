from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from patients.models import Patient

class AppointmentType(models.Model):
    """Model for appointment types/templates."""
    
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True, null=True)
    default_notes = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=20, default='#305F6D')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    """Model for patient appointments."""
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.ForeignKey(AppointmentType, on_delete=models.CASCADE)
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider_appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_type.name} on {self.start_time}"
    
    @property
    def is_past(self):
        from django.utils import timezone
        return self.end_time < timezone.now()

class Prescription(models.Model):
    """Model for prescriptions given during appointments."""
    
    FREQUENCY_CHOICES = (
        ('once_daily', 'Once Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times_daily', 'Three Times Daily'),
        ('four_times_daily', 'Four Times Daily'),
        ('as_needed', 'As Needed'),
        ('other', 'Other (See Notes)'),
    )
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    duration_days = models.PositiveIntegerField(default=30)
    refills = models.PositiveIntegerField(default=0)
    instructions = models.TextField()
    notes = models.TextField(blank=True, null=True)
    prescribed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_prescribed = models.DateField(auto_now_add=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.medication_name} {self.dosage} for {self.appointment.patient.full_name}"

class LabOrder(models.Model):
    """Model for lab orders associated with appointments."""
    
    STATUS_CHOICES = (
        ('ordered', 'Ordered'),
        ('collected', 'Specimen Collected'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='lab_orders')
    lab_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_date = models.DateField(auto_now_add=True)
    results_date = models.DateField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.lab_name} for {self.appointment.patient.full_name}"

class FollowUp(models.Model):
    """Model for follow-up appointments."""
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='follow_ups')
    recommended_time_frame = models.CharField(max_length=100)
    reason = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    notes = models.TextField(blank=True, null=True)
    is_scheduled = models.BooleanField(default=False)
    follow_up_appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_follow_up')
    
    # Audit trail
    history = HistoricalRecords()
    
    def __str__(self):
        status = "Scheduled" if self.is_scheduled else "Not Scheduled"
        return f"Follow-up for {self.appointment.patient.full_name} ({status})"
