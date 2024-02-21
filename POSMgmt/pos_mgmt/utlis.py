from rest_framework import status
from rest_framework.response import Response
from .models import Store
from .serializers import StoreSerializer


def check_user_store(user_id):
    try:
        store = Store.objects.filter(store_owner=user_id)
        serialier = StoreSerializer(store, many=True)
        return serialier.data
    except Store.DoesNotExist:
        return None
