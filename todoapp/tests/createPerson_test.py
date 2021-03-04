import json

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Person
from .factories import PersonFactory, TodoFactory
from .utils import generate_authenticated_api_client, generate_user

faker = Factory.create()


class CreatePerson_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        PersonFactory.create_batch(size=3)
        management.call_command("initialize")
        self.authenticated_api_client = generate_authenticated_api_client(
            generate_user(
                permissions=[]
            )
        )

    def test_create_person(self):
        """
        Ensure we can create a new person object.
        """
        client = self.authenticated_api_client
        person_count = Person.objects.count()
        person_dict = factory.build(dict, FACTORY_CLASS=PersonFactory)
        response = client.post(reverse('create_person-list'), person_dict)
        created_person_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Person.objects.count() == person_count + 1
        person = Person.objects.get(pk=created_person_pk)

        assert person_dict['last_login'] == str(person.last_login)
