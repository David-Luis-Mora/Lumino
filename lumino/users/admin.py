from django.contrib import admin

from subjects.models import Enrollment

from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'role',
        'user',
        'bio',
        'avatar',
    ]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'subject',
        'enrolled_at',
        'mark',
    ]
