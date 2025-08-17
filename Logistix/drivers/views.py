from django.shortcuts import render
from rest_frmaework import viewsets
from .models import Driver
from .serializers import DriverSerializer
from rest_framework.permissions import IsAuthenticated

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission = [IsAuthenticated]
