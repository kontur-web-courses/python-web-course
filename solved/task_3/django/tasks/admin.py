from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status", "deadline")
