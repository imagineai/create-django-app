import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from todoapp.serializers import TodoExpandForeignSerializer, TodoSerializer

from .factories import (
    CommentFactory,
    PersonFactory,
    TodoFactory,
    TodoWithForeignFactory,
)


class TodoSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.todo = TodoWithForeignFactory.create()

    def test_that_a_todo_is_correctly_serialized(self):
        todo = self.todo
        serializer = TodoSerializer
        serialized_todo = serializer(todo).data

        assert serialized_todo['id'] == todo.id
        assert serialized_todo['title'] == todo.title
        assert serialized_todo['description'] == todo.description
        assert serialized_todo['done'] == todo.done
        assert serialized_todo['due_date'] == str(todo.due_date)

        assert len(serialized_todo['comments']) == todo.comments.count()

    def test_that_a_todo_is_correctly_serialized_with_expand_serializer(self):
        todo = self.todo
        serializer = TodoExpandForeignSerializer
        serialized_todo = serializer(todo).data
        assert serialized_todo['id'] == todo.id
        assert serialized_todo['title'] == todo.title
        assert serialized_todo['description'] == todo.description
        assert serialized_todo['done'] == todo.done
        assert serialized_todo['due_date'] == str(todo.due_date)

        assert len(serialized_todo['comments']) == todo.comments.count()

        for i in range(0, todo.comments.count()):
            comment = todo.comments.all()[i]
            serialized_comment = serialized_todo['comments'][i]
            assert serialized_comment['message'] == comment.message
            assert serialized_comment['status'] == comment.status
            assert serialized_comment['id'] == comment.id
            assert serialized_comment['submitted'] == str(comment.submitted)

    def test_create_related_with_expanded_serializer(self):
        comments_dict = factory.build_batch(dict, FACTORY_CLASS=CommentFactory, size=3)
        for comment in comments_dict:
            comment.pop('todo')
        assignee_for_todos = PersonFactory.create()
        todo = factory.build(dict, FACTORY_CLASS=TodoWithForeignFactory,
                             comments=comments_dict, assignee=assignee_for_todos.pk)
        serializer = TodoExpandForeignSerializer(data=todo)
        assert serializer.is_valid()
        created_todo = serializer.save()
        for comment in comments_dict:
            assert created_todo.comments.filter(id=comment['id']).exists()
