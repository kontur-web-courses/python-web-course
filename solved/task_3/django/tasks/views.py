from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
