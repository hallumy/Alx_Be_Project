from django.db import models

class Product(models.Model):
    code        = models.IntegerField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    weight      = models.FloatField(max_length=10, decimal_places=2)
    
    def __str__(self):
        return self.code 
