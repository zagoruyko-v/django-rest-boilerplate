import re
from rest_framework import serializers


def normalize_phone_number(phone_number: str) -> str:
    phone_number = phone_number.strip()
    if phone_number.startswith("8"):
        phone_number = "+7" + phone_number[1:]
    elif phone_number.startswith("7"):
        phone_number = "+7" + phone_number[1:]
    elif phone_number.startswith("+7"):
        pass
    else:
        pass

    phone_number = re.sub(r"[^\d+]", "", phone_number)
    return phone_number


def validate_phone_number(value: str) -> str:
    normalized = normalize_phone_number(value)
    if not re.fullmatch(r"^\+7\d{10}$", normalized):
        raise serializers.ValidationError(
            "Номер телефона должен быть в формате +7XXXXXXXXXX"
        )
    return normalized
