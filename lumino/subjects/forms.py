from django import forms

from .models import Lesson, Subject


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'title', 'content']


class EnrollmentForm(forms.Form):
    OPCIONES = [
        (
            asignatura.id,
            asignatura.code,
        )
        for asignatura in Subject.objects.all()
    ]

    opciones = forms.MultipleChoiceField(
        choices=OPCIONES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
