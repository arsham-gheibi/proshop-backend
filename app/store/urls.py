from django.urls import path
from store.views import Products, Show

urlpatterns = (
    path('', Products.as_view()),
    path('<str:pk>/', Show.as_view()),
)
