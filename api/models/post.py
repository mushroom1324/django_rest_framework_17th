from django.db import models

from .base_model import BaseModel
from .category import Category
from .subject import Subject
from .user import User


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

