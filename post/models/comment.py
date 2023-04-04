from django.db import models

from post.models.post import Post
from api.models.base_model import BaseModel


class Comment(BaseModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.TextField(blank=False)

    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.post.__str__()) + "의 댓글: " + str(self.content[:10])



