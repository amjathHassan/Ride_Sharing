from datetime import datetime
import pytz
from rest_framework import status
from rest_framework.response import Response
from .models import Ride, User


def update_ride_location():
    try:
        ride_objs = Ride.objects.filter(status__in=['requested', 'started'])
        if ride_objs:
            for obj in ride_objs:
                obj.location_x = obj.driver.location_x
                obj.location_y = obj.driver.location_y
                obj.save()
    except Exception as e:
        print(e)
        return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)
