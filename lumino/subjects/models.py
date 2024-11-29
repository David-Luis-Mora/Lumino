# Create your models here.
# user.profile.get_role_display

from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    code = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
    )
    students = models.ManyToManyField(User, related_name='student_subjects', null=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_subjects',
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.title
