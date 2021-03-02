from django.db import models

class DummyModel(models.Model):
    """Model used in the generation of permissions"""

    class Meta:
        # No database table creation or deletion  \
        # operations will be performed for this model.
        managed = False
        # disable "add", "change", "delete"
        # and "view" default permissions
        default_permissions = ()

