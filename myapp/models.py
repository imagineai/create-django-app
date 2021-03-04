from django.db import models
from django.utils import timezone

from .management import dummymodel
from .user import User


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, null=True)
    due_date = models.DateField(null=True, default=timezone.now)
    done = models.BooleanField(null=True)
