from django.db import models
from vehicles.models import Vehicle
from drivers.models import Driver
from product.models import Product
from route.models import Route

class Trips(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    route   = models.ForeignKey(Route, on_delete=models.CASCADE)
    
    unit_price = models.FloatField(blank=True, null=True)
    standard_charge = models.FloatField(null=True, blank=True)
    date    = models.DateField(verbose_name='Date', auto_now_add=True)
    weight_kg  = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)

    
    fuel_used=models.FloatField()
    dnote_no = models.IntegerField()
    quantity  = models.IntegerField()
    total = models.FloatField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.product and not self.weight_kg:
            self.weight_kg = self.product.weight_kg
        if self.route and not self.distance:
            self.distance = self.route.distance

        if self.standard_charge is not None:
            self.total = self.standard_charge
        elif all(v is not None for v in [self.weight_kg, self.distance, self.unit_price, self.quantity]):
            self.total = (self.weight_kg * self.distance * self.unit_price * self.quantity) / 1000
        else:
            self.total = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Trip {self.id} {self.product.code} on {self.route.origin} to {self.route.destination} for {self.vehicle}"

