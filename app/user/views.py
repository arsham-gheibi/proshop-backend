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


class AbstractTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        data.update(serializer.items())
        return data


class AbstractTokenObtainPairView(TokenObtainPairView):
    serializer_class = AbstractTokenObtainPairSerializer


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

    def put(self, request):
        user = request.user
        data = request.data

        name = data.get('name', '')
        username = data.get('username', '')
        password = data.get('password', '')

        if name.strip():
            user.name = name
        if username.strip():
            user.username = username
        if password.strip():
            user.password = make_password(password)

        user.save()
        serializer = UserSerializerWithToken(user)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create(
            name=data['name'],
            username=data['username'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
