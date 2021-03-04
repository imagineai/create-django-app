from rest_framework import serializers

from .models import Comment, Person, Todo


class TodoSerializer(serializers.ModelSerializer):

    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Comment.objects.all(),
    )

    assignee = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all()
    )

    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(TodoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'due_date', 'done', 'comments', 'assignee']


class CommentSerializer(serializers.ModelSerializer):

    todo = serializers.PrimaryKeyRelatedField(
        queryset=Todo.objects.all()
    )

    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(CommentSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ['id', 'message', 'submitted', 'status', 'todo']


class PersonSerializer(serializers.ModelSerializer):

    todos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Todo.objects.all(),
    )

    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PersonSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = ['id', 'email', 'firstname', 'lastname', 'last_login', 'todos']


class TodoExpandForeignSerializer(TodoSerializer):
    comments = CommentSerializer(many=True)

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])

        todo = Todo.objects.create(**validated_data)

        for comment in comments_data:
            Comment.objects.create(todo=todo, **comment)

        return todo


class PersonExpandForeignSerializer(PersonSerializer):
    todos = TodoSerializer(many=True)

    def create(self, validated_data):
        todos_data = validated_data.pop('todos', [])

        person = Person.objects.create(**validated_data)

        for todo in todos_data:
            Todo.objects.create(assignee=person, **todo)

        return person
