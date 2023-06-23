from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = "user", "user"
    ADMIN = "admin", "admin"
    APPROVER = "approver", "approver"


class Operations(models.TextChoices):
    ADMIN_INVITE = "admin_invite", "admin invite"
    ADD_PAYMENT = "add_payment", "add payment"
    APPROVE_PAYMENT = "approve_payment", "approve payment"
    SEND_PAYMENT = "send_payment", "send payment"
    CAN_VIEW_BALANCE = "can_view_balance", "can view balance"


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "users"

    portal_user_id = models.UUIDField(unique=True, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=False)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=False)

    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.USER)

    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}" if self.first_name else self.username
        )


class RoleOperations(models.Model):
    class Meta:
        verbose_name = "Операции роли"
        verbose_name_plural = "Операции роли"
        db_table = "role_operations"

    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.USER)
    operation = models.CharField(max_length=30, choices=Operations.choices)

    def __str__(self):
        return self.get_role_display()
