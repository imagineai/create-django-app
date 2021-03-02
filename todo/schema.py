from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations.todo import CreateTodo, DeleteTodo, UpdateTodo
from .types import TodoNode


class Query(ObjectType):
    todo_api = relay.Node.Field(TodoNode)

    all_todo_api = DjangoFilterConnectionField(TodoNode)


class Mutation(ObjectType):
    create_todo_api = CreateTodo.Field()

    update_todo_api = UpdateTodo.Field()

    delete_todo_api = DeleteTodo.Field()
