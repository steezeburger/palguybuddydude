from django.db import models


class PalworldPlayerCheckIn(models.Model):
    player = models.ForeignKey('PalworldPlayer', on_delete=models.CASCADE)
    check_in_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'palworld_player_check_ins'
        verbose_name = 'Palworld Player Check In'
        verbose_name_plural = 'Palworld Player Check Ins'
