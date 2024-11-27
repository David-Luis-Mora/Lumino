from django.contrib.auth.models import User
from django.db import models
from subjects.models import Subject

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.username} - {self.subject.name}'
