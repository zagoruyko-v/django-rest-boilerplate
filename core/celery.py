from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Указываем, что Celery использует настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Используем строку конфигурации для настроек
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически регистрируем все задачи в проекте Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
