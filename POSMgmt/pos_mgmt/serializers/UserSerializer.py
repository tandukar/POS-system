from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from ..models import *

class CustomUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "email",
            "username",
            "password",
            "password_confirmation",
            "is_active",
            "is_staff",
        )

    def validate(self, data):
        password = data.get("password")
        password_confirmation = data.pop("password_confirmation", None)

        if password or password_confirmation:
            if password != password_confirmation:
                raise serializers.ValidationError(
                    {"password_confirmation": "Passwords do not match"}
                )

        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation", None)
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CustomUserSerializer, self).create(validated_data)
    