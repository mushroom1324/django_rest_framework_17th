from django.urls import path
from account import views

urlpatterns = [
    path('users/', views.user_list),
]
