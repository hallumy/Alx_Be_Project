from django.shortcuts import render
from rest_framework import viewsets
from .models import FuelLog
from .serializers import FuelLogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class FuelLogViewSet(viewsets.ModelViewSet):
    queryset = FuelLog.objects.all()
    serializer_class = FuelLogSerializer
    permission = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

