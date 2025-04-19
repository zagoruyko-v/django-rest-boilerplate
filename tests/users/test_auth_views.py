import pytest
from rest_framework import status
from unittest.mock import patch
from django.urls import reverse


@patch("users.services.phone_auth_service.SmsService.send_sms")
@patch(
    "users.services.phone_auth_service.SmsService.generate_verification_code",
    return_value="123456",
)
@pytest.mark.django_db
def test_send_code(mock_generate_code, mock_send_sms, client):
    """Тест на отправку кода авторизации"""

    url = reverse("users:auth_phone_request")
    data = {"phone_number": "+79999999999"}

    response = client.post(url, data)

    assert response.status_code == 201
    assert response.data["message"] == "Код отправлен на ваш номер телефона"
    mock_send_sms.assert_called_once_with("+79999999999", "123456")


@patch(
    "users.services.phone_auth_service.PhoneAuthService.validate_verification_code",
    return_value=True,
)
@pytest.mark.django_db
def test_verify_code(mock_validate_code, client, user):
    """Тест на верификацию кода"""

    url = reverse("users:auth_phone_verify")
    data = {"phone_number": user.phone_number, "code": "123456"}

    response = client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["access"] is not None
    assert response.data["refresh"] is not None
    mock_validate_code.assert_called_once_with(user.phone_number, "123456")
