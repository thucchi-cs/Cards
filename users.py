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
        self.remove_card(card)
        to.add_card(card)

    def take_card(self, _from: "User", card: Card):
        self.add_card(card)
        _from.remove_card(card)

    def add_card(self, card: Card):
        self.hand.append(card)
    
    def remove_card(self, card: Card):
        self.hand.remove(card)
