from graphene import relay
from graphene_django import DjangoObjectType

from .models import Todo


class TodoNode(DjangoObjectType):

    class Meta:
        model = Todo
        interfaces = (relay.Node, )
        fields = ['id', 'date', 'text', 'done']
        filter_fields = ['id', 'date', 'text', 'done']
