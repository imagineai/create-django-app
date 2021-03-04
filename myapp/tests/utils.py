from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient

from .factories import UserFactory


def generate_user(groups=[], is_active=True, is_superuser=False, permissions=[]):
    """
    Generate a custom user
    """
    user = UserFactory.create(is_active=is_active, is_superuser=is_superuser)
    for group in groups:
        user.groups.add(Group.objects.get(name=group))
    for permission in permissions:
        user.user_permissions.add(Permission.objects.get(codename=permission))
    return user


def generate_authenticated_api_client(user):
    """
    Generate an authenticated api client, with the given user
    """
    api_client = APIClient()
    api_client.force_authenticate(user)
    return api_client
