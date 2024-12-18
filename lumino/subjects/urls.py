from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', lambda request: redirect('subjects/', permanent=False)),
    path('subjects/', views.subject_list, name='subject-list'),
    path('subjects/enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('subjects/unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('subjects/<str:code>/', views.subject_detail, name='subject-detail'),
    path('subjects/<str:code>/lessons/', views.subject_lessons, name='subject_lessons'),
    path('subjects/lessons/<str:pk>/', views.lesson_detail, name='lesson-detail'),
    path('subjects/<str:code>/lessons/add', views.add_lesson, name='add-lesson'),
    path('subjects/lessons/<int:pk>/edit', views.edit_lesson, name='edit-lesson'),
    path('subjects/lessons/<int:pk>/delete', views.delete_lesson, name='delete-lesson'),
    path('subjects/<str:code>/marks', views.mark_list, name='mark-list'),
    path('subjects/<str:code>/marks/edit', views.edit_marks, name='edit-marks'),
]
