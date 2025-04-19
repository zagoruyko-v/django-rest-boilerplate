from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from .models import User, ConfirmationCode


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Персональная информация"), {"fields": ("first_name", "last_name")}),
        (
            _("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Важные даты"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("last_login",)
    list_display = ("phone_number", "first_name", "last_name", "is_staff")
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = (
        "user",
        "code",
        "delivery_method",
        "purpose",
        "status",
        "created_at",
        "verified_at",
    )
    search_fields = ("user__phone_number", "code", "user__email")
    readonly_fields = ("created_at", "verified_at")
    list_filter = ("status", "created_at", "delivery_method")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
