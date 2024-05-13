from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import UserSeializer, UserSerializerWithToken


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        data.update(serializer.items())
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetAllUsers(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSeializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSeializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create(
            first_name=data['name'],
            username=data['username'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
