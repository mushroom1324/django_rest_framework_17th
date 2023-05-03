from django.urls import path
from api import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    path('subjects/', views.SubjectListViewSet.as_view()),
    path('subjects/<int:pk>/', views.SubjectDetailViewSet.as_view()),
    path('login/', obtain_jwt_token),
    path('login/verify/', verify_jwt_token),
    path('login/refresh/', refresh_jwt_token),
]

