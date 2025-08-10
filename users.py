import pygame
from cards import Card

class User():
    player_count = 0

    def __init__(self, hand: list):
        super().__init__()

        User.player_count += 1
        self.id = User.player_count
        self.hand = hand

    def play_card(self, to: "User", card: Card):
        pass

    def take_card(self, _from: "User", card: Card):
        pass

    def add_card(self, card: Card):
        pass

    def remove_card(self, card: Card):
        pass

    def shufleHand():
        shuffle(cards)
