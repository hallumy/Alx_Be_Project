from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Vehicle` model. Handles serialization, validation, and creation of vehicle records.
    """
    class Meta:
        model = Vehicle
        fields = ['id', 'reg_number', 'model', 'fuel_type', 'efficiency', 'last_service_date', 'tonnage']

    
    def validate_reg_number(self, value):
        """
        Ensures the vehicle registration number is unique.
        """
        if Vehicle.objects.filter(reg_number=value).exists():
            raise serializers.ValidationError("A vehicle with this registration number already exists.")
        return value

    def validate_efficiency(self, value):
        """
        Ensures that the fuel efficiency is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Fuel efficiency must be greater than zero.")
        return value

    def validate_tonnage(self, value):
        """
        Ensures the tonnage is within a valid range from 1 to 30.
        """
        if value not in dict(Vehicle.TONNAGE_CHOICES).keys():
            raise serializers.ValidationError("Invalid tonnage value.")
        return value

