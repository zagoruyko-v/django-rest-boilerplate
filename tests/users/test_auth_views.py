import pytest
from rest_framework import status
from unittest.mock import patch
from django.urls import reverse


@patch("users.services.sms_service.SmsService.send_sms")
@patch(
    "users.services.sms_service.SmsService.generate_verification_code",
    return_value="123456",
)
@pytest.mark.django_db
def test_send_code(mock_generate_code, mock_send_sms, client):
    """Тест на отправку кода авторизации"""

    mock_send_sms.return_value = None

    url = reverse("users:send-phone-code")
    data = {"phone_number": "+79999999999"}

    response = client.post(url, data)

    assert response.status_code == 201
    assert response.data["message"] == "Код отправлен на ваш номер телефона"

    mock_send_sms.assert_called_once_with("+79999999999", "123456")


@patch("users.services.sms_service.SmsService.send_sms")
@pytest.mark.django_db
def test_verify_code(mock_send_sms, client, user, phone_verification):
    """Тест на верификацию кода"""

    mock_send_sms.return_value = True

    url = reverse("users:verify-phone")  # Путь к твоей вьюшке
    data = {"phone_number": "+79999999999", "code": "123456"}

    response = client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.data
    assert response.data["access_token"] is not None
