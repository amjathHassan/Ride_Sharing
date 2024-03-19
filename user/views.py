from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (RegisterSerializer, UserSerializer, LoginSerializer, UpdateProfileSerializer,
                          CustomerDetailsSerializer)

# Create your views here.


class RegisterApi(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        try:
            serializer = RegisterSerializer(data=request.data)
            email = request.data.get('email')
            phone = request.data.get('phone')
            if get_user_model().objects.filter(email=email).exists():
                return Response({
                    "message": "User with this Email already exist",
                    "success": False
                }, status=status.HTTP_400_BAD_REQUEST)

            if get_user_model().objects.filter(phone=phone).exists():
                return Response({
                    "message": "User with this Phone number already exist",
                    "success": False
                }, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "message": "User Created Successfully",
                    "success": True
                })
            else:
                return Response({
                    "message": "Registration Failed",
                    "success": False,
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            user = None
            serializer = LoginSerializer(data=request.data)
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')

            if email and phone:
                try:
                    user = get_user_model().objects.get(email=email)
                except ObjectDoesNotExist:
                    return Response({'message': "Invalid Email", "success": False}, status=status.HTTP_400_BAD_REQUEST)
                if not user.phone == phone:
                    return Response({'message': "Mobile No: doesn't match with email", "success": False},
                                    status=status.HTTP_400_BAD_REQUEST)
            if email:
                try:
                    user = get_user_model().objects.get(email=email)
                except ObjectDoesNotExist:
                    return Response({'message': "Invalid Email", "success": False}, status=status.HTTP_400_BAD_REQUEST)
            if phone:
                try:
                    user = get_user_model().objects.get(phone=phone)
                except ObjectDoesNotExist:
                    return Response({'message': "Invalid Mobile No", "success": False},
                                    status=status.HTTP_400_BAD_REQUEST)
            if user:
                    user_details = {}
                    user_details.update(
                        {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name,
                         'street': user.street, 'city': user.city, 'state': user.state,
                         'country': user.country, 'phone': user.phone})

                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    access_token.set_exp(lifetime=timedelta(days=1000))
                    print("hi-------")
                    if user.check_password(password):
                        return Response({'role': user.role, 'message': 'Login Success', "success": True,
                                         'refresh': str(refresh),
                                         'access': str(access_token), 'user_details': user_details})
                    else:
                        return Response({'message': 'Wrong Password', "success": False},
                                        status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "Invalid Email or Mobile No:", "success": False, "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileApi(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        try:
            user_obj = get_user_model().objects.get(id=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid User ID', "success": False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if request.user.id == kwargs.get('pk'):
                user_obj.username = request.data.get('username')
                user_obj.first_name = request.data.get('first_name')
                user_obj.last_name = request.data.get('last_name')
                user_obj.street = request.data.get('street')
                user_obj.city = request.data.get('city')
                user_obj.state = request.data.get('state')
                user_obj.country = request.data.get('country')
                user_obj.phone = request.data.get('phone')
                user_obj.save()
                serializer = UpdateProfileSerializer(user_obj, context={'request': request})
                if serializer:
                    return Response(
                        {'message': 'Profile Updated Successfully', 'success': True, 'data': serializer.data},
                        status=status.HTTP_200_OK)
                return Response({"message": "Updating Profile Failed", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = CustomerDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.role == "Admin":
            customer_list_obj = get_user_model().objects.all().order_by('-id')
            serializer = CustomerDetailsSerializer(customer_list_obj, many=True, context={'request': request})

            return Response(
                {"success": True, "message": "List of Customers", "data": serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"success": False, "message": "You Dont Have Permission To List Users"},
                status=status.HTTP_403_FORBIDDEN)


class UserDeleteAPI(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        try:
            customer_delete_obj = get_user_model().objects.get(id=kwargs.get('pk'))
            if request.user.id == customer_delete_obj.id or request.user.role == "Admin":
                customer_delete_obj.delete()
                return Response({"message": "Customer deleted", "success": True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "You don't have permission for this user.", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class DriverAvailableListView(generics.ListAPIView):
    serializer_class = CustomerDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        customer_list_obj = get_user_model().objects.filter(role='Driver', availability='available').order_by('-id')
        serializer = CustomerDetailsSerializer(customer_list_obj, many=True, context={'request': request})

        return Response(
            {"success": True, "message": "List of Customers", "data": serializer.data},
            status=status.HTTP_200_OK)


class DriverLocationUpdate(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        try:
            user_obj = get_user_model().objects.get(id=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid User ID', "success": False}, status=status.HTTP_400_BAD_REQUEST)
        try:

            if request.user.id == kwargs.get('pk') or request.user.role == "Admin":
                user_obj.location_x = request.data.get('location_x')
                user_obj.location_y = request.data.get('location_y')
                user_obj.save()
                serializer = UpdateProfileSerializer(user_obj, context={'request': request})
                if serializer:
                    return Response(
                        {'message': 'Profile Updated Successfully', 'success': True, 'data': serializer.data},
                        status=status.HTTP_200_OK)
            else:
                return Response({"message": "You are not allowed to update", "success": False},
                                status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class DriverAvailabilityUpdate(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        try:
            user_obj = get_user_model().objects.get(id=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid User ID', "success": False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if request.user.id == kwargs.get('pk') or request.user.role == "Admin":
                user_obj.availability = request.data.get('availability')
                user_obj.save()
                serializer = UpdateProfileSerializer(user_obj, context={'request': request})
                if serializer:
                    return Response(
                        {'message': 'Profile Updated Successfully', 'success': True, 'data': serializer.data},
                        status=status.HTTP_200_OK)
            else:
                return Response({"message": "You are not allowed to update", "success": False},
                                status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)

