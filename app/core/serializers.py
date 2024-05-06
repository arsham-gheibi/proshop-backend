from rest_framework import serializers
from core import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            'name', 'price', 'brand', 'category', 'description',
            'rating', 'num_reviews', 'count_in_stock'
        )
