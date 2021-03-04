from rest_framework import mixins, viewsets

from .models import Comment, Person, Todo
from .serializers import CommentSerializer, PersonSerializer, TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = []
    filterset_fields = ['done']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    filterset_fields = ['status']


class CreatePersonViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = []
