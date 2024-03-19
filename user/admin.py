from django.contrib import admin

from .models import User, UserList

# Register your models here.
admin.site.register(User, UserList)