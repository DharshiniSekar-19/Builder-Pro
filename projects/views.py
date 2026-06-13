from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Project
from .forms import ProjectForm
from activities.models import Activity, WBSItem
from accounts.decorators import project_manager_required, role_required

@login_required
def project_list(request):
    role = request.user.profile.role
    if role == 'super_admin':
        projects = Project.objects.all()
    elif role in ['project_manager']:
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = Project.objects.all()

    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    if search:
        projects = projects.filter(name__icontains=search)

    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
@project_manager_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', pk=project.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create Project'})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    activities = Activity.objects.filter(project=project)
    wbs_items = WBSItem.objects.filter(project=project, parent=None)
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'activities': activities,
        'wbs_items': wbs_items,
    })

@login_required
@project_manager_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', pk=project.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Edit Project', 'project': project})

@login_required
@project_manager_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def project_wbs(request, pk):
    project = get_object_or_404(Project, pk=pk)
    wbs_items = WBSItem.objects.filter(project=project, parent=None)
    return render(request, 'projects/wbs.html', {'project': project, 'wbs_items': wbs_items})

@login_required
def ajax_project_status_counts(request):
    projects = Project.objects.all()
    data = {
        'planning': projects.filter(status='planning').count(),
        'in_progress': projects.filter(status='in_progress').count(),
        'completed': projects.filter(status='completed').count(),
        'delayed': projects.filter(status='delayed').count(),
        'on_hold': projects.filter(status='on_hold').count(),
    }
    return JsonResponse(data)
