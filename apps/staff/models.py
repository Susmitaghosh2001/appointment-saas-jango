from django.db import models

class Staff(models.Model):
    """Staff member model"""
    business = models.ForeignKey('tenants.Business', on_delete=models.CASCADE, related_name='staff_members')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='staff_profiles')
    phone = models.CharField(max_length=20, blank=True)
    services = models.ManyToManyField('services.Service', related_name='staff', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'staff'
        unique_together = ['business', 'user']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.business.name}"

class StaffAvailability(models.Model):
    """Staff availability schedule"""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['staff', 'day_of_week']
        verbose_name_plural = 'staff availabilities'

    def __str__(self):
        return f"{self.staff} - {self.get_day_of_week_display()}"