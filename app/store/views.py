from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Product
from core.serializers import ProductSerializer


class Home(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
