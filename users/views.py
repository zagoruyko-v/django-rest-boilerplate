import logging

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, ConfirmationCode
from .serializers import (
    PhoneAuthRequestCodeSerializer,
    PhoneAuthVerifyCodeSerializer,
    UserInfoSerializer,
)
from .services.phone_auth_service import TooManyRequestsError, ConfirmationCodeService

logger = logging.getLogger(__name__)


class PhoneAuthRequestCodeView(GenericAPIView):
    serializer_class = PhoneAuthRequestCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        user, created = User.objects.get_or_create_by_phone(phone_number)

        purpose = (
            ConfirmationCode.Purpose.REGISTER
            if created
            else ConfirmationCode.Purpose.LOGIN
        )

        ConfirmationCodeService(user).request(
            delivery_method=ConfirmationCode.DeliveryMethod.PHONE,
            purpose=purpose,
        )

        if created:
            logger.info(f"Создан новый пользователь {user.id} по номеру {phone_number}")

        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(
            {"message": "Код отправлен на ваш номер телефона"},
            status=http_status,
        )


class PhoneAuthVerifyCodeView(GenericAPIView):
    serializer_class = PhoneAuthVerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]
        user = User.objects.get(phone_number=phone_number)

        confirmation_service = ConfirmationCodeService(user)

        try:
            confirmation_service.verify(
                delivery_method=ConfirmationCode.DeliveryMethod.PHONE,
                input_code=code,
            )
        except TooManyRequestsError as e:
            logger.warning(f"Слишком частые запросы для пользователя {user.id}")
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            logger.info(f"Ошибка при верификации кода для пользователя {user.id}")
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(
            f"Код успешно подтвержден для пользователя {user.id} по номеру {phone_number}"
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserInfoView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
