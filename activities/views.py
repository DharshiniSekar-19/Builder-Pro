from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Activity, Dependency, WBSItem
from projects.models import Project
from .forms import ActivityForm, WBSForm
from .cpm import run_cpm
from .pert import PERTAnalyzer
from accounts.decorators import project_manager_required, site_engineer_required, role_required

@login_required
def activity_list(request):
    project_id = request.GET.get('project')
    status = request.GET.get('status')
    search = request.GET.get('search')

    role = request.user.profile.role
    if role == 'super_admin':
        activities = Activity.objects.all()
    elif role == 'project_manager':
        projects = Project.objects.filter(created_by=request.user)
        activities = Activity.objects.filter(project__in=projects)
    elif role == 'site_engineer':
        activities = Activity.objects.filter(assigned_to=request.user)
    else:
        activities = Activity.objects.all()

    if project_id:
        activities = activities.filter(project_id=project_id)
    if status:
        activities = activities.filter(status=status)
    if search:
        activities = activities.filter(name__icontains=search)

    projects = Project.objects.all()
    return render(request, 'activities/activity_list.html', {
        'activities': activities,
        'projects': projects,
    })

@login_required
@project_manager_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save()
            messages.success(request, 'Activity created successfully!')
            return redirect('activity_detail', pk=activity.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm()
        project_id = request.GET.get('project')
        if project_id:
            form.fields['project'].initial = project_id
    return render(request, 'activities/activity_form.html', {'form': form, 'title': 'Create Activity'})

@login_required
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'activities/activity_detail.html', {'activity': activity})

@login_required
@project_manager_required
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_detail', pk=activity.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'activities/activity_form.html', {'form': form, 'title': 'Edit Activity', 'activity': activity})

@login_required
@project_manager_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    project_id = activity.project_id
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('activity_list')
    return render(request, 'activities/activity_confirm_delete.html', {'activity': activity})

@login_required
@site_engineer_required
def update_activity_status(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Activity.STATUS_CHOICES):
            activity.status = new_status
            activity.save()
            messages.success(request, f'Activity status updated to {activity.get_status_display()}')
    return redirect('activity_detail', pk=activity.pk)

@login_required
def cpm_analysis(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    critical_path = run_cpm(project)
    activities = Activity.objects.filter(project=project)

    critical_ids = [a.id for a in critical_path]
    non_critical = [a for a in activities if a.id not in critical_ids]

    project_duration = 0
    for a in critical_path:
        project_duration += a.expected_duration

    return render(request, 'activities/cpm_analysis.html', {
        'project': project,
        'critical_path': critical_path,
        'non_critical': non_critical,
        'project_duration': round(project_duration, 2),
    })

@login_required
def pert_analysis(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    activities = Activity.objects.filter(project=project)

    total_expected = sum(a.expected_duration for a in activities)
    total_variance = sum(a.variance for a in activities)
    total_std = total_variance ** 0.5

    return render(request, 'activities/pert_analysis.html', {
        'project': project,
        'activities': activities,
        'total_expected': round(total_expected, 2),
        'total_variance': round(total_variance, 4),
        'total_std': round(total_std, 2),
    })

@login_required
def pert_probability(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    activities = Activity.objects.filter(project=project)

    total_expected = sum(a.expected_duration for a in activities)
    total_variance = sum(a.variance for a in activities)
    total_std = total_variance ** 0.5

    target_days = float(request.GET.get('target_days', total_expected))
    probability = PERTAnalyzer.probability(target_days, total_expected, total_std)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'expected_duration': round(total_expected, 2),
            'variance': round(total_variance, 4),
            'standard_deviation': round(total_std, 2),
            'target_days': target_days,
            'probability': probability,
        })

    return render(request, 'activities/pert_probability.html', {
        'project': project,
        'total_expected': round(total_expected, 2),
        'total_variance': round(total_variance, 4),
        'total_std': round(total_std, 2),
        'target_days': target_days,
        'probability': probability,
    })

@login_required
@project_manager_required
def wbs_create(request):
    if request.method == 'POST':
        form = WBSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'WBS item created successfully!')
            return redirect('project_wbs', pk=form.cleaned_data['project'].pk)
    else:
        form = WBSForm()
    return render(request, 'activities/wbs_form.html', {'form': form})

@login_required
@project_manager_required
def wbs_edit(request, pk):
    item = get_object_or_404(WBSItem, pk=pk)
    if request.method == 'POST':
        form = WBSForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'WBS item updated!')
            return redirect('project_wbs', pk=item.project.pk)
    else:
        form = WBSForm(instance=item)
    return render(request, 'activities/wbs_form.html', {'form': form, 'item': item})

@login_required
def ajax_pert_data(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    data = {
        'optimistic_time': activity.optimistic_time,
        'most_likely_time': activity.most_likely_time,
        'pessimistic_time': activity.pessimistic_time,
        'expected_duration': activity.expected_duration,
        'variance': activity.variance,
        'standard_deviation': activity.standard_deviation,
    }
    return JsonResponse(data)
