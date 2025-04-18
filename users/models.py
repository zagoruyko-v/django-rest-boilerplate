from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone
from .utils.phone_number import normalize_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Необходимо указать номер телефона")

        phone_number = normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError(
                "Суперпользователь должен иметь is_staff=True и is_superuser=True."
            )
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="Номер телефона",
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.phone_number


class PhoneVerification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    phone_number = models.CharField(max_length=12, verbose_name="Номер телефона")
    code = models.CharField(max_length=6, verbose_name="Код подтверждения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    verified_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Время подтверждения"
    )

    def is_valid(self):
        if self.verified_at:
            return False
        expiration_time = self.created_at + timezone.timedelta(minutes=5)
        return timezone.now() <= expiration_time

    def __str__(self):
        return f"Код для {self.phone_number}"

    class Meta:
        verbose_name = "подтверждение номера телефона"
        verbose_name_plural = "подтверждения номеров телефонов"
