from django.contrib import admin
from .models import Business, BusinessSettings

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug', 'owner__email', 'phone']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']

@admin.register(BusinessSettings)
class BusinessSettingsAdmin(admin.ModelAdmin):
    list_display = ['business', 'timezone', 'currency', 'email_notifications', 'sms_notifications']
    list_filter = ['timezone', 'currency', 'email_notifications', 'sms_notifications']
    search_fields = ['business__name']
    ordering = ['business']
