from django.db import models
from django_fsm import FSMField, transition
from simple_history.models import HistoricalRecords


class TaskLog(models.Model):
    class EventType(models.TextChoices):
        SMS = "sms", "СМС"
        EMAIL = "email", "Почта"

    class Status(models.TextChoices):
        PENDING = "pending", "В ожидании"
        SUCCESS = "success", "Успешно"
        FAILED = "failed", "Ошибка"

    task_id = models.CharField(
        max_length=255,
        verbose_name="ID задачи",
    )

    event_type = models.CharField(
        max_length=50,
        choices=EventType.choices,
        verbose_name="Тип события",
    )

    recipient = models.CharField(
        max_length=255,
        verbose_name="Получатель",
    )

    payload = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Переданные данные",
    )

    status = FSMField(
        default=Status.PENDING,
        choices=Status.choices,
        verbose_name="Статус",
    )

    result_info = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Результат выполнения",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено",
    )

    history = HistoricalRecords()

    @transition(field=status, source=Status.PENDING, target=Status.SUCCESS)
    def mark_success(self):
        pass

    @transition(field=status, source=Status.PENDING, target=Status.FAILED)
    def mark_failed(self):
        pass

    class Meta:
        verbose_name = "сelery"
        verbose_name_plural = "сelery"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_event_type_display()} → {self.recipient} [{self.status}]"
