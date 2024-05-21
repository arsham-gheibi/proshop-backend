"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)


def image_file_path(instance, filename):
    """
    Generate file path for new product image
    ."""

    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'product', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not username:
            raise ValueError('User must have an username address.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Create and return a new superuser."""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_file_path)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.PositiveIntegerField()
    num_reviews = models.IntegerField(default=0)
    count_in_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - ${self.price}'

    def save(self, *args, **kwargs):
        if self.rating not in (1, 2, 3, 4, 5):
            raise ValueError('Rating Should be between 1-5')

        return super(Product, self).save(*args, **kwargs)


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    payment_method = models.CharField(max_length=255)
    tax_price = models.DecimalField(max_digits=7, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order = models.OneToOneField(
        'Order', on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.address)
