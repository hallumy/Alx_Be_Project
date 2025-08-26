from django.test import TestCase
from vehicles.models import Vehicle
from drivers.models import Driver
from product.models import Product
from route.models import Route
from your_app.models import Trips, DeliveryNote

class TripsModelTest(TestCase):

    def setUp(self):
        self.vehicle = Vehicle.objects.create(model="FRR", reg_number="ABC123")
        self.driver = Driver.objects.create(name="John Doe", license_number="D123")
        self.product = Product.objects.create(code="1 or 1A", weight_kg=10)
        self.route = Route.objects.create(origin="Origin A", destination="Destination B", distance=500)

        self.trip = Trips.objects.create(
            vehicle=self.vehicle,
            product=self.product,
            drivers=self.driver,
            route=self.route,
            unit_price=20.00,
            standard_charge=100.00,
            fuel_used=50.00,
            dnote_no=12345,
            quantity=5
        )

    def test_trip_total_with_standard_charge(self):
        """Test if total equals standard charge when provided."""
        self.assertEqual(self.trip.total, 100.00)

    def test_trip_total_without_standard_charge(self):
        """Test if total is calculated correctly when no standard charge."""
        self.trip.standard_charge = None
        self.trip.save()
        expected_total = (self.trip.weight * self.trip.distance * self.trip.unit_price * self.trip.quantity) / 1000
        self.assertEqual(self.trip.total, expected_total)

    def test_distance_property(self):
        """Test if distance property returns correct value from related Route model."""
        self.assertEqual(self.trip.distance, self.route.distance)

    def test_weight_property(self):
        """Test if weight property returns correct value from related Product model."""
        self.assertEqual(self.trip.weight, self.product.weight_kg)

    def test_str_method(self):
        """Test string representation of the trip."""
        expected_str = f"Trip {self.trip.id} - {self.product.code} on {self.route.origin} to {self.route.destination}"
        self.assertEqual(str(self.trip), expected_str)


class DeliveryNoteModelTest(TestCase):

    def setUp(self):
        self.vehicle = Vehicle.objects.create(model="FRR", reg_number="ABC123")
        self.driver = Driver.objects.create(name="John Doe", license_number="D123")
        self.product = Product.objects.create(code="1 or 1A", weight_kg=10)
        self.route = Route.objects.create(origin="Origin A", destination="Destination B", distance=500)
        self.trip = Trips.objects.create(
            vehicle=self.vehicle,
            product=self.product,
            drivers=self.driver,
            route=self.route,
            unit_price=20.00,
            standard_charge=100.00,
            fuel_used=50.00,
            dnote_no=12345,
            quantity=5
        )
        self.delivery_note = DeliveryNote.objects.create(dnote_no="D123", trip=self.trip)

    def test_delivery_note_str_method(self):
        """Test string representation of the DeliveryNote."""
        self.assertEqual(str(self.delivery_note), self.delivery_note.dnote_no)
