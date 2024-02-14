from django.db import models
from django.utils import timezone
# Create your models here.


class InventoryItem(models.Model):
    item_code = models.CharField(max_length=10, unique=True)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)  
    quantity_unit = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    price_unit = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.item_name


class ItemPurchase(models.Model):
    item_code = models.CharField(max_length=10)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    quantity_unit = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField(default=0.00)
    price_unit = models.CharField(max_length=50, null=True, blank=True) 
    vendor = models.CharField(max_length=255, null=True, blank=True)
    purchased_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.item_name
    

