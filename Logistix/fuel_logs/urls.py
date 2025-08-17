from rest_framework.routers import DefaultRouter
from .views import FuelLogViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', FuelLogViewSet, basename='fuel-log')  # /api/fuel-logs/

urlpatterns = [
    path('', include(router.urls)),
]
