from django.shortcuts import render
from rest_framework import viewsets
from .models import Route
from .serializers import RouteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
