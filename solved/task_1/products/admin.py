from django.contrib import admin
from products.models import Product


@admin.register(Product)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
