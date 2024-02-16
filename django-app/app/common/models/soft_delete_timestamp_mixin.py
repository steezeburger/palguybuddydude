from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.managers.soft_delete_model_manager import SoftDeleteModelManager

is_active_help_text = _(
    'Designates whether this object should be treated as active. '
    'Unselect this instead of deleting objects.'
)


class SoftDeleteTimestampMixin(models.Model):
    """
    Set `is_active` to False instead of deleting rows in the database.
    `deleted_at` will be set to the current time at time of deletion.
    """
    deleted_at = models.DateTimeField(db_index=True, null=True)
    is_active = models.BooleanField(_('active'),
                                    db_index=True,
                                    default=True,
                                    help_text=is_active_help_text)

    objects = SoftDeleteModelManager()

    def delete(self, *args, **kwargs):
        if kwargs.pop('force_delete', None):
            super().delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            self.is_active = False
            super().save()

    def undelete(self, *args, **kwargs):
        self.is_active = True
        self.deleted_at = None
        super().save()

    class Meta:
        abstract = True
