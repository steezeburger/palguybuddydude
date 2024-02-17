from django.db import models


class CRUDTimestampsMixin(models.Model):
    """
    `created_at` will be set on creation.
    `modified_at` will be updated on saves.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
