from django.shortcuts import render
from rest_framework import generics
from .models import Trips
from .serializers import TripSerializer

class TripListView(generics.ListCreateAPIView):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer

