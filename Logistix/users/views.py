from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .serializers import UserSerializer 
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.

    Method: POST
    Access: Public (no authentication required)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    """
    API endpoint to authenticate and log in a user.

    Method: POST
    Access: Public
    Request data: { "email": "<user_email>", "password": "<user_password>" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle POST request to log in user.
        If credentials are valid, returns user info.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "email": user.email, "role": user.role})
        return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    """
    API endpoint to log out the current authenticated user.

    Method: POST
    Access: Authenticated users only
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        """
        Handle POST request to log out user.
        Clears session data.
        """
        logout(request)
        return Response({"message": "Logged out successfully"})

@api_view(['GET'])
def profile(request):
    """
    API endpoint to return the current authenticated user's profile.

    Method: GET
    Access: Authenticated users only
    """
    user = request.user
    return Response({
        "email": user.email,
        "role": user.role,
        "first_name": getattr(user, "first_name", ""),
        "last_name": getattr(user, "last_name", "")
    })

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    Admins and managers can see all users.
    Other roles can only see their own user data.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Set permissions dynamically based on action.
        - Allow anyone to create (register).
        - Allow only authenticated users to list/retrieve.
        - Restrict other actions to admin users.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        """
        Return different querysets based on user role.
        - Admins/managers: all users.
        - Others (e.g. driver): only their own data.
        """
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def drivers(self, request):
        """
        Custom endpoint to list all users with the role 'driver'.
        URL: /users/drivers/
        """
        drivers = User.objects.filter(role='driver')
        serializer = self.get_serializer(drivers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """
        Custom endpoint to get the authenticated user's own profile.
        URL: /users/profile/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)