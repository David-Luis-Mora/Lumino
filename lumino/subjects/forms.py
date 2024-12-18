from django import forms

from .models import Enrollment, Lesson, Subject


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'title', 'content']


class EnrollmentForm(forms.Form):
    options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=True, label='Enroll to the desiered subjects:'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        enrolled_subject_ids = Enrollment.objects.filter(student=user).values_list(
            'subject__id', flat=True
        )
        available_subjects = Subject.objects.exclude(id__in=enrolled_subject_ids)

        self.fields['options'].choices = [
            (subject.id, f'{subject.code} - {subject.name}') for subject in available_subjects
        ]


class UnenrollForm(forms.Form):
    options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Unenroll from the desiered subjects:',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        enrolled_subject_ids = Enrollment.objects.filter(student=user).values_list(
            'subject__id', flat=True
        )
        available_subjects = Subject.objects.filter(id__in=enrolled_subject_ids)

        self.fields['options'].choices = [
            (subject.id, f'{subject.code} - {subject.name}') for subject in available_subjects
        ]
