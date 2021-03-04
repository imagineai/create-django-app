import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from todoapp.serializers import PersonExpandForeignSerializer, PersonSerializer

from .factories import PersonFactory, PersonWithForeignFactory, TodoFactory


class PersonSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.person = PersonWithForeignFactory.create()

    def test_that_a_person_is_correctly_serialized(self):
        person = self.person
        serializer = PersonSerializer
        serialized_person = serializer(person).data

        assert serialized_person['id'] == person.id
        assert serialized_person['email'] == person.email
        assert serialized_person['firstname'] == person.firstname
        assert serialized_person['lastname'] == person.lastname
        assert serialized_person['last_login'] == str(person.last_login)

        assert len(serialized_person['todos']) == person.todos.count()

    def test_that_a_person_is_correctly_serialized_with_expand_serializer(self):
        person = self.person
        serializer = PersonExpandForeignSerializer
        serialized_person = serializer(person).data
        assert serialized_person['id'] == person.id
        assert serialized_person['email'] == person.email
        assert serialized_person['firstname'] == person.firstname
        assert serialized_person['lastname'] == person.lastname
        assert serialized_person['last_login'] == str(person.last_login)

        assert len(serialized_person['todos']) == person.todos.count()

        for i in range(0, person.todos.count()):
            todo = person.todos.all()[i]
            serialized_todo = serialized_person['todos'][i]
            assert serialized_todo['title'] == todo.title
            assert serialized_todo['description'] == todo.description
            assert serialized_todo['id'] == todo.id
            assert serialized_todo['due_date'] == str(todo.due_date)

    def test_create_related_with_expanded_serializer(self):
        todos_dict = factory.build_batch(dict, FACTORY_CLASS=TodoFactory, size=3)
        for todo in todos_dict:
            todo.pop('assignee')
        person = factory.build(dict, FACTORY_CLASS=PersonWithForeignFactory, todos=todos_dict)
        serializer = PersonExpandForeignSerializer(data=person)
        assert serializer.is_valid()
        created_person = serializer.save()
        for todo in todos_dict:
            assert created_person.todos.filter(id=todo['id']).exists()
