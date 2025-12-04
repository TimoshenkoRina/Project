import random


SUITS = ['буби', 'черви', 'крести', 'пики']

RANKS_52 = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

RANKS_36 = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    """склеиваем карту из масти и величины"""
    def __init__(self, rank, suit, value=0):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'{self.rank} {self.suit}'

    def __str__(self):
        return f"{self.rank} {self.suit}"

class Deck:
    def __init__(self, size=52):
        """создаем колоду под нужный размер"""
        self.cards = []

        # Выбираем нужный набор в зависимости от размера
        if size == 36:
            ranks = RANKS_36
        else:
            ranks = RANKS_52

        # Генерация карт
        for suit in SUITS:
            for rank in ranks:
                self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        """перемешиваем колоду"""
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)
