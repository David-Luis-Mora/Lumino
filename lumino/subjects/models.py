# Create your models here.


from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
    )

    students = models.ManyToManyField(User, related_name='users', blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_teacher',
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(
        blank=True,
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.title
