from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory
from todoapp.models import Comment, Person, Todo, User

faker = Factory.create()


class TodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo

    assignee = factory.SubFactory('todoapp.tests.factories.PersonFactory')
    id = LazyAttribute(lambda o: randint(0, 10000))
    title = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    description = LazyAttribute(lambda o: faker.text(max_nb_chars=1024))
    due_date = LazyFunction(faker.date)
    done = LazyFunction(faker.boolean)


class TodoWithForeignFactory(TodoFactory):
    @factory.post_generation
    def comments(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                CommentFactory(todo=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                CommentFactory(todo=obj)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    todo = factory.SubFactory('todoapp.tests.factories.TodoFactory')
    id = LazyAttribute(lambda o: randint(0, 10000))
    message = LazyAttribute(lambda o: faker.text(max_nb_chars=512))
    submitted = LazyFunction(faker.date)
    status = fuzzy.FuzzyChoice(Comment.STATUS_CHOICES, getter=lambda c: c[0])


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    id = LazyAttribute(lambda o: randint(0, 10000))
    email = LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    firstname = LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    lastname = LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    last_login = LazyFunction(faker.date)


class PersonWithForeignFactory(PersonFactory):
    @factory.post_generation
    def todos(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TodoFactory(assignee=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TodoFactory(assignee=obj)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    email = factory.LazyAttribute(lambda o: faker.email())
    username = factory.LazyAttribute(lambda o: o.email)
    is_superuser = False
    is_active = True
