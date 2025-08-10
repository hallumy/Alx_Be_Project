from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        """
        Creates and saves a user with the given email, role and 
        password.
        """
        
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Please enter a valid password")
        
        user = self.model(
            email=self.normalize_email(email),
            
        )
        
        if role == 'admin':
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
        elif role in ['driver', 'manager']:
            user.is_staff = True
            user.is_admin = False
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_admin = False
            user.is_superuser = False
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, role='admin', password=None):
        """
        Creates and saves a superuser with the given email and 
        password
        """
        user = self.create_user(
            email,
            role='admin',
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    last_login  = models.DateTimeField(verbose_name="Last Login", auto_now_add=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now=True)
    
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        """
        Checks if the user has specific permissions in the app_label
        like add, change, delete or view.
        """
        return self.is_admin or super().has_perm(perm, obj)
    
    def has_module_perm(self, app_label):
        """
        Checks whether the user has permissions to view the app 
        app_label
        """
        return self.is_admin or self.is_staff

