from django.db import models
from django.utils import timezone

from .management import dummymodel
from .user import User


class Todo(models.Model):
    assignee = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='todos')
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, null=True)
    due_date = models.DateField(null=True, default=timezone.now)
    done = models.BooleanField(null=True)


class Comment(models.Model):
    READ = 1
    UNREAD = 2
    STATUS_CHOICES = [
        (READ, 'READ'),
        (UNREAD, 'UNREAD')
    ]
    todo = models.ForeignKey('Todo', on_delete=models.CASCADE, related_name='comments')
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=512, null=True)
    submitted = models.DateField(null=True, default=timezone.now)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True)


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, null=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    last_login = models.DateField(null=True, default=timezone.now)
