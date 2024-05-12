from django.contrib import admin
from projects.models import Project


@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
