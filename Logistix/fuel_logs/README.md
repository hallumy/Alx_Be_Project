This app manages **fuel usage records** for the **LogistiX** logistics management system.  
It provides APIs to log fuel consumption, calculate efficiency, and link records to vehicles.

---

## Features
• Create, view, update, and delete fuel log entries  
• Link logs to specific vehicles  
• Store details such as:  
  - Date of log  
  - Distance covered  
  - Fuel used  
  - Fuel cost  
• Auto-calculate **fuel consumption** (distance ÷ fuel used)  
• Support comparisons with vehicle tonnage (planned feature)  

---

## API Endpoints

### Fuel Logs
GET `/api/fuel-logs/` → List all fuel logs  
POST `/api/fuel-logs/` → Create a new fuel log  
GET `/api/fuel-logs/{id}/` → Retrieve a specific fuel log  
PUT `/api/fuel-logs/{id}/` → Update a fuel log  
DELETE `/api/fuel-logs/{id}/` → Delete a fuel log  

---
