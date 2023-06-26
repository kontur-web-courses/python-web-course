from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Organization(models.Model):
    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        db_table = "organizations"

    id = models.UUIDField(unique=True, primary_key=True)
    product_name = models.CharField(max_length=120)
    employees = models.ManyToManyField(User)
    created_by_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="organizations"
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return str(self.id)


class RequisitesName(models.TextChoices):
    NAME = "name", "name"
    INN = "inn", "inn"
    KPP = "kpp", "kpp"
    OGRN = "ogrn", "ogrn"


class Requisites(models.Model):
    class Meta:
        verbose_name = "Реквизит"
        verbose_name_plural = "Реквизиты"
        db_table = "requisites"
        unique_together = [["organization", "name"]]

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="requisites"
    )
    name = models.CharField(max_length=15, choices=RequisitesName.choices)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.value}"
