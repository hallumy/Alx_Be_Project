from django.db import models
from product.models import Product
from django.utils import timezone
from trips.models import Trips
from vehicles.models import Vehicle
from django.core.exceptions import ValidationError



class Invoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
        ("cancelled", "Cancelled"),
    ]
    invoice_number = models.CharField(max_length=100, unique=True)
    trips          = models.ManyToManyField(Trips, related_name="invoices")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank = True, related_name='invoices')
    date_created   = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    subtotal       = models.FloatField()
    tax            = models.FloatField()
    total          = models.FloatField()

    def mark_as_paid(self):
        self.status = "paid"
        self.date_paid = timezone.now()
        self.save()
        
    def calculate_totals(self, tax_rate=0.16):
        """
        Adds all trips in the invioce and calculates
        totals with tax
        """
        trips = self.trips.all()
        subtotal = sum(trip.total for trip in trips)
        tax = subtotal * tax_rate
        self.subtotal = subtotal
        self.tax = tax
        self.total = subtotal + tax

    def save(self, *args, **kwargs):
        if self.pk is not None and not self.trips.exists():
            self.trips.set(self.trips.all())
        super().save(*args, **kwargs)
        if self.trips.exists():
            self.calculate_totals()
            super().save(update_fields=["subtotal", "tax", "total"])
    
    def clean(self):
        if not self.pk:
            return

        super().clean()
        trips = self.trips.all()
        if self.trips.count() > 1:
            reg_numbers = [trip.vehicle.registration_number for trip in self.trips.all()]
            if len(set(reg_numbers)) > 1:
                raise ValidationError("All trips in an invoice must belong to the same vehicle (registration number).")
            if self.vehicle_id and self.vehicle_id not in vehicle_ids:
                raise ValidationError("Selected vehicle does not match the trips' vehicle.")


    def get_delivery_notes(self):
        """
        Collect all delivery note numbers from all trips in this invoice.
        """
        delivery_notes = []
        for trip in self.trips.all():
            delivery_notes.extend(trip.delivery_notes.values_list('dnote_no', flat=True))
        return list(set(delivery_notes))
        
    def __str__(self):
        date_str = self.date_created.strftime('%Y-%m-%d') if self.date_created else "No Date"
        return f"Invoice {self.invoice_number} - Created on {date_str}"
