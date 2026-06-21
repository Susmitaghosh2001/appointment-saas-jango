from django.db import models
from django.core.validators import MinValueValidator
import uuid

class Booking(models.Model):
    """Appointment booking model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey('tenants.Business', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('services.Service', on_delete=models.PROTECT, related_name='bookings')
    staff = models.ForeignKey('staff.Staff', on_delete=models.PROTECT, related_name='bookings', null=True, blank=True)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date', '-start_time']

    def __str__(self):
        return f"{self.customer.email} - {self.service.name} - {self.booking_date}"

class BlockedSlot(models.Model):
    """Staff blocked time slots"""
    staff = models.ForeignKey('staff.Staff', on_delete=models.CASCADE, related_name='blocked_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.date} {self.start_time}-{self.end_time}"