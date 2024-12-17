import re
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from users.models import Profile


@pytest.mark.django_db
def test_user_detail_displays_all_elements(client, student, teacher):
    client.force_login(student)
    response = client.get(f'/users/{student.username}/')
    assert response.status_code == HTTPStatus.OK
    assertContains(response, f'{student.first_name} {student.last_name}')
    assertContains(response, 'Student')
    assertContains(response, student.email)
    assertContains(response, student.profile.bio)
    response_text = response.content.decode()
    # sorl-thumbnail creates this path for thumbnails
    assert re.search(r'<img src="/media/cache.*?"', response_text)

    response = client.get(f'/users/{teacher.username}/')
    assert response.status_code == HTTPStatus.OK
    assertContains(response, 'Teacher')


@pytest.mark.django_db
def test_user_detail_contains_link_to_edit_profile(client, user_with_profile):
    client.force_login(user_with_profile)
    response = client.get(f'/users/{user_with_profile.username}/')
    assert response.status_code == HTTPStatus.OK
    assertContains(response, '/user/edit/')


@pytest.mark.django_db
def test_user_detail_as_student_contains_link_to_leave(client, student):
    client.force_login(student)
    response = client.get(f'/users/{student.username}/')
    assert response.status_code == HTTPStatus.OK
    assertContains(response, '/user/leave/')


@pytest.mark.django_db
def test_user_detail_as_teacher_does_not_contain_link_to_leave(client, teacher):
    client.force_login(teacher)
    response = client.get(f'/users/{teacher.username}/')
    assert response.status_code == HTTPStatus.OK
    assertNotContains(response, '/user/leave/')


@pytest.mark.django_db
def test_edit_profile_contains_right_user_info(client, user_with_profile):
    client.force_login(user_with_profile)
    response = client.get('/user/edit/')
    assertContains(response, user_with_profile.profile.avatar.url)
    assertContains(response, user_with_profile.profile.bio)


@pytest.mark.django_db
def test_edit_profile_works_properly(client, user_with_profile, fake, image):
    client.force_login(user_with_profile)
    payload = dict(bio=fake.paragraph(), avatar=image)
    response = client.post('/user/edit/', payload, follow=True)
    assertRedirects(response, f'/users/{user_with_profile.username}/')
    profile = Profile.objects.get(user=user_with_profile)
    assert profile.bio == payload['bio']
    assert profile.avatar.size == image.size, 'Error al guardar la imagen de avatar.'
    assertContains(response, 'User profile has been successfully saved.')


@pytest.mark.django_db
def test_leave_works(client, student, django_user_model):
    student_pk = student.pk
    client.force_login(student)
    response = client.get('/user/leave/', follow=True)
    assertRedirects(response, '/')
    User = django_user_model
    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=student_pk)
    assertContains(response, 'Good bye! Hope to see you soon.')


@pytest.mark.django_db
def test_leave_is_forbidden_for_teachers(client, teacher):
    client.force_login(teacher)
    response = client.get('/user/leave/')
    assert response.status_code == HTTPStatus.FORBIDDEN
