from django.db import models

from account.models.user import User
from subject.models.subject import Subject


class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.__str__() + " -> " + self.subject.__str__()


