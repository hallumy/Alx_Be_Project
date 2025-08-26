from rest_framework.test import APITestCase
from rest_framework import status
from trips.models import Trips

class TripTests(APITestCase):

    def test_create_trip(self):
        """
        Test creating a trip with valid data.
        """
        url = '/trips/create/'
        data = {
            'vehicle': 'Truck A',
            'product': '1A',
            'quantity': 10,
            'unit_price': 100.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['vehicle'], 'Truck A')
        self.assertEqual(response.data['quantity'], 10)

    def test_create_trip_missing_fields(self):
        """
        Test creating a trip with missing required fields.
        """
        url = '/trips/create/'
        data = {
            'vehicle': 'Truck A',
            'product': 'Product X'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)
        self.assertIn('unit_price', response.data)

    def test_get_trips(self):
        """
        Test fetching all trips.
        """
        # Create some trips
        Trip.objects.create(vehicle='Truck A', product='Product X', quantity=10, unit_price=100.0)
        Trip.objects.create(vehicle='Truck B', product='Product Y', quantity=5, unit_price=200.0)

        url = '/trips/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two trips created

    def test_get_trip(self):
        """
        Test fetching a specific trip by ID.
        """
        trip = Trip.objects.create(vehicle='Truck A', product='Product X', quantity=10, unit_price=100.0)
        url = f'/trip/{trip.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vehicle'], 'Truck A')

    def test_get_trip_not_found(self):
        """
        Test fetching a trip that doesn't exist.
        """
        url = '/trip/999999/'  # Invalid trip ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Trip not found')

    def test_update_trip(self):
        """
        Test updating an existing trip.
        """
        trip = Trip.objects.create(vehicle='Truck A', product='Product X', quantity=10, unit_price=100.0)
        url = f'/trip/update/{trip.id}/'
        data = {
            'vehicle': 'Truck B',
            'product': 'Product Y',
            'quantity': 15,
            'unit_price': 150.0
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vehicle'], 'Truck B')

    def test_update_trip_not_found(self):
        """
        Test updating a trip that doesn't exist.
        """
        url = '/trip/update/999999/'  # Invalid trip ID
        data = {
            'vehicle': 'Truck B',
            'product': 'Product Y',
            'quantity': 15,
            'unit_price': 150.0
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Trip not found')

    def test_delete_trip(self):
        """
        Test deleting an existing trip.
        """
        trip = Trip.objects.create(vehicle='Truck A', product='Product X', quantity=10, unit_price=100.0)
        url = f'/trip/delete/{trip.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_trip_not_found(self):
        """
        Test deleting a trip that doesn't exist.
        """
        url = '/trip/delete/999999/'  # Invalid trip ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Trip not found')

    def test_invalid_method_on_trip(self):
        """
        Test that invalid HTTP methods (like PATCH) return the correct error.
        """
        trip = Trip.objects.create(vehicle='Truck A', product='Product X', quantity=10, unit_price=100.0)
        url = f'/trip/{trip.id}/'
        response = self.client.patch(url, {}, format='json')  # PATCH is not allowed for this endpoint
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn('Method Not Allowed', response.data)
