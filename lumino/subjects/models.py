from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolled'
    )
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='enrollments'
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True
    )

    def __str__(self):
        return f'{self.student.username} - {self.subject.name}'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['options'].queryset = Subject.objects.exclude(enrollments__student=user)

class Subject(models.Model):
    code = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='student_subjects', through=Enrollment, blank=True
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='teacher_subjects',
    )

    def __str__(self):
        return self.name

class Lesson(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.title
