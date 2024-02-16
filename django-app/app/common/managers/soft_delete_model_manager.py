from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.query.QuerySet):
    def delete(self, *args, **kwargs):
        if kwargs.get('force_delete', None):
            return super().delete()

        return super().update(is_active=False, deleted_at=now())

    def undelete(self, *args, **kwargs):
        return super().update(is_active=True, deleted_at=None)


class SoftDeleteModelManager(models.Manager):
    """
    Custom manager for models that use SoftDeleteTimestampMixin.
    """
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model)
