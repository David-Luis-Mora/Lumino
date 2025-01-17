from django.conf import settings
from django.db import models

# Create your models here.
class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    role = models.CharField(max_length=1, choices=Role, default=Role.STUDENT)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars',
        blank=True,
        null=True,
        default='avatars/noavatar.png',
    )

    def __str__(self):
        return self.user.username
