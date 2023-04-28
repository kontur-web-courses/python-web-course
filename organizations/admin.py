from django.contrib import admin

from organizations.models import Organization, Requisites


class RequisitesInline(admin.TabularInline):
    model = Requisites


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name")
    inlines = [RequisitesInline]
