from django.urls import path
from post import views

urlpatterns = [
    path('', views.PostList.as_view()),
]
