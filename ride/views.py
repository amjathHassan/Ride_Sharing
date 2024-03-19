from django.shortcuts import render

# Create your views here.
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Ride, User
from .serializers import (RideSerializer, RideDetailsSerializer, ViewRideListApiSerializer, UpdateRideSerializer)

# Create your views here.


class CreateRideApi(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            serializer = RideSerializer(data=request.data)
            user_id = request.data.get('id')
            if serializer.is_valid():
                ride = serializer.save()
                return Response({
                    "user": RideSerializer(ride).data,
                    "message": "Ride Requested Successfully",
                    "success": True
                })
            else:
                return Response({
                    "message": "Ride Request Failed",
                    "success": False,
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class ViewRideDetailApi(generics.GenericAPIView):
    serializer_class = RideDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            print("========", request.user.id)
            ride_object = Ride.objects.get(id=kwargs.get('pk'))
            if ride_object.rider != request.user and ride_object.driver != request.user:
                return Response({'message': 'Invalid User', 'success': False}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer_class = RideDetailsSerializer(ride_object, context={'request': request})
            return Response({"success": True,
                             "message": f"Details of Ride {ride_object.id}",
                             "data": serializer_class.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)




class ViewRideListApi(generics.ListAPIView):
    serializer_class = ViewRideListApiSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.role == "Admin":
            ride_list_obj = Ride.objects.all().order_by('-id')
            serializer = ViewRideListApiSerializer(ride_list_obj, many=True, context={'request': request})

            return Response(
                {"success": True, "message": "List of Rides", "data": serializer.data},
                status=status.HTTP_200_OK)
        elif request.user.role == "Driver":
            ride_list_obj = Ride.objects.filter(driver=request.user.id).order_by('-id')
            serializer = ViewRideListApiSerializer(ride_list_obj, many=True, context={'request': request})

            return Response(
                {"success": True, "message": "List of Rides", "data": serializer.data},
                status=status.HTTP_200_OK)
        elif request.user.role == "Rider":
            ride_list_obj = Ride.objects.filter(rider=request.user.id).order_by('-id')
            serializer = ViewRideListApiSerializer(ride_list_obj, many=True, context={'request': request})

            return Response(
                {"success": True, "message": "List of Rides", "data": serializer.data},
                status=status.HTTP_200_OK)


class RideUpdateApi(generics.GenericAPIView):
    serializer_class = UpdateRideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        try:
            ride_obj = Ride.objects.get(id=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid Ride ID', "success": False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if ride_obj.rider == request.user or ride_obj.driver == request.user or request.user.role == "Admin":
                if request.user.role == "Rider":
                    if request.data.get('status') in ['accepted', 'completed']:
                        return Response({"message": "Rider Not Allowed To Accept and Complete Ride", "success": False},
                                        status=status.HTTP_403_FORBIDDEN)
                    if ride_obj.status == 'requested':
                        driver_obj = User.objects.get(id=request.data.get('driver'))
                        ride_obj.driver = driver_obj
                        ride_obj.location_x = driver_obj.location_x
                        ride_obj.location_y = driver_obj.location_y
                    ride_obj.dropoff_location = request.data.get('dropoff_location')
                    ride_obj.status = request.data.get('status')
                else:
                    if request.data.get('status') != 'cancelled':
                        ride_obj.location_x = ride_obj.driver.location_x
                        ride_obj.location_y = ride_obj.driver.location_y
                    if request.data.get('status') == 'accepted':
                        driver_obj = User.objects.get(id=request.user.id)
                        driver_obj.availability = 'unavailable'
                        driver_obj.save()
                    ride_obj.status = request.data.get('status')
                ride_obj.save()
                serializer = UpdateRideSerializer(ride_obj, context={'request': request})
                if serializer:
                    return Response(
                        {'message': 'Ride Updated Successfully', 'success': True, 'data': serializer.data},
                        status=status.HTTP_200_OK)
                return Response({"message": "Updating Ride Failed", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "No permission For Updating Ride", "success": False},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)