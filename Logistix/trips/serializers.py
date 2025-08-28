from rest_framework import serializers
from .models import Trips
from product.models import Product
from route.models import Route
from vehicles.models import Vehicle
from drivers.models import Driver

class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trips model.

    Handles input for creating/updating trips using primary key references,
    and outputs detailed trip-related fields including related model data.
    """

    product_code = serializers.CharField(source='product.code', read_only=True)
    product_weight = serializers.FloatField(source='product.weight_kg', read_only=True)
    route_origin = serializers.CharField(source='route.origin', read_only=True)
    route_destination = serializers.CharField(source='route.destination', read_only=True)
    reg_number = serializers.CharField(source='vehicle.reg_number', read_only=True)
    distance = serializers.IntegerField(source='route.distance', read_only=True)
    weight = serializers.FloatField(read_only=True)
    total = serializers.FloatField(read_only=True)

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())

    class Meta:
        model = Trips
        fields = [
            'id',
            'product', 'product_code', 'product_weight',
            'route', 'route_origin', 'route_destination', 'distance',
            'vehicle', 'reg_number',
            'driver', 'dnote_no', 'fuel_used',
            'quantity', 'unit_price', 'standard_charge',
            'weight', 'total'
        ]

    def validate(self, data):
        """
        Restrict fields if the user is a driver.
        """
        user = self.context['request'].user
        if hasattr(user, 'role') and user.role == 'driver':
            # Fields drivers are allowed to set
            allowed_fields = {
                'product', 'route', 'vehicle', 'dnote_no', 'quantity'
            }

            for field in data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError(f"Drivers cannot set '{field}' field.")

        return data
    
    def create(self, validated_data):
        """
        Automatically assign the driver from request.user for drivers.
        """
        user = self.context['request'].user
        if hasattr(user, 'role') and user.role == 'driver':
            driver_instance = Driver.objects.filter(user=user).first()
            if not driver_instance:
                raise serializers.ValidationError("Driver profile not found for this user.")
            validated_data['driver'] = driver_instance

        return super().create(validated_data)


    def validate_quantity(self, value):
        """
        Ensure quantity is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def validate_unit_price(self, value):
        """
        Ensure unit price is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than 0.")
        return value
