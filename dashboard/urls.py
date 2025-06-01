from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('medical-references/', views.medical_references, name='medical_references'),
    path('drug-interaction/', views.check_drug_interaction, name='drug_interaction'),
    path('medical-calculator/', views.medical_calculator, name='medical_calculator'),
]