from rest_framework.routers import DefaultRouter
from .views import RouteViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]