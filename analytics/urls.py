from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics_dashboard'),
    path('project/<int:pk>/report/', views.project_report, name='project_report'),
    path('project/<int:pk>/cpm-report/', views.cpm_report, name='cpm_report'),
    path('project/<int:pk>/pert-report/', views.pert_report, name='pert_report'),
    path('project/<int:pk>/export-excel/', views.export_project_excel, name='export_project_excel'),
    path('export-activities-excel/', views.export_activities_excel, name='export_activities_excel'),
    path('ajax/chart-data/', views.ajax_chart_data, name='ajax_chart_data'),
]
