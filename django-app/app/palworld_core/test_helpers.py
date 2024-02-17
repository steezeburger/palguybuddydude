import factory

from factory.django import DjangoModelFactory

from palworld_core.models import PalworldPlayer


class PalworldPlayerFactory(DjangoModelFactory):
    class Meta:
        model = PalworldPlayer

    player_uid = factory.Faker('uuid4')
    steam_id = factory.Faker('uuid4')
    display_name = factory.Faker('name')
    first_seen_at = factory.Faker('date_time')
    last_seen_at = factory.Faker('date_time')

    uuid = factory.Faker('uuid4')
    created_at = factory.Faker('date_time')
    modified_at = factory.Faker('date_time')
    deleted_at = factory.Faker('date_time')
    is_active = factory.Faker('boolean')
