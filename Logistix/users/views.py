from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that adds additional user information to the token payload.
    """
    username_field = 'username'
    @classmethod
    def get_token(cls, user):
        """
        Customize the token payload to include email, role, and full name.
        """
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['name'] = f"{user.first_name} {user.last_name}".strip()
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Login view that uses the custom token serializer to provide enriched token payloads.

    Endpoint: POST /api/auth/login/
    """
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user.

    Endpoint: POST /api/auth/register/
    Access: Public
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.

    - Admins and managers can view all users.
    - Drivers and regular users can only see their own profile.
    - Includes custom actions for user profile and drivers list.

    Base endpoint: /api/auth/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Assign permissions based on the action being performed.
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'retrieve', 'profile', 'drivers']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        """
        Restrict queryset based on user's role:
        - Admins and managers see all users
        - Others see only themselves
        """
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        Retrieve the profile of the currently authenticated user.

        Endpoint: GET /api/auth/users/profile/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def drivers(self, request):
        """
        List all users with the role of 'driver'.

        Endpoint: GET /api/auth/users/drivers/
        """
        drivers = User.objects.filter(role='driver')
        serializer = self.get_serializer(drivers, many=True)
        return Response(serializer.data)


class LogoutView(APIView):
    """
    API view to logout a user by blacklisting their refresh token.

    Endpoint: POST /api/auth/logout/
    Required: refresh token in the request body
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Blacklist the provided refresh token to invalidate the session.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
