from django.urls import path
from subject import views

urlpatterns = [
    path('', views.SubjectList.as_view()),
]
