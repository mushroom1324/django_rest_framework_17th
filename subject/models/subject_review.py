from django.db import models

from api.models.base_model import BaseModel
from subject.models.subject import Subject


class SubjectReview(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    rate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "리뷰: " + str(self.subject)
