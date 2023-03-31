from django.db import models


class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    professor_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location_info = models.CharField(max_length=255)
    is_cyber = models.BooleanField()
    time = models.TextField()