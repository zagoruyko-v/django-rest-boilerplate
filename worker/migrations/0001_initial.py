# Generated by Django 5.0.4 on 2025-04-19 14:24

import django.db.models.deletion
import django_fsm
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, verbose_name='ID задачи')),
                ('event_type', models.CharField(choices=[('sms', 'СМС'), ('email', 'Почта')], max_length=50, verbose_name='Тип события')),
                ('recipient', models.CharField(max_length=255, verbose_name='Получатель')),
                ('payload', models.JSONField(blank=True, null=True, verbose_name='Переданные данные')),
                ('status', django_fsm.FSMField(choices=[('pending', 'В ожидании'), ('success', 'Успешно'), ('failed', 'Ошибка')], default='pending', max_length=50, verbose_name='Статус')),
                ('result_info', models.JSONField(blank=True, null=True, verbose_name='Результат выполнения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Лог задачи',
                'verbose_name_plural': 'Логи задач',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalTaskLog',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, verbose_name='ID задачи')),
                ('event_type', models.CharField(choices=[('sms', 'СМС'), ('email', 'Почта')], max_length=50, verbose_name='Тип события')),
                ('recipient', models.CharField(max_length=255, verbose_name='Получатель')),
                ('payload', models.JSONField(blank=True, null=True, verbose_name='Переданные данные')),
                ('status', django_fsm.FSMField(choices=[('pending', 'В ожидании'), ('success', 'Успешно'), ('failed', 'Ошибка')], default='pending', max_length=50, verbose_name='Статус')),
                ('result_info', models.JSONField(blank=True, null=True, verbose_name='Результат выполнения')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Обновлено')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Лог задачи',
                'verbose_name_plural': 'historical Логи задач',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
