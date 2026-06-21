from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid

class Business(models.Model):
    """Tenant/Business model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='businesses')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BusinessSettings(models.Model):
    """Business configuration settings"""
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='settings')
    timezone = models.CharField(max_length=50, default='UTC')
    slot_duration = models.IntegerField(default=30, help_text='Duration in minutes')
    currency = models.CharField(max_length=3, default='USD')
    working_days = models.JSONField(default=dict, help_text='JSON field for working hours')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    reminder_emails = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.business.name}"