from django.contrib import admin
from .models import Activity, Dependency, WBSItem

class DependencyInline(admin.TabularInline):
    model = Dependency
    fk_name = 'activity'
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'priority', 'status', 'expected_duration', 'is_critical', 'float_time']
    list_filter = ['status', 'priority', 'is_critical']
    search_fields = ['name', 'project__name']
    inlines = [DependencyInline]

@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ['activity', 'predecessor_activity']

@admin.register(WBSItem)
class WBSItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'parent', 'progress']
