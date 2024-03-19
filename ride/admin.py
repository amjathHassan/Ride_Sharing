from django.contrib import admin
from .models import Ride, RideList

# Register your models here.
admin.site.register(Ride, RideList)