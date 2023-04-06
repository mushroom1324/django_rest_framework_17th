from django.urls import path
from subject import views

urlpatterns = [
    path('subjects/', views.subject_list),
]
