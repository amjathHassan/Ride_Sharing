# Create your models here.
from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location_x = models.TextField(blank=True)
    location_y = models.TextField(blank=True)

    def __str__(self):
        return f"Ride #{self.id} - {self.status}"


class RideList(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'pickup_location', 'dropoff_location', 'status', 'created_at', 'updated_at')