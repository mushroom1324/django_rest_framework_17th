from django.urls import path
from account import views
from account.views import UserListAPIView, RegisterAPIView, LoginAPIView

urlpatterns = [
    path('', views.UserListAPIView.as_view()),
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
]
