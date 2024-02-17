import unittest
from Deck import Deck

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_creation(self):
        self.assertEqual(len(self.deck.deck), 52)

    def test_shuffle_deck(self):
        initial_order = self.deck.deck[:]
        self.deck.shuffle()
        shuffled_order = self.deck.deck
        self.assertNotEqual(initial_order, shuffled_order)

    def test_get_card(self):
        card = self.deck.get_card()
        self.assertIsNotNone(card)
        self.assertEqual(len(self.deck.deck), 51)

if __name__ == '__main__':
    unittest.main()