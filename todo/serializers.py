from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(TodoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Todo
        fields = ['id', 'date', 'text', 'done']
