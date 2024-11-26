# Create your models here.


from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    teacher = models.ForeignKey('User', related_name='users', on_delete=models.CASCADE)
    students = models.ForeignKey('User', related_name='users', on_delete=models.CASCADE)
