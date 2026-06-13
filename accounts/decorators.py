from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            role = request.user.profile.role
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to access this page.")
        return wrapper
    return decorator

def super_admin_required(view_func):
    return role_required(['super_admin'])(view_func)

def project_manager_required(view_func):
    return role_required(['super_admin', 'project_manager'])(view_func)

def site_engineer_required(view_func):
    return role_required(['super_admin', 'project_manager', 'site_engineer'])(view_func)
