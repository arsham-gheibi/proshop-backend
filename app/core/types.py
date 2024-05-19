from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from core.models import Product, Order, OrderItem, ShippingAddress


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'is_staff')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'image', 'price', 'brand', 'category',
            'description', 'rating', 'num_reviews', 'count_in_stock'
        )


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            'user', 'payment_method', 'tax_price',
            'shipping_price', 'total_price', 'is_paid'
        )


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ('product', 'order', 'name', 'qty', 'price')


class ShippingAddressType(DjangoObjectType):
    class Meta:
        model = ShippingAddress
        fields = (
            'order', 'country', 'city', 'address',
            'postal_code', 'shipping_price'
        )
