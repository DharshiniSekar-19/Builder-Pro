from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from projects.models import Project
from activities.models import Activity
from .decorators import role_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    role = user.profile.role if hasattr(user, 'profile') else 'viewer'

    if role == 'super_admin':
        projects = Project.objects.all()
        activities = Activity.objects.all()
    elif role == 'project_manager':
        projects = Project.objects.filter(created_by=user)
        activities = Activity.objects.filter(project__in=projects)
    elif role == 'site_engineer':
        activities = Activity.objects.filter(assigned_to=user)
        projects = Project.objects.filter(activities__in=activities).distinct()
    else:
        projects = Project.objects.all()
        activities = Activity.objects.all()

    total_projects = projects.count()
    active_projects = projects.filter(status='in_progress').count()
    completed_projects = projects.filter(status='completed').count()
    delayed_projects = projects.filter(status='delayed').count()

    total_activities = activities.count()
    completed_activities = activities.filter(status='completed').count()
    critical_activities = activities.filter(is_critical=True).count()

    project_status_data = {
        'planning': projects.filter(status='planning').count(),
        'in_progress': active_projects,
        'completed': completed_projects,
        'delayed': delayed_projects,
        'on_hold': projects.filter(status='on_hold').count(),
    }

    activity_status_data = {
        'not_started': activities.filter(status='not_started').count(),
        'in_progress': activities.filter(status='in_progress').count(),
        'completed': completed_activities,
    }

    recent_projects = projects.order_by('-created_at')[:5]
    recent_activities = activities.order_by('-created_at')[:5]

    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'delayed_projects': delayed_projects,
        'total_activities': total_activities,
        'completed_activities': completed_activities,
        'critical_activities': critical_activities,
        'project_status_data': project_status_data,
        'activity_status_data': activity_status_data,
        'recent_projects': recent_projects,
        'recent_activities': recent_activities,
    }
    return render(request, 'accounts/dashboard.html', context)
