from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterApi.as_view(), name='user register'),
    path('login', views.LoginApi.as_view(), name='user login'),
    path('updateprofile/<int:pk>', views.UpdateProfileApi.as_view(), name='update user'),
    path('user_list', views.UserListView.as_view(), name='user list'),
    path('delete/<int:pk>', views.UserDeleteAPI.as_view(), name='delete user'),

    path('available-drivers', views.DriverAvailableListView.as_view(), name='available drivers'),
    path('update-driver-location/<int:pk>', views.DriverLocationUpdate.as_view(), name='update location'),
    path('update-driver-availability/<int:pk>', views.DriverAvailabilityUpdate.as_view(), name='update availability'),

]
