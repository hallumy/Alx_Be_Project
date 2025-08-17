# Users App (LogistiX)

This app handles **authentication, registration, and role-based permissions** for the LogistiX logistics management system.  

---

## Features

* Custom User model with roles:  
  • Admin  
  • Manager  
  • Driver  
  • Accountant  

* JWT Authentication (Login, Refresh, Logout)  
* Role-based access control  
* CRUD operations for users  

---

## API Endpoints

**Authentication**  
POST `/api/register/` → Register new user  
POST `/api/login/` → Login and get JWT tokens  
POST `/api/token/refresh/` → Refresh JWT token  
POST `/api/logout/` → Logout and blacklist token  

**User Management**  
GET `/api/users/` → List users (access depends on role)  
GET `/api/users/<id>/` → Get user details  
PUT `/api/users/<id>/` → Update user  
DELETE `/api/users/<id>/` → Delete user (admin only)  

---

## Permissions by Role

**Admin**  
Full access to all user data and actions  

**Manager**  
Can view and update users, but cannot delete  

**Driver**  
Can only update their own profile information  

**Accountant**  
Can only update accountant-related fields  

---

## Installation & Setup

1. Install dependencies  
   `pip install djangorestframework djangorestframework-simplejwt`

2. Add to `settings.py`  


3. Apply migrations  
`python manage.py makemigrations`  
`python manage.py migrate`

4. Run the server  
`python manage.py runserver`

