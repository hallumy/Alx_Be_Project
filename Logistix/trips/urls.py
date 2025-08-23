from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripListView.as_view(), name='trip-list'),       # GET all trips / POST new trip
    path('<int:pk>/', views.TripDetailView.as_view(), name='trip-detail'),  # GET/PUT/DELETE trip by ID
]
