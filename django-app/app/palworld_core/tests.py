from django.test import TestCase

from palworld_core.test_helpers import PalworldPlayerFactory


class TestPalworldPlayerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.player = PalworldPlayerFactory(last_seen_at='2021-01-02 00:00:00', first_seen_at='2021-01-01 00:00:00')

    def test_player_is_online(self):
        self.assertTrue(self.player.is_online)

    def test_player_is_offline(self):
        self.player = PalworldPlayerFactory(last_seen_at='2021-01-01 00:00:00', first_seen_at='2021-01-01 00:00:00')
