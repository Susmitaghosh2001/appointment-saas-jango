from django.db import models
from django.core.validators import MinValueValidator

class ServiceType(models.Model):
    """Service type/category model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class name')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Type'
        verbose_name_plural = 'Service Types'
        ordering = ['name']

    def __str__(self):
        return self.name

class Service(models.Model):
    """Business service model"""
    business = models.ForeignKey('tenants.Business', on_delete=models.CASCADE, related_name='services')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name='services', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(5)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['business', 'name']

    def __str__(self):
        return f"{self.business.name} - {self.name}"