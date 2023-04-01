from django.db import models

from api.models.subject import Subject


class SubjectReview(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "리뷰: " + str(self.subject)


