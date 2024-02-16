from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.crud_timestamps_mixin import CRUDTimestampsMixin
from common.models.soft_delete_timestamp_mixin import SoftDeleteTimestampMixin
from core.managers import UserManager


class User(CRUDTimestampsMixin,
           SoftDeleteTimestampMixin,
           AbstractBaseUser,
           PermissionsMixin):
    USERNAME_FIELD = 'email'
    objects = UserManager()

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        default_permissions = ()
        unique_together = []
        ordering = ('id',)
