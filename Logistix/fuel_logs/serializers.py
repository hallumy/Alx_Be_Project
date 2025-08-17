
from rest_framework import serializers
from .models import FuelLog

class FuelLogSerializer(serializers.ModelSerializer):
    fuel_consumption = serializers.ReadOnlyField()
    consumption_status = serializers.ReadOnlyField()

    class Meta:
        model = FuelLog
        fields = '__all__'
