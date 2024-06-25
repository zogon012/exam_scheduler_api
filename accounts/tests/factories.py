# accounts/tests/factories.py

import factory
from django.contrib.auth import get_user_model

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username', 'email')

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_admin = False