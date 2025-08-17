
This app manages vehicle records for the **LogistiX** logistics management system.  
It provides CRUD operations for vehicles, including support for **vehicle tonnage categories** and integration with drivers, trips, and fuel logs.

---

## Features
• Add, view, update, and delete vehicles  
• Assign vehicle tonnage from predefined choices (e.g., 1 ton, 2 tons, etc.)  
• Store vehicle details such as:  
  - Registration number  
  - Model  
  - Fuel type  
  - Efficiency  
  - Last service date  
• Relationships with drivers and fuel logs  

---

## API Endpoints

### Vehicles
GET `/api/vehicles/` → List all vehicles  
POST `/api/vehicles/` → Create a new vehicle  
GET `/api/vehicles/{id}/` → Retrieve a specific vehicle  
PUT `/api/vehicles/{id}/` → Update a specific vehicle  
DELETE `/api/vehicles/{id}/` → Delete a specific vehicle  

---
