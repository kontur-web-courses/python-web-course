from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from services.data import regenerate
from tokens.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    change_list_template = "admin/token_list.html"

    list_display = ("jwt",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("regenerate_data/", self._regenerate_data)]
        return my_urls + urls

    def _regenerate_data(self, request):
        regenerate()
        return HttpResponseRedirect("../")

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
