from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet

router = DefaultRouter()
router.register(r'', VehicleViewSet, name='vehicle')  # /api/vehicles/

urlpatterns = router.urls

