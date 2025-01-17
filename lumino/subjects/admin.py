from django.contrib import admin

from .models import Lesson, Subject

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name',
        'teacher',
    ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'title',
        'content',
    ]
