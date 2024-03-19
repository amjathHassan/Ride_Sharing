from django.contrib import admin
from django.urls import path
from . import views

app_name = 'ride'

urlpatterns = [
    path('request', views.CreateRideApi.as_view(), name='create request'),
    path('ride-details/<int:pk>', views.ViewRideDetailApi.as_view(), name='ride details'),
    path('ride-list', views.ViewRideListApi.as_view(), name='list rides'),
    path('ride-update/<int:pk>', views.RideUpdateApi.as_view(), name='update ride'),
]
