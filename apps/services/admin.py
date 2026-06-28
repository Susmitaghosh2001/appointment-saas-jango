from django.contrib import admin
from .models import ServiceType, Service

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'service_type', 'price', 'duration_minutes', 'is_active']
    list_filter = ['is_active', 'service_type', 'business', 'created_at']
    search_fields = ['name', 'description', 'business__name']
    ordering = ['-created_at']
