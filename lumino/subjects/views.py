from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from users.models import Profile

from .forms import EnrollmentForm, LessonForm, UnenrollForm
from .models import Enrollment, Lesson, Subject


@login_required
def subject_list(request):
    profile = request.user.profile

    if profile.role == Profile.Role.TEACHER:
        subjects = Subject.objects.filter(teacher=request.user)
        not_teacher = False
        show_certificate_link = False
    else:
        subjects = Subject.objects.filter(students=request.user)
        not_teacher = True
        enrollments = Enrollment.objects.filter(student=request.user, subject__in=subjects)
        show_certificate_link = all(enrollment.mark is not None for enrollment in enrollments)

    return render(
        request,
        'subjects/subject_list.html',
        {
            'subjects': subjects,
            'not_teacher': not_teacher,
            'show_certificate_link': show_certificate_link,
        },
    )


# @role_required('S')
@login_required
def enroll_subjects(request):
    msj = 'Enroll'
    msj2 = 'Successfully enrolled in the chosen subjects.'
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, user=request.user)
        if form.is_valid():
            selected_options = form.cleaned_data['options']
            for subject_id in selected_options:
                subject = Subject.objects.get(id=subject_id)
                Enrollment.objects.get_or_create(student=request.user, subject=subject)
            messages.success(request, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subject-list')
        # else:

        # messages.success(request, 'Successfully enrolled in the chosen subjects.')
        # return redirect('subjects:subject-list')

    else:
        form = EnrollmentForm(user=request.user)

    return render(
        request, 'subjects/enroll_unenroll.html', {'form': form, 'msj': msj, 'msj2': msj2}
    )


# @role_required('S')
@login_required
def unenroll_subjects(request):
    msj = 'Unenroll'
    if request.method == 'POST':
        form = UnenrollForm(request.POST, user=request.user)
        if form.is_valid():
            selected_options = form.cleaned_data['options']
            for subject_id in selected_options:
                subject = Subject.objects.get(id=subject_id)
                Enrollment.objects.filter(student=request.user, subject=subject).delete()
            messages.success(request, 'Successfully unenrolled from the chosen subjects.')
            return redirect('subjects:subject-list')
        else:
            messages.error(request, 'There was an error with your request.')
            messages.success(request, 'Successfully unenrolled from the chosen subjects.')
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
def lesson_detail(request, code, pk):
    lesson = Lesson.objects.get(pk=pk, subject__code=code)
    subject = lesson.subject
    if request.user.profile.role == 'T':
        if subject.teacher != request.user:
            raise PermissionDenied()
        return render(request, 'subjects/lesson_detail.html', {'lesson': lesson, 'can_edit': True})
    elif request.user.profile.role == 'S':
        if request.user not in subject.students.all():
            raise PermissionDenied()
        return render(
            request, 'subjects/lesson_detail.html', {'lesson': lesson, 'subject': lesson.subject}
        )
    else:
        raise PermissionDenied()


# @role_required('T')
@login_required
def add_lesson(request, code):
    subject = Subject.objects.get(code=code)
    user = request.user
    msj = 'Lesson was successfully added.'
    if subject.teacher == user:
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.subject = subject
                if lesson.subject.teacher != request.user:
                    return PermissionDenied('No tienes permisos.')
                lesson.save()
                messages.success(request, 'Lesson was successfully added.')
                return redirect('subjects:subject-detail', code=lesson.subject.code)

        else:
            form = LessonForm()
            print('Error del test-----------------------------------------')
        return render(
            request, 'subjects/lesson_form.html', {'form': form, 'subject': subject, 'msj': msj}
        )
    else:
        raise PermissionDenied("You don't have permission to edit this lesson.")


# @role_required('T')
@login_required
def edit_lesson(request, code, pk):
    subject = Subject.objects.get(code=code)
    lesson = Lesson.objects.get(pk=pk, subject=subject)

    if request.user != subject.teacher:
        raise PermissionDenied("You don't have permission to edit this lesson.")

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes were successfully saved.')
            return redirect('subjects:subject-detail', code=subject.code)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'subjects/lesson_form.html', {'form': form, 'subject': subject})


# @role_required('T')
@login_required
def delete_lesson(request, code, pk):
    lesson = Lesson.objects.get(pk=pk, subject__code=code)
    if lesson.subject.teacher != request.user:
        raise PermissionDenied()
    if request.method == 'POST':
        code = lesson.subject.code
        lesson.delete()
        messages.success(request, 'Lesson was successfully deleted.')
        return redirect('subjects:subject-detail', code=code)
    return render(request, 'subjects/confirm_delete.html', {'object': lesson})


# @role_required('T')
@login_required
def mark_list(request, code):
    subject = Subject.objects.get(code=code)
    if subject.teacher != request.user:
        return HttpResponseForbidden('No tienes permisos para acceder a esta página.')
    enrollments = subject.enrollments.all()
    return render(
        request, 'subjects/mark_list.html', {'enrollments': enrollments, 'subject': subject}
    )


# @role_required('T')
@login_required
def edit_marks(request, code):
    subject = Subject.objects.get(code=code)
    if subject.teacher != request.user:
        return HttpResponseForbidden('No tienes permisos para acceder a esta página.')
    # raise PermissionDenied('No tienes permiso para editar calificaciones en este módulo.')
    enrollments = Enrollment.objects.filter(subject=subject)

    EnrollmentFormSet = modelformset_factory(
        Enrollment, fields=('mark',), extra=0, can_delete=False
    )

    if request.method == 'POST':
        formset = EnrollmentFormSet(request.POST, queryset=enrollments)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Marks were successfully saved.')
            return redirect('subjects:mark-list', code=subject.code)
        # else:
        #     for form in formset:
        #         print(form.errors)
    else:
        formset = EnrollmentFormSet(queryset=enrollments)

    return render(request, 'subjects/edit_marks.html', {'formset': formset, 'subject': subject})


def request_certificate(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    if not all(enrollment.mark is not None for enrollment in enrollments):
        return HttpResponseForbidden(
            'No puedes solicitar el certificado. No todas tus asignaturas tienen calificación.'
        )

    return JsonResponse({'message': 'Solicitud de certificado enviada correctamente.'})
