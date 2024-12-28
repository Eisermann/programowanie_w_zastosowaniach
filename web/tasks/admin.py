from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'assigned_to')
    search_fields = ('title', 'description')
