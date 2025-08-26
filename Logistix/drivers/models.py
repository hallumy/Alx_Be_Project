from django.db import models
from users.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    assigned_vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.email

    def clean(self):
        """
        Custom validation method to validate the license number format
        and other fields.
        """
        if len(self.license_number) < 10:
            raise ValidationError("License number must be at least 10 characters long.")
        
        if self.assigned_vehicle:
            if self.assigned_vehicle.is_assigned:
                raise ValidationError("This vehicle is already assigned to another driver.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

