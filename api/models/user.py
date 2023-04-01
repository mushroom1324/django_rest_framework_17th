from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField('self', blank=True)  # ManyToManyField

    def __str__(self):
        return self.user.__str__()  # user로 들어가서 user의 str을 호출(username이 default)

