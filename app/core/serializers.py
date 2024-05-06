from rest_framework import serializers
from core import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            'name', 'image', 'price', 'brand', 'category',
            'description', 'rating', 'num_reviews', 'count_in_stock'
        )
