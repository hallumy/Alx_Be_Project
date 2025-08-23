from django.urls import path
from . import views

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='invoice-list'),       # GET all invoices / POST new invoice
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),  # GET/PUT/DELETE invoice by ID
]
