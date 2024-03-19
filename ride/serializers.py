from rest_framework import serializers
from .models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


class RideDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = '__all__'


class ViewRideListApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = "__all__"


class UpdateRideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = "__all__"
