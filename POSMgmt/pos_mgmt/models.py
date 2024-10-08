from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class InventoryItem(models.Model):
    item_code = models.CharField(max_length=10, unique=True)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    min_margin = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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
    cost_price = models.FloatField(default=0.00)
    price_unit = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.CharField(max_length=255, null=True, blank=True)
    purchased_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name


class Organization(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    org_email = models.EmailField()
    org_contact = models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ItemSales(models.Model):
    item_code = models.CharField(max_length=10)
    item_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity_unit = models.CharField(max_length=50, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sold_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item_name


class Store(models.Model):
    store_name = models.CharField(max_length=255)
    store_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_contact = models.CharField(max_length=30)
    store_email = models.EmailField(blank=True)
    address = models.CharField(max_length=255)
    logo = models.TextField()
    established_date = models.DateField()

    def __str__(self):
        return self.store_name


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_contact = models.IntegerField()
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name + self.customer_contact


class Transaction(models.Model):
    item_sales = models.ManyToManyField(ItemSales)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
