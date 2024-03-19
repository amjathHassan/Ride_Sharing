from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, default='None', blank=True)
    email = models.EmailField(blank=False, max_length=255, unique=True)
    first_name = models.CharField(blank=False, max_length=150, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    street = models.TextField(blank=False)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)
    country = models.TextField(blank=True)
    phone = models.TextField(blank=False)
    role = models.CharField(max_length=20,choices=[('Rider', 'Rider'),
                            ('Driver', 'Driver'), ('Admin', 'Admin')],
                            default='Rider')
    availability = models.CharField(max_length=20, choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
                                                             default='available')
    location_x = models.TextField(blank=True)
    location_y = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email


class UserList(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'street', 'phone', 'role')
