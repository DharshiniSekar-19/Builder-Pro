from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_list, name='activity_list'),
    path('create/', views.activity_create, name='activity_create'),
    path('<int:pk>/', views.activity_detail, name='activity_detail'),
    path('<int:pk>/edit/', views.activity_edit, name='activity_edit'),
    path('<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    path('<int:pk>/update-status/', views.update_activity_status, name='update_activity_status'),
    path('cpm/<int:project_id>/', views.cpm_analysis, name='cpm_analysis'),
    path('pert/<int:project_id>/', views.pert_analysis, name='pert_analysis'),
    path('pert/<int:project_id>/probability/', views.pert_probability, name='pert_probability'),
    path('wbs/create/', views.wbs_create, name='wbs_create'),
    path('wbs/<int:pk>/edit/', views.wbs_edit, name='wbs_edit'),
    path('ajax/<int:pk>/pert-data/', views.ajax_pert_data, name='ajax_pert_data'),
]
