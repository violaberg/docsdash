from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings

from .forms import LoginForm, SignupForm, ProfileForm, PasswordResetForm
from .models import User, LoginAttempt, UserSession
from .decorators import admin_required

def login_view(request):
    """Handle user login with security features."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Record login attempt
            login_attempt = LoginAttempt(
                email=email,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Successful login
                login(request, user)
                login_attempt.user = user
                login_attempt.successful = True
                login_attempt.save()
                
                # Create user session
                UserSession.objects.create(
                    user=user,
                    session_key=request.session.session_key,
                    ip_address=request.META.get('REMOTE_ADDR', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # Update last login time
                user.last_login = timezone.now()
                user.save()
                
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                # Failed login
                login_attempt.save()
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    """Handle user logout."""
    if request.user.is_authenticated:
        # Update user session record
        UserSession.objects.filter(
            user=request.user,
            session_key=request.session.session_key,
            logged_out=False
        ).update(logged_out=True)
        
        logout(request)
    
    return redirect('login')

@admin_required
def signup_view(request):
    """Handle user registration (admin only)."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.email}')
            return redirect('user_management')
    else:
        form = SignupForm()
    
    return render(request, 'authentication/signup.html', {'form': form})

@login_required
def profile_view(request):
    """Handle user profile viewing and editing."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'authentication/profile.html', {'form': form})

def password_reset_view(request):
    """Handle password reset requests."""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # In a real app, this would send an email with a reset link
            # For this demo, we'll just show a success message
            messages.success(request, 'Password reset link sent to your email')
            return redirect('login')
    else:
        form = PasswordResetForm()
    
    return render(request, 'authentication/password_reset.html', {'form': form})

@admin_required
def user_management_view(request):
    """View for managing users (admin only)."""
    users = User.objects.all()
    return render(request, 'authentication/user_management.html', {'users': users})

@admin_required
def toggle_user_status(request, user_id):
    """Toggle a user's active status (admin only)."""
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.email} {status}')
    except User.DoesNotExist:
        messages.error(request, 'User not found')
    
    return redirect('user_management')

@login_required
def toggle_theme(request):
    """Toggle between light and dark themes."""
    user = request.user
    user.use_dark_theme = not user.use_dark_theme
    user.save()
    
    return JsonResponse({'success': True, 'dark_theme': user.use_dark_theme})

class SessionsView(LoginRequiredMixin, TemplateView):
    """View for managing active sessions."""
    template_name = 'authentication/sessions.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_sessions'] = UserSession.objects.filter(
            user=self.request.user,
            logged_out=False
        ).order_by('-last_activity')
        return context

@login_required
def end_session(request, session_id):
    """End a specific session."""
    try:
        session = UserSession.objects.get(id=session_id, user=request.user)
        session.logged_out = True
        session.save()
        messages.success(request, 'Session ended successfully')
    except UserSession.DoesNotExist:
        messages.error(request, 'Session not found')
    
    return redirect('sessions')
