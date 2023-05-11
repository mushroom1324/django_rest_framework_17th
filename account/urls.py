from django.urls import path
from account import views
from account.views import UserListAPIView, RegisterAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.UserListAPIView.as_view()),
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),  # 토큰 재발급하기
    path('logout/', views.LogoutAPIView.as_view()),
]
