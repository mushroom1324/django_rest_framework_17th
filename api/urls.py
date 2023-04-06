from django.urls import path
from api import views

urlpatterns = [
    path('subjects/', views.subject_list),
    path('subjects/<int:pk>/', views.subject_detail),
]

