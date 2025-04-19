from rest_framework import serializers
from users.utils.phone_number import validate_phone_number


class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, data):
        return validate_phone_number(data)


class PhoneAuthRequestCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class PhoneAuthVerifyCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    code = serializers.CharField()
