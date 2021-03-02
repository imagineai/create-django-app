from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from ..dummymodel import DummyModel


class Command(BaseCommand):
    """Django command to create Initial Data"""

    def handle(self, *args, **options):
        # Cant generate a permission without a class
        content_type = ContentType.objects.get_for_model(DummyModel)
        # Create permissions from list
        PERMISSION_LIST = []

        for permission in PERMISSION_LIST:
            Permission.objects.get_or_create(codename=permission, name=permission.title(), content_type=content_type)

        PERMISSION_GROUP_RELATION = [
        ]

        for relation in PERMISSION_GROUP_RELATION:
            group, created = Group.objects.get_or_create(name=relation['group'])
            for permission_codename in relation['permissions']:
                permission = Permission.objects.get(codename=permission_codename)
                group.permissions.add(permission)
