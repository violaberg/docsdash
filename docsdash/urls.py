"""
DocsDash URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('auth/', include('authentication.urls')),
    path('', include('django_pwa.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)