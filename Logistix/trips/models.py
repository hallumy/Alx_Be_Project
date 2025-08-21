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
    distance= models.FloatField(max_digit=8, decimal_place=2)
    price   = models.FloatField(max_digit=8, decimal_places=2)
    date    = models.DateField(_(""), auto_now=False, auto_now_add=False)
    weight  = models.FloatField(max_digit=8, decimal_places=2)
    Fuel_used=models.FloatField(max_digit=8, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)