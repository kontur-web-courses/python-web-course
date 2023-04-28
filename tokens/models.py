from django.db import models


class Token(models.Model):
    class Meta:
        verbose_name = "Ключ"
        verbose_name_plural = "Ключи"
        db_table = "tokens"

    jwt = models.CharField(max_length=150)
    secret = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
