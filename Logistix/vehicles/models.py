from django.db import models

class Vehicle(models.Model):
    TONNAGE_CHOICES = [
        (1, '1 ton'),
        (2, '2 tons'),
        (3, '3 tons'),
        (4, '4 tons'),
        (5, '5 tons'),
        (6, '6 tons'),
        (7, '7 tons'),
        (8, '8 tons'),
        (9, '9 tons'),
        (10, '10 tons'),
        (12, '12 tons'),
        (15, '15 tons'),
        (20, '20 tons'),
        (28, '28 tons'),
        (30, '30 tons'),
]
    reg_number = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)
    efficiency = models.FloatField(help_text='km per litre', default= 0.00) # to write the formula later
    last_service_date = models.DateField(null=True, blank=True)
    tonnage = models.IntegerField(choices=TONNAGE_CHOICES, default=1, help_text='Vehicle weight')

    def __str__(self):
        return self.reg_number
