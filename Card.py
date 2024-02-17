class Card:
    def __init__(self, name, value):
        if not isinstance(value, int):
            raise TypeError("Card value must be an integer.")
        self.name = name
        self.value = value