from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friend_list = models.ManyToManyField('self', blank=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.username
