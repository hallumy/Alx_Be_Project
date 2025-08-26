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
    weight  = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)

    
    fuel_used=models.FloatField()
    dnote_no = models.IntegerField()
    quantity  = models.IntegerField()
    total = models.FloatField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.standard_charge is not None:
            self.total = self.standard_charge
        elif None not in [self.weight, self.distance, self.unit_price, self.quantity]:
            self.total = (self.weight * self.distance * self.unit_price * self.quantity) / 1000
        else:
            self.total = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Trip {self.primary_id} - {self.product.code} on {self.route.origin} to {self.route.destination}"

class DeliveryNote(models.Model):
    dnote_no = models.CharField(max_length=50)
    trip = models.ForeignKey(Trips, related_name='delivery_notes', on_delete=models.CASCADE)

    def __str__(self):
        return self.dnote_no
