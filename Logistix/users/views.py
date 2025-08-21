from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .serializers import UserSerializer 
from rest_framework.views import APIView
from rest_framework.decorators import api_view

User = get_user_model()

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Login

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "email": user.email, "role": user.role})
        return Response({"error": "Invalid credentials"}, status=400)

# Logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        logout(request)
        return Response({"message": "Logged out successfully"})

@api_view(['GET'])
def profile(request):
    user = request.user
    return Response({
        "email": user.email,
        "role": user.role,
        "first_name": getattr(user, "first_name", ""),
        "last_name": getattr(user, "last_name", "")
    })
