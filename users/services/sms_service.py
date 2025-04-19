class SmsService:
    @staticmethod
    def send_sms(phone_number: str, code: str):
        """Мокированная отправка SMS. На данный момент просто логирует"""
        print(f"Отправка SMS на номер {phone_number} с кодом {code}")
