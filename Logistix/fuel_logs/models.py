from django.db import models
from vehicles.models import Vehicle 

class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    distance = models.FloatField()
    fuel_used = models.FlaotField()

    @property
    def fuel_consumption(self):
        if self.fuel_used:
            return self.distance / self.fuel_used
        return 0

    def consumption_status(self):
        """
        Compares fuel consumption based on vehicle tonnage
        in km per litre
        """
        consumption = self.fuel_consumption
        vehicle_tonnage = self.vehicle.tonnage

        if vehicle_tonnage < 5:
            low, high = 8, 6
        elif vehicle_tonnage < 10:
            low, high = 5, 4
        elif vehicle_tonnage < 18:
            low, high = 4, 3
        else:
            low, high = 3, 2

        if consumption < low:
            return "Below expected range"
        elif consumption > high:
            return "Above expected range"
        else:
            return "Within expected range" 
