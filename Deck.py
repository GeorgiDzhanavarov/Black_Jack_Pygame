import Card
import random

class Deck:
    def __init__(self):
        suits = ["diamonds", "clubs", "hearts", "spades"]
        self.deck = []

        for suit in suits:
            for number in range(2,15):
                if number > 10 and number < 14:
                    value = 10
                elif number == 14:
                    value = 11
                else:
                    value = number     
                self.deck.append(Card.Card(f'{number}_of_{suit}',value))

    def shuffle(self):
        random.shuffle(self.deck)

    def get_card(self):
        card = self.deck.pop(0)
        return card

        


