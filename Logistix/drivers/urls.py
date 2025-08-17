from .views import DriverViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', DriverViewSet, basename='driver')  # /api/drivers/

urlpatterns = [
    path('', include(router.urls)),
]
