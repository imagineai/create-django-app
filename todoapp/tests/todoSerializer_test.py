import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from todoapp.serializers import TodoSerializer

from .factories import TodoFactory


class TodoSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.todo = TodoFactory.create()

    def test_that_a_todo_is_correctly_serialized(self):
        todo = self.todo
        serializer = TodoSerializer
        serialized_todo = serializer(todo).data

        assert serialized_todo['id'] == todo.id
        assert serialized_todo['title'] == todo.title
        assert serialized_todo['description'] == todo.description
        assert serialized_todo['done'] == todo.done
        assert serialized_todo['due_date'] == str(todo.due_date)
