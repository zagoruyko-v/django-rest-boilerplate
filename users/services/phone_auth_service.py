import logging
from datetime import timedelta
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.crypto import get_random_string

from users.models import ConfirmationCode

logger = logging.getLogger(__name__)


class TooManyRequestsError(Exception):
    pass


class ConfirmationCodeService:
    CODE_LENGTH = 6
    CODE_CHARSET = "0123456789"
    CODE_TTL = timedelta(minutes=3)

    def __init__(self, user):
        self.user = user

    def _generate_code(self):
        return get_random_string(
            length=self.CODE_LENGTH, allowed_chars=self.CODE_CHARSET
        )

    def _not_expired(self, created_at):
        return now() <= created_at + self.CODE_TTL

    def _deliver_code(self, delivery_method, code):
        logger.info(
            f"Отправка кода {code} пользователю {self.user} через {delivery_method}"
        )

    def is_valid(self, code):
        return code.status == ConfirmationCode.Status.CREATED and self._not_expired(
            code.created_at
        )

    @transaction.atomic
    def request(self, delivery_method, purpose):
        recent_code = ConfirmationCode.objects.filter(
            user=self.user,
            delivery_method=delivery_method,
            created_at__gte=now() - self.CODE_TTL,
        ).first()
        if recent_code:
            logger.warning(f"Слишком частые запросы для пользователя {self.user}")
            raise TooManyRequestsError("Слишком частые запросы. Попробуйте позже.")

        ConfirmationCode.objects.filter(
            user=self.user,
            delivery_method=delivery_method,
            status=ConfirmationCode.Status.CREATED,
        ).delete()

        code = self._generate_code()
        confirmation_code = ConfirmationCode.objects.create(
            user=self.user,
            code=code,
            purpose=purpose,
            delivery_method=delivery_method,
        )

        self._deliver_code(delivery_method, code)
        logger.debug(
            f"Код {code} создан и отправлен пользователю {self.user} ({delivery_method})"
        )
        return confirmation_code

    @transaction.atomic
    def verify(self, delivery_method, input_code):
        confirmation_code = ConfirmationCode.objects.filter(
            user=self.user,
            delivery_method=delivery_method,
            status=ConfirmationCode.Status.CREATED,
        ).first()

        if not confirmation_code:
            logger.warning(
                f"Не найден код для пользователя {self.user} и метода {delivery_method}"
            )
            raise ValidationError("Код не найден")

        if confirmation_code.code != input_code or not self.is_valid(confirmation_code):
            logger.info(f"Неверный или просроченный код от пользователя {self.user}")
            raise ValidationError("Неверный или просроченный код")

        confirmation_code.verified_at = now()
        confirmation_code.mark_used()
        confirmation_code.save(update_fields=["status", "verified_at"])
        logger.info(f"Код подтвержден для пользователя {self.user}")

        return confirmation_code
