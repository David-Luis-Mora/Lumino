# Generated by Django 5.1.2 on 2024-12-04 16:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('subjects', '0003_alter_subject_students'),
=======
        ('subjects', '0003_enrollment_alter_subject_students'),
>>>>>>> 13a8391a5136aba6601cb26f3883c18c2c3f3ecb
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]
