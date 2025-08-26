
from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, UserViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)), 
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', views.profile, name='profile'),
]
