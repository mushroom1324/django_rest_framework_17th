from django.db import models
from rest_framework import serializers

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friend_list = models.ManyToManyField('self', blank=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image', 'friend_list')
