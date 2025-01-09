from subjects.models import Subject


def user_subjects(request):
    if request.user.is_authenticated:
        subjects = Subject.objects.filter(enrollments__student=request.user)
        return {'subjects': subjects}
    return {}
