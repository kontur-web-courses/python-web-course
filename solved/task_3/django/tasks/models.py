from django.db import models
from projects.models import Project


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW"
        IN_WORK = "IN_WORK"
        COMPLETE = "COMPLETE"

    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=Status.choices)
    deadline = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name
