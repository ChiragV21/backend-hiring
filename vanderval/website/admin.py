from django.contrib import admin
from .models import Site, UserRecords, JobExecution

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'domain', 'url', 'record_capicity', 'description')
    
    # Search functionality for specified fields
    search_fields = ('name', 'domain', 'url')
    
    # Filter by record capacity
    list_filter = ('record_capicity',)

@admin.register(UserRecords)
class UserRecordsAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'email', 'phone', 'dob', 'country', 'state', 'city', 'pincode', 'is_active')
    
    # Search functionality for specified fields
    search_fields = ('name', 'email', 'phone', 'country', 'state', 'city')
    
    # Filters for the admin list view
    list_filter = ('is_active', 'country', 'state')
    
    # Optional: Organize fields in the detail view
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'dob', 'email', 'phone')
        }),
        ('Address Details', {
            'fields': ('address', 'country', 'state', 'city', 'pincode')
        }),
        ('Other Details', {
            'fields': ('site', 'is_active')
        }),
    )

@admin.register(JobExecution)
class JobExecutionAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('task_type', 'status', 'site', 'created_at', 'started_at', 'finished_at')
    
    # Search functionality for specified fields
    search_fields = ('task_type', 'status', 'site__name')
    
    # Filters for the admin list view
    list_filter = ('status', 'task_type', 'site')

    # Read-only fields for tracking time
    readonly_fields = ('created_at', 'started_at', 'finished_at')
