from django.shortcuts import render
from rest_framework import viewsets
from .models import FuelLog
from .serializers import FuelLogSerializer
from rest_framework.permissions import IsAuthenticated

class FuelLogViewSet(viewsets.ModelViewSet):
    queryset = FuelLog.objects.all()
    serializer_class = FuelLogSerializer
    permission = [IsAuthenticated]
