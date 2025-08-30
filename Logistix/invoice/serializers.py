from rest_framework import serializers
from .models import Invoice
from trips.serializers import TripSerializer  # import trips serializer
from vehicles.models import Vehicle

class InvoiceSerializer(serializers.ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)
    trip_ids = serializers.PrimaryKeyRelatedField(
        queryset=Invoice.trips.field.related_model.objects.all(),  # Trips model
        many=True,
        write_only=True,
        source='trips'
    )
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    
    vehicle_reg_number = serializers.CharField(source='vehicle.reg_number', read_only=True)
    delivery_notes = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'trip_ids',
            'invoice_number',
            'trips',
            'subtotal',
            'tax',
            'total',
            'status',
            'date_created',
            'delivery_notes',
        ]
    
    def get_delivery_notes(self, obj):
        """
        Returns a list of delivery note numbers associated with the invoice's trips.
        """
        return obj.get_delivery_notes()

    def validate_trip_ids(self, trips):
        """
        Ensures that all selected trips are from the same vehicle.
        Raises a ValidationError if trips span multiple vehicles.
        """
        vehicle = self.initial_data.get('vehicle')
        if not vehicle:
            raise serializers.ValidationError("Vehicle is required to validate trips.")

        vehicle_id = int(vehicle)
        for trip in trips:
            if trip.vehicle_id != vehicle_id:
                raise serializers.ValidationError(
                    f"Trip {trip.id} does not belong to the selected vehicle."
                )
        return trips

    def create(self, validated_data):
        """
        Create invoice and compute subtotal, tax, and total based on trip totals.
        Totals are calculated automatically by the model's save() method.
        """
        trips = validated_data.pop('trips', [])
        invoice = Invoice(**validated_data)
        invoice.full_clean()  
        invoice.save()
        invoice.trips.set(trips)
        invoice.calculate_totals()
        invoice.save()  
        return invoice