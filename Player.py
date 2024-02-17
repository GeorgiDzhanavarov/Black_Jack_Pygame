class Player:
    def __init__(self, money, socket):
        self.money = money
        self.socket = socket
        self.cards = []
        self.score = 0
        self.is_ready = False
        self.bet_value = None

    def add_card(self, card):
        self.cards.append(card)

    def clear_player(self):
        self.cards = []
        self.score = 0
        self.is_ready = False
        self.bet_value = None

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

    def bet(self, value):
        if self.money < value:
            return False   
        self.bet_value = value
        self.money -= value
        return True
    
    def hit_option(self):
        self.calculate_score()
        if self.score >= 21:
            return False
        else:
            return True    

    def stay_option(self):
        self.is_ready = True

    def double_option(self):
        if self.money < self.bet_value:
            return False
        self.money -= self.bet_value
        self.bet_value *= 2
        return True


