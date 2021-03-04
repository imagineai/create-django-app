from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(TodoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'due_date', 'done']
