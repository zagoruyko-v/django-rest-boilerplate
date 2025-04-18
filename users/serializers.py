from rest_framework import serializers
from .models import PhoneVerification, User
from .services.sms_service import SmsService
from .utils.phone_number import validate_phone_number


class PhoneVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=12)

    class Meta:
        model = PhoneVerification
        fields = ["phone_number"]

    def validate_phone_number(self, value):
        return validate_phone_number(value)

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.save()
        PhoneVerification.objects.filter(
            phone_number=phone_number, verified_at__isnull=True
        ).delete()
        code = SmsService.generate_verification_code()
        phone_verification = PhoneVerification.objects.create(
            user=user, phone_number=phone_number, code=code
        )
        SmsService.send_sms(phone_number, code)
        return phone_verification


class PhoneTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone_number = attrs["phone_number"]
        code = attrs["code"]
        try:
            phone_verification = PhoneVerification.objects.get(
                phone_number=phone_number
            )
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Код не был отправлен на этот номер")

        if not phone_verification.is_valid():
            raise serializers.ValidationError("Код уже истек")

        if code != phone_verification.code:
            raise serializers.ValidationError("Неверный код")

        return attrs

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        user, created = User.objects.get_or_create(phone_number=phone_number)
        return user
