from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, Appointment
from .serializers import PatientSerializer, AppointmentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['medical_record_number', 'blood_type']
    search_fields = ['first_name', 'last_name', 'medical_record_number']
    ordering_fields = ['created_at', 'last_name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'follow_up_needed']
    ordering_fields = ['date_time', 'created_at']

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)