from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from shared.decorators import role_required
from users.models import Profile

from .forms import EnrollmentForm, LessonForm, UnenrollForm
from .models import Enrollment, Lesson, Subject


@login_required
def subject_list(request):
    profile = request.user.profile
    if profile.role == Profile.Role.TEACHER:
        subjects = Subject.objects.filter(teacher=request.user)
        not_teacher = False
    else:
        subjects = Subject.objects.filter(students=request.user)
        not_teacher = True

    return render(
        request, 'subjects/subject_list.html', {'subjects': subjects, 'not_teacher': not_teacher}
    )


@login_required
@role_required('S')
def enroll_subjects(request):
    msj = 'Enroll'
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, user=request.user)
        if form.is_valid():
            selected_options = form.cleaned_data['options']
            for subject_id in selected_options:
                subject = Subject.objects.get(id=subject_id)
                Enrollment.objects.get_or_create(student=request.user, subject=subject)
            return redirect('subjects:subject-list')
    else:
        form = EnrollmentForm(user=request.user)

    return render(request, 'subjects/enroll_unenroll.html', {'form': form, 'msj': msj})


@login_required
@role_required('S')
def unenroll_subjects(request):
    msj = 'Unenroll'
    if request.method == 'POST':
        form = UnenrollForm(request.POST, user=request.user)
        if form.is_valid():
            selected_options = form.cleaned_data['options']
            for subject_id in selected_options:
                subject = Subject.objects.get(id=subject_id)
                Enrollment.objects.filter(student=request.user, subject=subject).delete()
            return redirect('subjects:subject-list')
    else:
        form = UnenrollForm(user=request.user)

    return render(request, 'subjects/enroll_unenroll.html', {'form': form, 'msj': msj})


@login_required
def subject_detail(request, code):
    subject = Subject.objects.get(code=code)
    enrollment = False
    grade = False
    lessons = subject.lessons.all()
    profile = request.user.profile
    user = request.user
    if profile.role == Profile.Role.TEACHER:
        if subject.teacher == user:
            is_teacher = True
        else:
            raise PermissionDenied()
    else:
        enrollment = subject.enrollments.filter(student=request.user).first()
        # enrolle = Enrollment.objects.filter(student=user, subject=subject)
        if enrollment != None:
            is_teacher = False
            grade = enrollment.mark
        else:
            raise PermissionDenied()

    return render(
        request,
        'subjects/subject_detail.html',
        {
            'subject': subject,
            'is_teacher': is_teacher,
            'lessons': lessons,
            'grade': grade,
        },
    )


@login_required
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


@login_required
def lesson_detail(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    subject = lesson.subject

    if request.user.profile.role == 'T':
        if subject.teacher != request.user:
            raise PermissionDenied()
        return render(request, 'subjects/lesson_detail.html', {'lesson': lesson, 'can_edit': True})
    elif request.user.profile.role == 'S':
        if request.user not in subject.students.all():
            raise PermissionDenied()
        return render(request, 'subjects/lesson_detail.html', {'lesson': lesson})
    else:
        raise PermissionDenied()


@login_required
@role_required('T')
def add_lesson(request, code):
    subject = Subject.objects.get(code=code)
    user = request.user
    if subject.teacher == user:
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                lesson = form.save(commit=False)
                if lesson.subject.teacher != request.user:
                    return HttpResponseForbidden('No tienes permisos.')
                lesson.save()
                return redirect('subjects:subject-detail', code=lesson.subject.code)

        else:
            form = LessonForm()
            form
        return render(request, 'subjects/lesson_form.html', {'form': form})
    else:
        raise PermissionDenied()


@login_required
@role_required('T')
def edit_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if lesson.subject.teacher != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('subjects:subject-detail', code=lesson.subject.code)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'subjects/lesson_form.html', {'form': form})


@login_required
@role_required('T')
def delete_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if lesson.subject.teacher != request.user:
        raise PermissionDenied()
    if request.method == 'POST':
        code = lesson.subject.code
        lesson.delete()
        return redirect('subjects:subject-detail', code=code)
    return render(request, 'subjects/confirm_delete.html', {'object': lesson})


@login_required
@role_required('T')
def mark_list(request):
    subject = Subject.objects.get(code='DSW', teacher=request.user)
    enrollments = subject.enrollments.all()
    return render(request, 'mark_list.html', {'enrollments': enrollments})


@login_required
@role_required('T')
def edit_marks(request):
    subjects = Subject.objects.filter(teacher=request.user)

    if not subjects.exists():
        raise PermissionDenied('No tienes asignaturas asignadas para editar calificaciones.')

    enrollments = Enrollment.objects.filter(subject__in=subjects)

    EnrollmentFormSet = Enrollment.object.get(
        fields=('mark',),
        extra=0,
        can_delete=False,
    )

    if request.method == 'POST':
        formset = EnrollmentFormSet(request.POST, queryset=enrollments)
        if formset.is_valid():
            formset.save()
            return redirect('mark_list')
    else:
        formset = EnrollmentFormSet(queryset=enrollments)

    return render(request, 'edit_marks.html', {'subjects': subjects, 'formset': formset})
