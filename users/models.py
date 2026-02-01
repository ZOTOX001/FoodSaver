from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('claimant', 'Claimant'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='claimant')
    is_verified = models.BooleanField(default=False)
    
    # Location
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    # Verification details
    restaurant_license = models.CharField(max_length=50, blank=True, help_text="For Donors")
    ngo_registration = models.CharField(max_length=50, blank=True, help_text="For Claimants")
    
    # Institutional details
    institution_name = models.CharField(max_length=100, blank=True)

    # Trust Score
    trust_score = models.FloatField(default=5.0)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
