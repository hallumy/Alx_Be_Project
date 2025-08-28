from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Vehicle
from .serializers import VehicleSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class VehicleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting vehicles.
    Only authenticated users can perform these actions.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self, request):
        """
        Handle GET request for listing all vehicles.
        """
        vehicles = self.get_queryset()  # Get all vehicles
        serializer = self.get_serializer(vehicles, many=True)  # Serialize the data
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST request for creating a new vehicle.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new vehicle to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created vehicle data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Handle GET request for retrieving a specific vehicle by ID.
        """
        try:
            vehicle = self.get_object()  # Get the vehicle by ID
            serializer = self.get_serializer(vehicle)  # Serialize the vehicle data
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Handle PUT request to update an existing vehicle.
        """
        try:
            vehicle = self.get_object()  # Get the vehicle by ID
            serializer = self.get_serializer(vehicle, data=request.data)  # Validate and update the data
            if serializer.is_valid():
                serializer.save()  # Save the updated vehicle data
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehicle.DoesNotExist:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Handle DELETE request to remove a vehicle by ID.
        """
        try:
            vehicle = self.get_object()
            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({'detail': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)