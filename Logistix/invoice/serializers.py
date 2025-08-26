from rest_framework import serializers
from .models import Invoice
from trips.serializers import TripSerializer  # import trips serializer

class InvoiceSerializer(serializers.ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)
    subtotal = serializers.FloatField(read_only=True)
    tax = serializers.FloatField(read_only=True)
    total = serializers.FloatField(read_only=True)
    delivery_notes = serializers.SerializerMethodField() 

    class Meta:
        model = Invoice
        fields = [
            'id',
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
        return obj.get_delivery_notes()