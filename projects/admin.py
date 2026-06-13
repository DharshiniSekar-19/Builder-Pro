from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_name', 'status', 'start_date', 'end_date', 'budget', 'created_by']
    list_filter = ['status']
    search_fields = ['name', 'client_name', 'location']
