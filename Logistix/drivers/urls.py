from .views import DriverViewSet

router = DefaultRouter()
router.register(r'', DriverViewSet, name='driver')  # /api/drivers/

urlpatterns = router.urls

