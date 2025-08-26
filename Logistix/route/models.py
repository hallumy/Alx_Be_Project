from django.db import models

class Route(models.Model):
    origin      = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    distance    = models.IntegerField()
    
    class Meta:
        db_table = 'route' 

    def __str__(self):
        return f"{self.origin} → {self.destination}"