from django.urls import path
from store.views import Home

urlpatterns = (
    path('', Home.as_view()),
)
