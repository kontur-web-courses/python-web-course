from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import RoleOperations

User = get_user_model()

admin.site.unregister(Group)


@admin.register(RoleOperations)
class RoleOperationsAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Organization info"),
            {"fields": ("portal_user_id", "email", "phone", "role", "deleted")},
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "created_at", "updated_at")},
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    list_display = ("username", "first_name", "last_name", "is_superuser", "deleted")
