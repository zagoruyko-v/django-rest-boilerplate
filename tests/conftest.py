import os
import pytest
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"
django.setup()

from users.models import User, ConfirmationCode


@pytest.fixture
def user():
    """Создаем пользователя для тестов"""
    return User.objects.create_user(phone_number="+79999999999", password="password123")


@pytest.fixture
def phone_verification(user):
    """Создаем объект PhoneAuthentication для тестов"""
    return ConfirmationCode.objects.create(
        user=user, phone_number="+79999999999", code="123456"
    )


@pytest.fixture
def client():
    """APIClient для тестов"""
    from rest_framework.test import APIClient

    return APIClient()
