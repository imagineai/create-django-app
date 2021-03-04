from rest_framework import viewsets

from .models import Todo
from .serializers import TodoSerializer


class TodoApiViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = []
    filterset_fields = ['id', 'title', 'description', 'due_date', 'done']
