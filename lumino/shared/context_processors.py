from subjects.models import Subject

def user_subjects(request):
    if request.user.is_authenticated:
        subjects = Subject.objects.filter(teacher=request.user)
        return {'subjects': subjects}
    return {}
