from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('<string:name>/', views.subject_detail, name='subject-detail'),
    path('<string:name>/lessons/', views.subject_lessons, name='subject_lessons'),
    path('<string:name>/lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('<string:name>/lessons/add', views.add_lesson, name='lesson-detail'),
    path('<string:name>/lessons/<int:pk>/edit', views.edit_lesson, name='lesson-detail'),
    path('<string:name>/lessons/<int:pk>/delete', views.delete_lesson, name='lesson-detail'),
    path('<string:name>/marks', views.mark_list, name='subject-detail'),
    path('<string:name>/marks/edit', views.edit_marks, name='subject-detail'),
]
