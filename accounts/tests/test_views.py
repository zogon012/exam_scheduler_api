# accounts/tests/test_views.py

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user(authenticated_client):
    client, _ = authenticated_client(is_admin=True)
    url = reverse('customuser-list')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 2
    user = User.objects.get(id=response.data['id'])
    assert user.username == 'newuser'
    assert not user.is_admin

@pytest.mark.django_db
def test_update_user(authenticated_client, create_user):
    client, _ = authenticated_client(is_admin=True)
    user = create_user(username='updateuser', email='updateuser@example.com')
    url = reverse('customuser-detail', args=[user.id])
    data = {'username': 'updateduser'}
    response = client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert User.objects.get(id=user.id).username == 'updateduser'

@pytest.mark.django_db
def test_delete_user_with_admin(authenticated_client, create_user):
    client, _ = authenticated_client(is_admin=True)
    non_admin_user = create_user(username='deleteuser', email='deleteuser@example.com')

    initial_user_count = User.objects.count()

    url = reverse('customuser-detail', args=[non_admin_user.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Expected 204, got {response.status_code} with data: {response.data}"
    assert User.objects.count() == initial_user_count - 1

@pytest.mark.django_db
def test_delete_user_with_non_admin(authenticated_client, create_user):
    client, _ = authenticated_client(is_admin=False)
    another_non_admin_user = create_user(username='anotheruser', email='anotheruser@example.com')

    initial_user_count = User.objects.count()

    url = reverse('customuser-detail', args=[another_non_admin_user.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert User.objects.count() == initial_user_count