from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('create/<int:patient_id>/', views.appointment_create, name='appointment_create_for_patient'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/status/<str:status>/', views.appointment_status_update, name='appointment_status_update'),
    
    # Appointment related actions
    path('<int:appointment_pk>/add-prescription/', views.add_prescription, name='add_prescription'),
    path('<int:appointment_pk>/add-lab-order/', views.add_lab_order, name='add_lab_order'),
    path('<int:appointment_pk>/add-follow-up/', views.add_follow_up, name='add_follow_up'),
    path('follow-up/<int:follow_up_pk>/schedule/', views.schedule_follow_up, name='schedule_follow_up'),
    
    # Appointment types
    path('types/', views.appointment_type_list, name='appointment_type_list'),
    path('types/<int:pk>/edit/', views.appointment_type_edit, name='appointment_type_edit'),
    path('types/<int:pk>/toggle-status/', views.toggle_appointment_type_status, name='toggle_appointment_type_status'),
    
    # Calendar
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.get_calendar_events, name='get_calendar_events'),
]
