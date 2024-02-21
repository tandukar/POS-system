from rest_framework import status
from rest_framework.response import Response
from .models import Store


def check_user_store(user_id):
    try:
        store = Store.objects.get(store_owner=user_id)
        if store:
            return Response(
                {"message": "You are not authorized to access this store"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Store.DoesNotExist:
        return Response(
            {"message": "Store not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
