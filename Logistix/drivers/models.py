from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
from vehicles.models import Vehicle


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    vehicle = models.OneToOneField('vehicles.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    is_assigned = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def clean(self):
        """
        Custom validation method to validate the license number format
        and other fields.
        """
        if len(self.license_number) < 10:
            raise ValidationError("License number must be at least 10 characters long.")
        
        if Driver.objects.filter(vehicle=self.vehicle).exclude(pk=self.pk).exists():
            raise ValidationError("This vehicle is already assigned to another driver.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

