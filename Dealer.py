import Deck
import Player
import Card

class Dealer:
    def __init__(self):
        self.deck = None
        self.cards = []
        self.score = 0
        self.players = []
        self.is_ready = False

    def clear_dealer(self):
        self.deck = None
        self.cards = []
        self.score = 0
        self.players = []
        self.is_ready = False

    def new_deck(self):
        self.deck = Deck.Deck()
        self.deck.shuffle()

    def deal_cards(self):
        for player in self.players:
            for _ in range(0,2):
                self.deal_one_card(player)
        for _ in range(0,2):
            self.cards.append(self.deck.get_card())

    def deal_one_card(self,player):
        player.add_card(self.deck.get_card())

    def calculate_score(self):
        self.score = 0
        temp_score = 0
        for card in self.cards:
            self.score += card.value
            if card.value == 11:
                temp_score += 1
            else:
                temp_score += card.value
        if self.score > 21 and temp_score < 22:
            self.score = temp_score

    def hit(self):
        self.calculate_score()
        if self.score >= 21:
            return False
        if self.score < 17:
            self.cards.append(self.deck.get_card())
            self.hit()
        self.is_ready = True

    def pay_player(self):
        for player in self.players:
            player.calculate_score()
            if player.score > self.score and player.score <= 21:
                player.money += 2*player.bet_value
            elif player.score == self.score and player.score <= 21:
                player.money += player.bet_value
            elif player.score <= 21 and self.score > 21:
                player.money += 2*player.bet_value
            print(self.score)
            print(player.score)