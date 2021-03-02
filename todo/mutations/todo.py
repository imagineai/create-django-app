import graphene
from graphene import relay
from graphql_relay import from_global_id
from todo.models import Todo
from todo.types import TodoNode

class TodoData(graphene.InputObjectType):
    id = graphene.Int()
    date = graphene.Date()
    text = graphene.String()
    done = graphene.Boolean()



class CreateTodo(relay.ClientIDMutation):
    class Input:
        data = TodoData()

    todo = graphene.Field(TodoNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data ):

        obj = Todo.objects.create(**data)



        return CreateTodo(todo=obj)

class UpdateTodo(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = TodoData()

    todo = graphene.Field(TodoNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):

        obj, _ = Todo.objects.update_or_create(pk=from_global_id(id)[1], defaults=data)

        
        return UpdateTodo(todo=obj)

class DeleteTodo(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = Todo.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteTodo(ok=True)

