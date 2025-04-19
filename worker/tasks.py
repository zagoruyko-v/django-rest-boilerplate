import random
import time
from celery import shared_task
from django.utils import timezone
from myapp.models import TaskLog


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_sms_task(self, phone_number: str, code: str):
    """Celery задача для отправки SMS с retry при ошибке"""
    log = TaskLog.objects.create(
        task_id=self.request.id,
        event_type=TaskLog.EventType.SMS,
        recipient=phone_number,
        status=TaskLog.Status.PENDING,
        payload={"message": f"Отправка SMS на номер {phone_number} с кодом {code}"},
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )

    try:
        print(f"Отправка SMS на номер {phone_number} с кодом {code} начата.")
        time.sleep(60)

        if random.choice([True, False]):
            raise Exception("Ошибка при отправке SMS!")

        log.status = TaskLog.Status.SUCCESS
        log.result_info = {"info": f"SMS отправлена на {phone_number} с кодом {code}"}
        log.save()

        print(f"Отправка SMS на номер {phone_number} с кодом {code} успешно выполнена")

    except Exception as e:
        log.status = TaskLog.Status.FAILED
        log.result_info = {"error": str(e)}
        log.save()

        print(f"Ошибка при отправке SMS на номер {phone_number}. Попытка повторить...")

        raise self.retry(exc=e)
