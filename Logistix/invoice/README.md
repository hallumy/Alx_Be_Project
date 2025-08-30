# Invoice App README

This app is part of the logistics system and handles **Invoice creation** and management. It associates **trips** with invoices, calculates the **subtotal**, **tax**, and **total**, and provides functionality for marking invoices as paid.

## Features:
- **Create and manage invoices**: Create invoices that track trips, associated vehicles, and calculate totals.
- **Automatic Total Calculation**: The app automatically calculates `subtotal`, `tax`, and `total` based on the trips selected for each invoice.
- **Invoice Status**: Manage invoice statuses such as "pending", "paid", "unpaid", and "cancelled".
- **Delivery Notes**: Collect and list all delivery note numbers associated with the invoice's trips.
- **Vehicle Validation**: Ensures that all trips in an invoice belong to the same vehicle (or vehicle type).

## Installation

To install and configure the Invoice app:

1. **Clone the repository**:

   git clone https://github.com/yourusername/invoice-app.git
Install dependencies:

pip install -r requirements.txt
Migrate the database:


python manage.py migrate
Create a superuser to access the Django admin:


python manage.py createsuperuser
Run the application:


python manage.py runserver
Access Django Admin at http://127.0.0.1:8000/admin to manage invoices.

Models:
Invoice Model:
invoice_number: A unique string representing the invoice number.

trips: Many-to-many relationship with trips. Allows multiple trips to be associated with one invoice.

vehicle: ForeignKey to a vehicle. Indicates the vehicle associated with the invoice.

status: Choices are "pending", "paid", "unpaid", or "cancelled".

subtotal: The sum of the total of each associated trip.

tax: The calculated tax on the subtotal.

total: The final total after adding tax to the subtotal.

Functions:
mark_as_paid(): Marks the invoice as paid and sets the date_paid field.

calculate_totals(): Automatically calculates the subtotal, tax, and total for the invoice.

clean(): Ensures all trips in the invoice belong to the same vehicle.

get_delivery_notes(): Collects all delivery note numbers from associated trips.

API Endpoints:
GET /invoices/: List all invoices.

POST /invoices/: Create a new invoice.

GET /invoices/{id}/: Retrieve a single invoice by its ID.

POST /invoices/{id}/mark_as_paid/: Mark the invoice as paid.

GET /invoices/{id}/delivery_notes/: Retrieve all delivery note numbers associated with the invoice.

Example of Creating an Invoice:

curl -X POST \
  http://127.0.0.1:8000/api/invoices/ \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "invoice_number": "INV-2025-001",
    "trip_ids": [1, 2, 3],
    "vehicle": 1,
    "status": "pending"
}'