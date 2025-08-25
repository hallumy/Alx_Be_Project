from django.shortcuts import render
from rest_framework import generics, status
from .models import Trips
from .serializers import TripSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class TripListView(generics.ListCreateAPIView):
    """
    Handles GET requests to list all trips and POST requests
    to create new trips. The queryset defines the trips in the 
    response, and the serializer determines how the model is 
    represented.
    """
    queryset = Trips.objects.all()
    serializer_class = TripSerializer

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET requests to retrieve, PUT/PATCH requests to update,
    and DELETE requests to remove a specific trip. The queryset 
    defines the trip instance, and the serializer controls how it's 
    represented.
    """
    queryset = Trips.objects.all()
    serializer_class = TripSerializer

@api_view(['GET'])
def get_product_weight(request, product_code):
    """
    Checks for the product code in the database
    Returns the weight of the product
    """
    try:
        product = Product.objects.get(code=product_code)
        return Response({'weight': product.weight_kg})
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

def get_distance(request, origin, destination):
    """
    Looks up the distance in the database and
    Returns the distance. Checks whether 
    Distance exists and gives a response
    """ 
    try:
        distance_entry = Distance.objects.get(origin=origin, destination=destination)
        return Response({'distance': distance_entry.distance})
    except Distance.DoesNotExist:
        return Response({'detail': 'Distance between these locations not found.'}, status=status.HTTP_404_NOT_FOUND)
