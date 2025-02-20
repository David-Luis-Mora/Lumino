# Generated by Django 5.1.4 on 2025-01-13 19:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0008_alter_enrollment_student'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_subjects', through='subjects.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
    ]
