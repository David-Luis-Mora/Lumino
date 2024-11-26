# Create your models here.


from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=256)
    name = models.TextField(max_length=256)
    # teacher =
    # students =
