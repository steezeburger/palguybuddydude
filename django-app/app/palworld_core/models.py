from django.db import models

from common.models.crud_timestamps_mixin import CRUDTimestampsMixin
from common.models.soft_delete_timestamp_mixin import SoftDeleteTimestampMixin
from common.models.uuid_mixin import UUIDModelMixin


class PalworldPlayer(UUIDModelMixin, CRUDTimestampsMixin, SoftDeleteTimestampMixin):
    player_uid = models.CharField(max_length=255, unique=True)
    steam_id = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255, unique=True)

    first_seen_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'palworld_players'
        verbose_name = 'Palworld Player'
        verbose_name_plural = 'Palworld Players'

    @property
    def is_online(self):
        # FIXME - this is just a placeholder for now; logic not correct.
        return self.last_seen_at > self.first_seen_at
