import pygame

class Card(pygame.sprite.Sprite):
    suits = ["spade", "heart", "diamond", "club"]
    
    def __init__(self, suit: str, value: int):
        super().__init__()

        self.suit = suit
        self.value = value


    def generate_cards():
        cards = []
        for s in Card.suits:
            for val in range(1, 14):
                cards.append(Card(s, val))

        return cards

    def shuffle_cards():
        pass