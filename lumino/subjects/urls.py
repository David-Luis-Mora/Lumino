from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('<str:code>/', views.subject_detail, name='subject-detail'),
    path('<str:code>/lessons/', views.subject_lessons, name='subject_lessons'),
    path('<str:code>/lessons/add/', views.add_lesson, name='add-lesson'),
    path('<str:code>/lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('<str:code>/lessons/<int:pk>/edit/', views.edit_lesson, name='edit-lesson'),
    path('<str:code>/lessons/<int:pk>/delete/', views.delete_lesson, name='delete-lesson'),
    path('<str:code>/marks/', views.mark_list, name='mark-list'),
    path('<str:code>/marks/edit/', views.edit_marks, name='edit-marks'),
    path('certificate/', views.request_certificate, name='request-certificate'),
]
