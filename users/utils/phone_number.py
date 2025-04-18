import re


def normalize_phone_number(phone_number):
    return phone_number.strip().replace(" ", "").replace("-", "")


def validate_phone_number(value):
    phone_regex = r"^\+7\d{10}$"
    if not re.match(phone_regex, value):
        raise ValueError("Номер телефона должен быть в формате +7XXXXXXXXXX")
    return value
