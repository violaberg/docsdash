from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    """Decorator for views that require admin privileges."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def medical_staff_required(view_func):
    """Decorator for views that require medical staff privileges."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_medical_staff and not request.user.is_admin:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
