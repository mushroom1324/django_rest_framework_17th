from django.urls import path
from api import views

urlpatterns = [
    path('subjects/', views.SubjectListViewSet.as_view()),
    path('subjects/<int:pk>/', views.SubjectDetailViewSet.as_view()),
]

