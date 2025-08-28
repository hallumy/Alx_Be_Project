from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Trips, Product, Route
from .serializers import TripSerializer

class TripViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing trips.

    - Drivers can only create and view their own trips.
    - Admins and managers have full access.
    """
    serializer_class = TripSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'driver':
            return Trips.objects.filter(driver__user=user)
        return Trips.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_trip_data(self, data):
        """
        Automatically populate product and route info from minimal user input.
        """
        product_code = data.get('product_code')
        if not product_code:
            return None, Response({'detail': 'Product code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(code=product_code)
        except Product.DoesNotExist:
            return None, Response({'detail': 'Product not found.'}, status=status.HTTP_400_BAD_REQUEST)

        data['product'] = product.id
        data['weight'] = product.weight_kg

        origin = data.get('origin')
        destination = data.get('destination')
        if origin and destination:
            try:
                route = Route.objects.get(origin=origin, destination=destination)
                data['route'] = route.id
                data['distance'] = route.distance
            except Route.DoesNotExist:
                return None, Response({'detail': 'Route not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return data, None

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data, error_response = self.get_trip_data(data)
        if error_response:
            return error_response

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        trip = self.get_object()
        data = request.data.copy()
        data, error_response = self.get_trip_data(data)
        if error_response:
            return error_response

        serializer = self.get_serializer(trip, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        trip = self.get_object()
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
