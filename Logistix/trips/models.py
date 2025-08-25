from django.db import models
from vehicles.models import Vehicle
from drivers.models import Driver
from product.models import Product
from route.models import Route

class Trips(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    drivers = models.ForeignKey(Driver, on_delete=models.CASCADE)
    route   = models.ForeignKey(Route, on_delete=models.CASCADE)
    
    unit_price = models.FloatField(blank=True, null=True)
    standard_charge = models.FloatField(null=True, blank=True)
    date    = models.DateField(verbose_name='Date', auto_now_add=True)
    
    fuel_used=models.FloatField()
    dnote_no = models.IntegerField()
    quantity  = models.IntegerField()
    
    @property
    def distance(self):
        """
        Returns distance of the route for
        this trip
        """
        return self.route.distance

    @property
    def weight(self):
        """
        Returns the weight of one item of the product 
        carried
        """
        return self.product.weight_kg

    @property
    def total(self):
        if self.standard_charge is not None:
            return self.standard_charge
        if None in [self.weight, self.distance, self.unit_price, self.quantity]:
            return 0
        return (self.weight * self.distance * self.unit_price * self.quantity) /1000
    
    def __str__(self):
        return f"Trip {self.primary_id} - {self.product.code} on {self.route.origin} to {self.route.destination}"

class DeliveryNote(models.Model):
    dnote_no = models.CharField(max_length=50)
    trip = models.ForeignKey(Trips, related_name='delivery_notes', on_delete=models.CASCADE)

    def __str__(self):
        return self.dnote_no
