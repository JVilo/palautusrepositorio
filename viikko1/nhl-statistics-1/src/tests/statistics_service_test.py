import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_whit_name(self):
        player = self.stats.search("Kurri")
        
        self.assertEqual(str(player), "Kurri EDM 37 + 53 = 90")

    def test_search_whit_wrong_name(self):
        player = self.stats.search("Grönlund")
        self.assertEqual(player, None)

    
    def test_top_points(self):
        player = self.stats.top(1)
        for p in player:
            player = p
        self.assertEqual(str(player), "Lemieux PIT 45 + 54 = 99")
        

    def test_team(self):
        player = self.stats.team("PIT")
        for p in player:
            player = p
        self.assertEqual("Lemieux PIT 45 + 54 = 99",str(player))