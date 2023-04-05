from django.db import models


class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    professor_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location_info = models.CharField(max_length=255)
    time = models.TextField(blank=True)

    is_cyber = models.BooleanField(default=False)

    def __str__(self):
        return self.subject_name


