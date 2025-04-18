from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, PhoneVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
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
    readonly_fields = ("last_login", "date_joined")
    list_display = ("phone_number", "first_name", "last_name", "is_staff")
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "user",
        "code",
        "created_at",
        "verified_at",
        "is_valid_display",
    )
    search_fields = ("phone_number", "code", "user__phone_number")
    readonly_fields = ("created_at", "verified_at")

    def is_valid_display(self, obj):
        return obj.is_valid()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    is_valid_display.short_description = "Код действителен"
    is_valid_display.boolean = True
