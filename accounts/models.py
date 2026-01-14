# # account/models/customuser.py

# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# from .manager import CustomUserManager

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     USER_TYPE_CHOICES = (
#         ('ADMIN', 'Admin'),
#         ('AGENT', 'Agent'),
#         ('USER', 'User'),
#     )
#     username = models.CharField(max_length=100)
#     # Add any additional fields you need for your user model: want to be agent   
#     agency_name = models.CharField(max_length=100, blank=True, null=True)
#     agency_address = models.CharField(max_length=255, blank=True, null=True)
#     agency_phone = models.CharField(max_length=20, blank=True, null=True)
#     agency_website = models.URLField(blank=True, null=True)
#     # Standard fields
#     agency_email = models.EmailField(blank=True, null=True)
    

#     email = models.EmailField(unique=True, verbose_name="Email Address")
#     first_name = models.CharField(max_length=30, verbose_name="First Name")
#     last_name = models.CharField(max_length=30, verbose_name="Last Name")
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='USER', verbose_name="User Type")
    
#     # Standard Django flags
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     # Timestamp fields (optional but often useful)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)

#     # Link the custom manager
#     objects = CustomUserManager()

#     # Set email as the unique identifier for authentication instead of username.
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('AGENT', 'Agent'),
        ('USER', 'User'),
        ('INVESTOR', 'Investor'),
        ('INTERNAL', 'Internal'),
    )

    # Basic info
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='USER', verbose_name="User Type")

    # Agent-specific optional fields
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    agency_address = models.CharField(max_length=255, blank=True, null=True)
    agency_phone = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    agency_website = models.URLField(blank=True, null=True)
    agency_email = models.EmailField(blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    # Standard Django flags
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # Link the custom manager
    objects = CustomUserManager()

    # Email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
