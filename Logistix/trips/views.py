from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Trips, Product, Route
from .serializers import TripSerializer

class TripViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing trips. Handles CRUD operations.
    """
    queryset = Trips.objects.all()
    serializer_class = TripSerializer

    def get_product_weight(self, product_code):
        """
        Retrieve the weight of a product by its code.
        """
        if not product_code:
            return None

        cleaned_code = product_code.replace(',', '').strip()

        try:
            product = Product.objects.get(code=cleaned_code)
            return product.weight_kg
        except Product.DoesNotExist:
            return None

    def get_distance(self, origin, destination):
        """
        Retrieve the distance between two locations.
        """
        try:
            distance_entry = Route.objects.get(origin=origin, destination=destination)
            return distance_entry.distance
        except Route.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None):
        """
        Handle PUT request to update an existing trip.
        You may also want to recalculate and update the product weight or distance here.
        """
        trip = self.get_object()
        
        product_code = request.data.get('product_code', trip.product_code)  
        origin = request.data.get('origin', trip.origin)  
        destination = request.data.get('destination', trip.destination) 
        
        product_weight = self.get_product_weight(product_code)
        trip_distance = self.get_distance(origin, destination)

        if not product_weight:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if not trip_distance:
            return Response({'detail': 'Distance between origin and destination not found.'}, status=status.HTTP_400_BAD_REQUEST)
 
        request.data['weight'] = product_weight
        request.data['distance'] = trip_distance

        serializer = self.get_serializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Handle DELETE request to remove a trip.
        """
        trip = self.get_object()
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)