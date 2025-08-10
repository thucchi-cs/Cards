import pygame
from cards import Card
import uuid
from random import shuffle

class User():
    player_count = 0
    id: uuid = uuid.uuid4()

    def __init__(self, hand: list=[]):
        super().__init__()

        User.player_count += 1
        self.id = User.player_count
        self.hand = pygame.sprite.Group(hand)

    def play_card(self, to: "User", card: Card):
        self.remove_card(card)
        to.add_card(card)

    def take_card(self, _from: "User", card: Card):
        self.add_card(card)
        _from.remove_card(card)

    def add_card(self, card: Card):
        self.hand.add(card)
    
    def remove_card(self, card: Card):
        self.hand.remove(card)

    def shufleHand(self):
        hand = self.hand.sprites()
        shuffle(hand)
        self.hand.empty()
        self.hand.add(hand)
