import json
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    UserProfile,
    InventoryItem,
    ItemPurchase,
    Organization,
    ItemSales,
    Transaction,
    Customer,
)
from .serializers import (
    CustomUserSerializer,
    LoginSerializer,
    InventoryItemSerializer,
    ItemPurchaseSerializer,
    ItemSalesSerializer,
    StoreSerializer,
    CustomerSerializer,
)
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .decorators import user_login_required


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
                {"success": False, "error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ItemPurchaseView(APIView):
    def get(self, request):
        try:
            serialized_data = ItemPurchaseSerializer(
                ItemPurchase.objects.all(), many=True
            )
            return Response(
                {
                    "success": True,
                    "message": "Expenses retrieved successfully",
                    "data": serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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


class ItemPurchaseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ItemPurchase.objects.all()
    serializer_class = ItemPurchaseSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "success": True,
                "message": "Purhcased item retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Purhcased item  Updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            data = {"success": False, "message": str(e)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            data = {"success": True, "message": "Purhcased item  deleted successfully"}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {"success": False, "message": str(e)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemSalesView(APIView):
    @user_login_required
    def get(self, request):
        try:
            serialized_data = ItemSalesSerializer(ItemSales.objects.all(), many=True)
            return Response(
                {
                    "success": True,
                    "message": "Sales retrieved successfully",
                    "data": serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @user_login_required
    def post(self, request):
        try:
            item_sales = []
            for item_data in request.data["items"]:
                serialized_data = ItemSalesSerializer(data=item_data)
                if serialized_data.is_valid():
                    item_sale = serialized_data.save()
                    print(item_sale.id)
                    item_sales.append(item_sale.id)
                else:
                    return Response(serialized_data.errors)

            transaction = Transaction.objects.create(
                customer_id=request.data["customer_contact"]
            )
            transaction.item_sales.set(item_sales)

            transaction.save()
            return Response(item_sales)

        except Exception as e:
            return Response(
                {"success": False, "error": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StoreView(APIView):
    @user_login_required
    def post(self, request, userid, *args, **kwargs):
        try:
            serialized_data = StoreSerializer(data=request.data)
            if not serialized_data.is_valid():
                return Response(
                    {"success": False, "error": serialized_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serialized_data.save()
            return Response(
                {
                    "success": True,
                    "message": "Store registered successfully",
                    "data": serialized_data.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomerView(APIView):
    @user_login_required
    def post(self, request, user_id, *args, **kwargs):
        try:
            serialized_data = CustomerSerializer(data=request.data)
            if not serialized_data.is_valid():
                return Response(
                    {"success": False, "error": serialized_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serialized_data.save()
            return Response(
                {
                    "success": True,
                    "message": "Customer registered successfully",
                    "data": serialized_data.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @user_login_required
    def get(self, request, user_id, *args, **kwargs):
        try:
            serialized_data = CustomerSerializer(
                Customer.objects.filter(store_id=1), many=True
            )
            return Response(
                {
                    "success": True,
                    "message": "Customers retrieved successfully",
                    "data": serialized_data.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
