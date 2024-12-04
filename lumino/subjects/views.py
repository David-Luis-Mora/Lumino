from django.contrib.auth.decorators import login_required

# from django.http import HttpResponseForbidden
from django.shortcuts import render

from users.models import Profile

from .models import Lesson, Subject


@login_required
def subject_list(request):
    profile = request.user.profile
    if profile.role == Profile.Role.TEACHER:
        subjects = Subject.objects.filter(teacher=request.user)
    else:
        subjects = Subject.objects.filter(students=request.user)

    return render(request, 'subjects/subject_list.html', {'subjects': subjects})


def subject_detail(request, code):
    subject = Subject.objects.get(code=code)
    print(request.user)
    profile = request.user.profile

    if profile.role == Profile.Role.TEACHER:
        return render(request, 'subjects/subject_dashboard_teacher.html', {'subject': subject})
    else:
        return render(request, 'subjects/subject_dashboard_student.html', {'subject': subject})


def subject_lessons(request, code):
    subject = Subject.objects.get(code=code)
    lessons = Lesson.objects.filter(subject=subject)
    profile = request.user.profile

    if profile.role == Profile.Role.TEACHER:
        return render(
            request, 'subjects/lessons_teacher.html', {'subject': subject, 'lessons': lessons}
        )
    else:
        return render(
            request, 'subjects/lessons_student.html', {'subject': subject, 'lessons': lessons}
        )


def lesson_detail(request):
    pass


def add_lesson(request):
    pass


def edit_lesson(request):
    pass


def delete_lesson(request):
    pass


def mark_list(request):
    pass


def edit_marks(request):
    pass
