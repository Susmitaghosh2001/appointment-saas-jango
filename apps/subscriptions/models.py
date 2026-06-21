from django.db import models
from django.core.validators import MinValueValidator
import uuid

class Plan(models.Model):
    """Subscription plan model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    max_staff = models.IntegerField(null=True, blank=True, help_text='Unlimited if null')
    max_services = models.IntegerField(null=True, blank=True, help_text='Unlimited if null')
    booking_limit = models.IntegerField(null=True, blank=True, help_text='Monthly booking limit')
    duration_days = models.IntegerField(default=30, help_text='Subscription duration in days')
    features = models.JSONField(default=dict, help_text='Additional features')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    """Business subscription model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey('tenants.Business', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business.name} - {self.plan.name}"