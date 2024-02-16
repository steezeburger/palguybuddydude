import uuid
from django.db import models
from django.template.defaultfilters import truncatechars


class UUIDModelMixin(models.Model):
    """
    `uuid` field will be auto set with uuid4 values
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    @property
    def short_uuid(self):
        return truncatechars(self.uuid, 8)
