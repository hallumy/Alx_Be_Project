This app manages driver records for the **LogistiX** logistics management system.  
It provides CRUD operations for drivers and connects them to vehicles and trips.

---

## Features
• Create, view, update, and delete driver records  
• Link drivers to user accounts (role-based access)  
• Assign drivers to vehicles  
• Store details such as:  
  - Full name  
  - License number  
  - Phone number  
  - Assigned vehicle  

---

## API Endpoints

### Drivers
GET `/api/drivers/` → List all drivers  
POST `/api/drivers/` → Create a new driver  
GET `/api/drivers/{id}/` → Retrieve a specific driver  
PUT `/api/drivers/{id}/` → Update a driver  
DELETE `/api/drivers/{id}/` → Delete a driver  

---
