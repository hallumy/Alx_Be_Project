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

    def list(self, request):
        """
        List all invoices.
        """
        invoices = self.get_queryset()
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new invoice.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific invoice by ID.
        """
        invoice = self.get_object()
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update an invoice.
        """
        invoice = self.get_object()
        serializer = self.get_serializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete an invoice.
        """
        invoice = self.get_object()
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

