from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Driver
from .serializers import DriverSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class DriverViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting drivers.
    Only authenticated users can perform these actions.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Handle GET request to list all drivers.
        Returns a list of all driver records.
        """
        drivers = self.get_queryset()
        serializer = self.get_serializer(drivers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST request to create a new driver.
        Validates and saves the driver data provided in the request.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Handle GET request to retrieve a single driver by ID.
        Returns the driver's details.
        """
        driver = self.get_object()
        serializer = self.get_serializer(driver)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Handle PUT request to update a driver's information.
        Validates and updates the existing driver record.
        """
        driver = self.get_object()
        serializer = self.get_serializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Handle DELETE request to remove a driver by ID.
        Permanently deletes the driver record.
        """
        driver = self.get_object()
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

