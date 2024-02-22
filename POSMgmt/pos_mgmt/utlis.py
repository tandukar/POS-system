from rest_framework import status
from rest_framework.response import Response
from .models import Store
from .serializers import StoreSerializer


def check_user_store(user_id):
    try:
        store = Store.objects.get(store_owner=user_id)
        return StoreSerializer(store).data.get("id")
    except Store.DoesNotExist:
        return None
