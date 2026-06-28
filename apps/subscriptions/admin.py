from django.contrib import admin
from .models import Plan, Subscription

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'max_staff', 'max_services', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['price']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'business', 'plan', 'start_date', 'end_date', 'is_active', 'payment_status']
    list_filter = ['is_active', 'payment_status', 'plan', 'created_at']
    search_fields = ['business__name', 'plan__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
