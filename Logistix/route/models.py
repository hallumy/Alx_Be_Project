from django.db import models

class Route(models.Model):
    Origin      = models.CharField(max_length=30)
    Destination = models.CharField(max_length=30)
    Distance    = models.IntegerField()
    
class Meta:
    db_table = 'distance_table' 