from django.db import models

from api.models.base_model import BaseModel
from api.models.comment import Comment


class Reply(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.comment.__str__()) + "의 답글: " + str(self.content[:10])

