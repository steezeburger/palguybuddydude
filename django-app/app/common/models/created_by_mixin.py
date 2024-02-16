from django.db import models


class CreatedByMixin(models.Model):
    """
    Adds `created_by` field.
    """
    created_by = models.ForeignKey(
        'core.User',
        db_index=True,
        related_name='%(class)ss_created',  # eg user.documents_created
        on_delete=models.CASCADE)

    class Meta:
        abstract = True
