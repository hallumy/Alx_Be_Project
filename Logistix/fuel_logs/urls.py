from rest_framework.routers import DefaultRouter
from .views import FuelLogViewSet

router = DefaultRouter()
router.register(r'', FuelLogViewSet, name='fuel-log')  # /api/fuel-logs/

urlpatterns = router.urls

