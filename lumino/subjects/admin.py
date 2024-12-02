from django.contrib import admin

from .models import Lesson, Subject

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name',
        'description',
        # 'get_students',
        'teacher',
    ]

    # def get_students(self, obj):
    #     return ', '.join([str(student) for student in obj.students.all()])


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'title',
        'content',
    ]
