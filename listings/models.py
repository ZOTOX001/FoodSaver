from django.db import models
from django.conf import settings
from django.utils import timezone

class Listing(models.Model):
    FOOD_TYPES = (
        ('cooked', 'Cooked Meal'),
        ('raw', 'Raw Ingredients'),
        ('packaged', 'Packaged Food'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('claimed', 'Claimed'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    )

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES)
    quantity_kg = models.FloatField()
    description = models.TextField()
    expiry_time = models.DateTimeField()
    pickup_instructions = models.TextField(blank=True)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.expiry_time

    def __str__(self):
        return f"{self.food_type} - {self.quantity_kg}kg by {self.donor.username}"

class Claim(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed (Picked Up)'),
    )

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claims')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    claimed_at = models.DateTimeField(auto_now_add=True)
    
    # Verification
    claimant_photo = models.ImageField(upload_to='claims/', blank=True, null=True, help_text="Photo taken by claimant at pickup")
    donor_photo = models.ImageField(upload_to='claims/', blank=True, null=True, help_text="Photo taken by donor at handover")

    def __str__(self):
        return f"Claim for {self.listing} by {self.claimant.username}"
