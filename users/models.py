from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):

    def _create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(phone_number, password, **extra_fields)

    def get_or_create_by_phone(self, phone_number):
        return self.get_or_create(phone_number=phone_number)

    def get_or_create_by_email(self, email):
        return self.get_or_create(email=email)


class User(AbstractUser):
    username = None
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="Номер телефона",
    )

    objects = UserManager()
    history = HistoricalRecords()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.phone_number


class ConfirmationCode(models.Model):
    class DeliveryMethod(models.TextChoices):
        PHONE = "phone", "Телефон"
        EMAIL = "email", "Email"

    class Purpose(models.TextChoices):
        REGISTER = "register", "Регистрация"
        LOGIN = "login", "Авторизация"

    class Status(models.TextChoices):
        CREATED = "created", "Создан"
        USED = "used", "Использован"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    code = models.CharField(
        max_length=6,
        verbose_name="Код",
    )
    delivery_method = models.CharField(
        max_length=50,
        choices=DeliveryMethod.choices,
        verbose_name="Способ доставки",
    )
    purpose = models.CharField(
        max_length=50,
        choices=Purpose.choices,
        verbose_name="Назначение",
    )
    status = FSMField(
        default=Status.CREATED,
        choices=Status.choices,
        protected=True,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время подтверждения",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "код подтверждения"
        verbose_name_plural = "коды подтверждений"

    def __str__(self):
        return f"Код для {self.user} ({self.get_delivery_method_display()}) — {self.get_purpose_display()}"

    @transition(field=status, source=Status.CREATED, target=Status.USED)
    def mark_used(self):
        self.verified_at = timezone.now()

    def clean(self):
        if not self.user.phone_number and not self.user.email:
            raise ValidationError(
                "У пользователя должен быть указан телефон или email."
            )
