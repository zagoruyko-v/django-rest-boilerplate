import random
import string


class SmsService:
    @staticmethod
    def send_sms(phone_number: str, code: str):
        """Мокированная отправка SMS. На данный момент просто логирует"""
        print(f"Отправка SMS на номер {phone_number} с кодом {code}")

    @staticmethod
    def generate_verification_code(length=6):
        """Генерация случайного кода для верификации"""
        return "".join(random.choices(string.digits, k=length))
