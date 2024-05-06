import uuid
from django.db import models
from django.conf import settings


class Product(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    # image =
    price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    num_reviews = models.IntegerField(default=0)
    count_in_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - ${self.price}'


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
    paid_at = models.DateTimeField(auto_now_add=False)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False)
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
