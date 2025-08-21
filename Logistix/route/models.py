from django.db import models

class Route(models.Model):
    Origin      = models.CharField(max_length=30)
    Destination = models.CharField(max_length=30)
    Distance    = models.IntegerField(max_length=20) 