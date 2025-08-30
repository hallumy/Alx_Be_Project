from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user  
        from django.contrib.auth.models import BaseUserManager    

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and 
        password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
            
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('manager', 'Manager'),
        ('dispatcher', 'Dispatcher'),
        ('accountant', 'Accountant'),
    ]
    # User Fields
    username    = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email       = models.EmailField(verbose_name="Email", max_length=255, unique=True) 
    role        = models.CharField(max_length=20, choices=ROLES, default='driver')
    # Profile Fields
    first_name  = models.CharField(max_length=30, blank=True, null=True)
    last_name   = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address     = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # Permissions Field
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    # Metadata
    last_login  = models.DateTimeField(verbose_name="Last Login", null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.first_name or self.email or "User"
    
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
