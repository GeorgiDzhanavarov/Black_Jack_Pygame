import unittest
from Card import Card

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card("Ace", 14)
        self.assertEqual(card.name, "Ace")
        self.assertEqual(card.value, 14)

    def test_card_name_and_value(self):
        card = Card("King", 13)
        self.assertEqual(card.name, "King")
        self.assertEqual(card.value, 13)

    def test_card_with_negative_value(self):
        card = Card("Negative", -5)
        self.assertEqual(card.name, "Negative")
        self.assertEqual(card.value, -5)

    def test_card_with_zero_value(self):
        card = Card("Zero", 0)
        self.assertEqual(card.name, "Zero")
        self.assertEqual(card.value, 0)

    def test_card_with_string_value(self):
        with self.assertRaises(TypeError):
            card = Card("Invalid", "value")


if __name__ == '__main__':
    unittest.main()