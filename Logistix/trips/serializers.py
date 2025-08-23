from rest_framework import serializers
from .models import Trips

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = '__all__'   