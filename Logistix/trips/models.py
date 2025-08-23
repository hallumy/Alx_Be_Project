from django.db import models
from vehicles.models import Vehicle
from drivers.models import Driver
from product.models import Product
from route.models import Route
from invoice.models import Invoice

class Trips(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    drivers = models.ForeignKey(Driver, on_delete=models.CASCADE)
    code    = models.ForeignKey(Product, on_delete=models.CASCADE)
    route   = models.ForeignKey(Route, on_delete=models.CASCADE)
    distance= models.FloatField()
    price   = models.FloatField()
    date    = models.DateField(verbose_name='Date', auto_now_add=True)
    weight  = models.FloatField()
    Fuel_used=models.FloatField()
    invoice = models.ForeignKey(Invoice, related_name="trips", on_delete=models.CASCADE)