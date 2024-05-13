from django.urls import path
from user.views import (
    GetAllUsers, Profile, MyTokenObtainPairView, RegisterUser)


urlpatterns = [
    path(
        '',
        GetAllUsers.as_view(),
        name='users'
    ),
    path(
        'profile/',
        Profile.as_view(),
        name='users-profile'
    ),
    path(
        'login/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'register/',
        RegisterUser.as_view(),
        name='users-register'
    )
]
