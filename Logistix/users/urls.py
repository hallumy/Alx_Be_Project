from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, RegisterView, UserViewSet, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
