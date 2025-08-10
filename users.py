import pygame
from cards import Card
import uuid, time
from random import shuffle

class User():
    player_count = 0
    id: uuid = uuid.uuid4()

    def __init__(self, hand: list=[]):
        super().__init__()

        User.player_count += 1
        self.id = User.player_count
        self.hand = pygame.sprite.Group(hand)
        self.onTurn = False

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

    def shuffleHand(self):
        hand = self.hand.sprites()
        shuffle(hand)
        self.hand.empty()
        self.hand.add(hand)

    def getCardCount(self):
        return len(self.hand)
    
    def update(self, board):
        if self.onTurn:
            for c in self.hand:
                c.show = True
                if c.clicked():
                    self.play_card(board.playing, c)
                    time.sleep(0.3)
            if len(board.house.hand) > 0:
                c = board.house.hand.sprites()[0]
                if c.clicked():
                    self.take_card(board.house, c)
                    time.sleep(0.3)
