from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from todo.models import Todo, User

faker = Factory.create()


class TodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo
        django_get_or_create = ('id',)

    id = LazyAttribute(lambda o: randint(0, 10000))
    date = LazyFunction(faker.date)
    text = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    done = LazyFunction(faker.boolean)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    email = factory.LazyAttribute(lambda o: faker.email())
    username = factory.LazyAttribute(lambda o: o.email)
    is_superuser = False
    is_active = True
