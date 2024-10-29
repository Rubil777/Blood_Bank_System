from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Donor(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    contact_info = models.CharField(max_length=255)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.blood_type})"


class BloodInventory(models.Model):
    blood_type = models.CharField(max_length=3, choices=Donor.BLOOD_TYPES, unique=True)
    units_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.blood_type}: {self.units_available} units"


class BloodRequest(models.Model):
    REQUEST_STATUS = [
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
        ('Denied', 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=Donor.BLOOD_TYPES)
    units_requested = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.username} for {self.units_requested} units of {self.blood_type}"
