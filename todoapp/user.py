from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    This UserModel is extending the django default UserModel
    here you can define any fields that you would want the users to have
    or create new models that extend this one to have different type of users
    the email field is an example.
    """
    email = models.EmailField(max_length=50, unique=True)
