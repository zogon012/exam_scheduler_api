# conftest.py

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope='session', autouse=True)
def create_superuser(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create_superuser(
            username='admin_user',
            email='admin@example.com',
            password='password123'
        )
        user.is_admin = True
        user.save()

@pytest.fixture
def create_user():
    def _create_user(username, email, password='password123', is_admin=False):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin
        )
        return user
    return _create_user

@pytest.fixture
def authenticated_client(api_client, create_user, create_superuser):
    def _get_client(is_admin=False):
        if is_admin:
            user = User.objects.get(username='admin_user')
        else:
            user = create_user(username='testuser', email='testuser@example.com', is_admin=is_admin)
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        return api_client, user
    return _get_client