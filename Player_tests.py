import unittest
from Player import Player
from Card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(100, None)  

    def test_initialization(self):
        self.assertEqual(self.player.money, 100)
        self.assertIsNone(self.player.socket)
        self.assertEqual(len(self.player.cards), 0)
        self.assertEqual(self.player.score, 0)
        self.assertFalse(self.player.is_ready)
        self.assertIsNone(self.player.bet_value)

    def test_add_card(self):
        card = Card("Ace", 11)
        self.player.add_card(card)
        self.assertEqual(len(self.player.cards), 1)
        self.assertEqual(self.player.cards[0], card)

    def test_clear_player(self):
        self.player.add_card(Card("Ace", 11))
        self.player.score = 21
        self.player.is_ready = True
        self.player.bet_value = 10
        self.player.clear_player()
        self.assertEqual(len(self.player.cards), 0)
        self.assertEqual(self.player.score, 0)
        self.assertFalse(self.player.is_ready)
        self.assertIsNone(self.player.bet_value)

    def test_calculate_score(self):
        self.player.add_card(Card("Ace", 11))
        self.player.add_card(Card("King", 10))
        self.player.calculate_score()
        self.assertEqual(self.player.score, 21)

    def test_bet(self):
        self.assertTrue(self.player.bet(50))
        self.assertEqual(self.player.money, 50)
        self.assertEqual(self.player.bet_value, 50)

    def test_hit_option(self):
        self.player.add_card(Card("Ace", 11))
        self.player.add_card(Card("King", 10))
        self.assertEqual(self.player.hit_option(), False)

    def test_stay_option(self):
        self.player.stay_option()
        self.assertTrue(self.player.is_ready)

    def test_double_option(self):
        self.player.money = 100
        self.player.bet_value = 10
        self.assertTrue(self.player.double_option())
        self.assertEqual(self.player.bet_value, 20)
        self.assertEqual(self.player.money, 90)

if __name__ == '__main__':
    unittest.main()