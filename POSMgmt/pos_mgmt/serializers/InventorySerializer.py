from rest_framework import serializers
from ..models import *


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class ItemPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPurchase
        fields = "__all__"

    def create(self, validated_data):
        item_code = validated_data.get("item_code")
        quantity = validated_data.get("quantity")
        vendor = validated_data.get("vendor")

        try:
            # Checking if InventoryItem with the itemcode and the vendor already exists
            inventory_item = InventoryItem.objects.get(
                item_code=item_code, vendor=vendor
            )
            inventory_item.quantity += quantity
            inventory_item.save()
        except InventoryItem.DoesNotExist:
            # If it doesnt exists create a new InventoryItem instance
            inventory_item = InventoryItem.objects.create(**validated_data)

        return super().create(validated_data)


class ItemSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSales
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
