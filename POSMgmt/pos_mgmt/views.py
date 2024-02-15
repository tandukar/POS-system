import json
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, InventoryItem, ItemPurchase, Organization
from .serializers import (
    CustomUserSerializer,
    LoginSerializer,
    InventoryItemSerializer,
    ItemPurchaseSerializer,
)
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterUserView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]

            # Set cookies for access and refresh tokens
            response = Response(
                {
                    "success": True,
                    "message": "User Logged in successfully",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)

            return response

        except Exception as e:
            return Response(
                {"success": False, "error": "An error occurred during login."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ItemPurchaseView(APIView):
    def post(self, request):
        try:
            serialized_data = ItemPurchaseSerializer(data=request.data)
            if not serialized_data.is_valid():
                return Response(
                    {"success": False, "error": serialized_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serialized_data.save()
            return Response(
                {
                    "success": True,
                    "message": "Item Purchased successfully",
                    "data": serialized_data.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
