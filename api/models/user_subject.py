from django.db import models

from api.models import UserProfile
from api.models.subject import Subject


class UserSubject(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
