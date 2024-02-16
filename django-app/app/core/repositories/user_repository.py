from common.repositories.base_repository import BaseRepository
from core.models import User


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def get_by_filter(cls, filter_input: dict = None):
        if filter_input:
            objects = cls.get_queryset().filter(**filter_input)
        else:
            objects = cls.get_queryset().all()
        return objects

    @classmethod
    def create(cls, data: dict) -> 'User':
        user = cls.model.objects.create(**data)
        return user

    @classmethod
    def update(cls, *, pk=None, obj: 'User' = None, data: dict) -> 'User':
        user = obj or cls.get(pk=pk)

        if data.get('is_active'):
            user.is_active = data['is_active']

        user.save()
        return user
