from django.db import models
from trips.models import Trips
from product.models import Product

class Invoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
        ("cancelled", "Cancelled"),
    ]
    code     = models.ForeignKey(Product, on_delete=models.CASCADE)
    DNote_no = models.CharField(max_length=20)
    trip     = models.ManyToManyField(Trips, on_delete=CASCADE)
    date_created = models.DateTimeField(verbose_name='Date Created', auto_add_now=True)
    status   = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    subtotal = models.FloatField(max_digit= 10, decimal_place=2)
    tax = models.FloatField(max_digit = 10, decimal_place=2)
    Total = models.FloatField(max_digit=10, decimal_place=2)

    def mark_as_paid(self):
        self.status = "paid"
        self.date_paid = timezone.now()
        self.save()
        
    def calculate_totals(self, tax_rate=0.16):
        """
        Adds all trips in the invioce and calculates
        totals with tax
        """
        subtotal = sum(trip.price for trip in self.trip.all())
        tax = subtotal * tax_rate
        self.subtotal = subtotal
        self.tax = tax
        self.total = subtotal + tax
        self.save()
        
    def __str__(self):
        return f"Invoice for {self.month.strftime('%B %Y')}"