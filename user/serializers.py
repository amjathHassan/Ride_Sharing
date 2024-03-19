from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        extra_kwargs = {
            'password': {'write_only': True},
        }
        fields = '__all__'

    def create(self, validated_data):
        user = get_user_model().objects.create(username=validated_data.get('username'),
                                               first_name=validated_data.get('first_name'),
                                               last_name=validated_data.get('last_name'),
                                               password=make_password(validated_data.get('password')),
                                               email=validated_data.get('email'),
                                               street=validated_data.get('street'),
                                               country=validated_data.get('country'),
                                               phone=validated_data.get('phone'),
                                               role=validated_data.get('role'),
                                               )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('last_name',)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'phone')


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class CustomerDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = "__all__"

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"