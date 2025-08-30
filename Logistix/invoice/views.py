from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        invoice = self.get_object()
        invoice.mark_as_paid()
        return Response({'status': 'Invoice marked as paid.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def delivery_notes(self, request, pk=None):
        invoice = self.get_object()
        notes = invoice.get_delivery_notes()
        return Response({'delivery_notes': notes}, status=status.HTTP_200_OK)