# Generated by Django 5.1.2 on 2024-12-07 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0001_initial'),
        ('subjects', '0005_alter_subject_students'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]
