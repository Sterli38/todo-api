from rest_framework import viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD для задач: list, create, retrieve, update (PUT), destroy."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_value_regex = r"\d+"  # нечисловой id -> 404
    # PATCH по заданию не нужен
    http_method_names = ["get", "post", "put", "delete", "head", "options"]
