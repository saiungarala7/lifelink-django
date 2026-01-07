# """
# Custom User Model with Role-Based Access Control (RBAC)
# """
# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class User(AbstractUser):
#     """
#     Custom User model extending AbstractUser
#     Includes role-based access control and location tracking
#     """
#     ROLE_CHOICES = [
#         ('donor', 'Donor'),
#         ('bloodbank', 'Blood Bank'),
#         ('patient', 'Patient'),
#     ]
    
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     location_name = models.CharField(max_length=255, null=True, blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
    
#     def __str__(self):
#         return f"{self.username} ({self.get_role_display()})"
    
#     def is_donor(self):
#         """Check if user is a donor"""
#         return self.role == 'donor'
    
#     def is_bloodbank(self):
#         """Check if user is a blood bank"""
#         return self.role == 'bloodbank'
    
#     def is_patient(self):
#         """Check if user is a patient"""
#         return self.role == 'patient'

"""
Custom User Model with Role-Based Access Control (RBAC)
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    Includes role-based access control and location tracking
    """

    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('bloodbank', 'Blood Bank'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)

    is_email_verified = models.BooleanField(default=False)  # 👈 ADD THIS

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ROLE
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # ✅ EMAIL MUST BE UNIQUE (ONLY CHANGE THAT MATTERS)
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )

    # LOCATION FIELDS
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True
    )
    location_name = models.CharField(
        max_length=255,
        null=True, blank=True
    )

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # ROLE HELPERS
    def is_donor(self):
        return self.role == 'donor'

    def is_bloodbank(self):
        return self.role == 'bloodbank'

    def is_patient(self):
        return self.role == 'patient'

import random

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False) 

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return f"{self.email} - OTP"

