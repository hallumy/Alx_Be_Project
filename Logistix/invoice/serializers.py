from rest_framework import serializers
from .models import Invoice
from trips.serializers import TripSerializer  # import trips serializer

class InvoiceSerializer(serializers.ModelSerializer):
    # Show trips inside invoice
    trips = TripSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
