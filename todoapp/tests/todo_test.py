import json

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Todo
from .factories import CommentFactory, PersonFactory, TodoFactory
from .utils import generate_authenticated_api_client, generate_user

faker = Factory.create()


class Todo_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        TodoFactory.create_batch(size=3)
        self.assignee = PersonFactory.create()
        management.call_command("initialize")
        self.authenticated_api_client = generate_authenticated_api_client(
            generate_user(
                permissions=[]
            )
        )

    def test_create_todo(self):
        """
        Ensure we can create a new todo object.
        """
        client = self.authenticated_api_client
        todo_count = Todo.objects.count()
        todo_dict = factory.build(dict, FACTORY_CLASS=TodoFactory, assignee=self.assignee.pk)
        response = client.post(reverse('todo-list'), todo_dict)
        created_todo_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Todo.objects.count() == todo_count + 1
        todo = Todo.objects.get(pk=created_todo_pk)

        assert todo_dict['due_date'] == str(todo.due_date)

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.authenticated_api_client
        response = client.get(reverse('todo-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Todo.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.authenticated_api_client
        todo_qs = Todo.objects.all()
        todo_count = Todo.objects.count()

        for i, todo in enumerate(todo_qs, start=1):
            response = client.delete(reverse('todo-detail', kwargs={'pk': todo.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert todo_count - i == Todo.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.authenticated_api_client
        todo_pk = Todo.objects.first().pk
        todo_detail_url = reverse('todo-detail', kwargs={'pk': todo_pk})
        todo_dict = factory.build(dict, FACTORY_CLASS=TodoFactory, assignee=self.assignee.pk)
        response = client.patch(todo_detail_url, data=todo_dict)
        assert response.status_code == status.HTTP_200_OK

        assert todo_dict['title'] == response.data['title']
        assert todo_dict['description'] == response.data['description']
        assert todo_dict['due_date'] == response.data['due_date']
        assert todo_dict['done'] == response.data['done']

    def test_update_due_date_with_incorrect_value_data_type(self):
        client = self.authenticated_api_client
        todo = Todo.objects.first()
        todo_detail_url = reverse('todo-detail', kwargs={'pk': todo.pk})
        todo_due_date = todo.due_date
        data = {
            'due_date': faker.pystr(),
        }
        response = client.patch(todo_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert todo_due_date == Todo.objects.first().due_date

    def test_update_done_with_incorrect_value_data_type(self):
        client = self.authenticated_api_client
        todo = Todo.objects.first()
        todo_detail_url = reverse('todo-detail', kwargs={'pk': todo.pk})
        todo_done = todo.done
        data = {
            'done': faker.pystr(),
        }
        response = client.patch(todo_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert todo_done == Todo.objects.first().done

    def test_update_title_with_incorrect_value_outside_constraints(self):
        client = self.authenticated_api_client
        todo = Todo.objects.first()
        todo_detail_url = reverse('todo-detail', kwargs={'pk': todo.pk})
        todo_title = todo.title
        data = {
            'title': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(todo_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert todo_title == Todo.objects.first().title

    def test_update_description_with_incorrect_value_outside_constraints(self):
        client = self.authenticated_api_client
        todo = Todo.objects.first()
        todo_detail_url = reverse('todo-detail', kwargs={'pk': todo.pk})
        todo_description = todo.description
        data = {
            'description': faker.pystr(min_chars=1025, max_chars=1025),
        }
        response = client.patch(todo_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert todo_description == Todo.objects.first().description
