from django.db import models
from django.core.validators import MinValueValidator

class Service(models.Model):
    """Business service model"""
    business = models.ForeignKey('tenants.Business', on_delete=models.CASCADE, related_name='services')
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