from django.db import models
from django.utils import timezone
from .management import dummymodel
from .user import User

class Todo(models.Model) :
    id = models.IntegerField(primary_key=True)
    date = models.DateField(null=True, default=timezone.now)
    text = models.CharField(max_length=255, null=True)
    done = models.BooleanField(null=True)

