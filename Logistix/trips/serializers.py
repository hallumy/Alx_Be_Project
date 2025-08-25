from rest_framework import serializers
from .models import Trips
from product.models import Product
from route.models import Route
from product.serializers import ProductSerializer 
from route.serializers import RouteSerializer
from vehicles.serializers import VehicleSerializer

class TripSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    product_code = serializers.CharField(source='product.code')
    product_weight = serializers.FloatField(source='product.weight_kg')
    route_origin = serializers.CharField(source='route.origin')
    route_destination = serializers.CharField(source='route.destination')
    reg_number = serializers.CharField(source='vehicle.reg_number')
    distance = serializers.IntegerField(source='route.distance')
    quantity = serializers.FloatField()
    total = serializers.ReadOnlyField()

    class Meta:
        model = Trips
        fields = [
            'id', 'product', 'product_code', 'product_weight', 'route', 'route_origin', 'route_destination',
            'distance', 'standard_charge','reg_number','dnote_no', 'fuel_used', 'weight', 'quantity', 'unit_price', 'total'
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than 0.")
        return value
