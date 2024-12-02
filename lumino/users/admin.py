from django.contrib import admin

from .models import Enrollment, Profile

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
class Enrollment(admin.ModelAdmin):
    list_display = [
        'student',
        'subject',
        'enrolled_at',
        'mark',
    ]
