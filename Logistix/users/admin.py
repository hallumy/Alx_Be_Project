from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

class CustomUserAdmin(BaseUserAdmin):
    #The forms to add or change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    
    # The fields to be used in displaying the User model
    # They override the definitions on the base UserAdmin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    #Fields when creating a new user from the admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "role", "password1", "password2", "is_active", "is_staff")
        }),
    )    
    
    list_display = ("email", "role", "is_active", "is_staff", "last_login", "date_joined")
    list_filter = ("is_active", "is_staff", "role")
    search_fields = ("email",)
    ordering = ("email",)
    
    readonly_fields = ("last_login", "date_joined")
        
admin.site.register(User, CustomUserAdmin)
# Registers new UserAdmin
