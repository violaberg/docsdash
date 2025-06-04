from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('create/', views.patient_create, name='patient_create'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('<int:pk>/toggle-status/', views.toggle_patient_status, name='toggle_patient_status'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    # Medical record additions
    path('<int:patient_pk>/add-allergy/', views.add_allergy, name='add_allergy'),
    path('<int:patient_pk>/add-chronic-condition/', views.add_chronic_condition, name='add_chronic_condition'),
    path('<int:patient_pk>/add-medication/', views.add_medication, name='add_medication'),
    path('<int:patient_pk>/add-medical-history/', views.add_medical_history, name='add_medical_history'),
    path('<int:patient_pk>/add-family-history/', views.add_family_history, name='add_family_history'),
    path('<int:patient_pk>/add-immunization/', views.add_immunization, name='add_immunization'),
    path('<int:patient_pk>/add-vital-signs/', views.add_vital_signs, name='add_vital_signs'),
    path('<int:patient_pk>/add-note/', views.add_note, name='add_note'),
    
    # Bulk actions
    path('bulk-action/', views.bulk_action, name='bulk_action'),
]
