from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import TaskLog


@admin.register(TaskLog)
class TaskLogAdmin(SimpleHistoryAdmin):
	list_display = (
		"created_at",
		"event_type",
		"status",
		"recipient",
		"task_id",
	)
	list_filter = (
		"event_type",
		"status",
		"created_at",
	)
	search_fields = (
		"recipient",
		"task_id",
	)

	readonly_fields = [field.name for field in TaskLog._meta.fields]

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
