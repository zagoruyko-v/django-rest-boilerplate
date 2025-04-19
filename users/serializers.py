from rest_framework import serializers
from users.utils.phone_number import validate_phone_number

from .models import User


class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, data):
        return validate_phone_number(data)


class PhoneAuthRequestCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class PhoneAuthVerifyCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    code = serializers.CharField()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone_number",
            "email",
            "first_name",
            "last_name",
        ]
        read_only_fields = [
            "phone_number",
        ]


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
