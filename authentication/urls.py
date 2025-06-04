from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from . import views
from .forms import PasswordChangeCustomForm

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='authentication/password_change.html',
        form_class=PasswordChangeCustomForm,
        success_url='/auth/profile/'
    ), name='password_change'),
    path('user-management/', views.user_management_view, name='user_management'),
    path('toggle-user-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('sessions/', views.SessionsView.as_view(), name='sessions'),
    path('end-session/<int:session_id>/', views.end_session, name='end_session'),
]
