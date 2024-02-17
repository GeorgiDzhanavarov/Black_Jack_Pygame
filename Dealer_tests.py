import unittest
from Dealer import Dealer
from Deck import Deck
from Player import Player

class TestDealer(unittest.TestCase):
    def setUp(self):
        self.dealer = Dealer()

    def test_initialization(self):
        self.assertIsNone(self.dealer.deck)
        self.assertEqual(len(self.dealer.cards), 0)
        self.assertEqual(self.dealer.score, 0)
        self.assertEqual(len(self.dealer.players), 0)
        self.assertFalse(self.dealer.is_ready)

    def test_clear_dealer(self):
        self.dealer.deck = Deck()
        self.dealer.cards = [1, 2, 3]
        self.dealer.score = 21
        self.dealer.players = [Player(100, None)]
        self.dealer.is_ready = True

        self.dealer.clear_dealer()

        self.assertIsNone(self.dealer.deck)
        self.assertEqual(len(self.dealer.cards), 0)
        self.assertEqual(self.dealer.score, 0)
        self.assertEqual(len(self.dealer.players), 0)
        self.assertFalse(self.dealer.is_ready)

    def test_new_deck(self):
        self.dealer.new_deck()
        self.assertIsNotNone(self.dealer.deck)
        self.assertEqual(len(self.dealer.deck.deck), 52)

    def test_deal_cards(self):
        player1 = Player(100, None)
        player2 = Player(200, None)
        self.dealer.players = [player1, player2]
        self.dealer.new_deck()
        self.dealer.deal_cards()

        self.assertEqual(len(player1.cards), 2)
        self.assertEqual(len(player2.cards), 2)
        self.assertEqual(len(self.dealer.cards), 2)

    def test_deal_one_card(self):
        player = Player(100, None)
        self.dealer.players = [player]
        self.dealer.new_deck()
        self.dealer.deal_one_card(player)

        self.assertEqual(len(player.cards), 1)
        self.assertEqual(len(self.dealer.deck.deck), 51)

if __name__ == '__main__':
    unittest.main()