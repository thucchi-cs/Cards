import pygame
from cards import Card
from users import User

class Board():
    cards = []
    house = None
    discard = None
    users = []

    # Will be set by server.py
    player_num = 0
    cards_per_player = 0

    def dealCards(cls, to: User, count: int):
        cards = cls.house.hand.sprites()[:count]
        to.take_card(cls.house, cards)

    def reset(cls):
        cls.cards = Card.generate_cards()
        cls.house = User(cls.cards)
        cls.discard = User(cls.cards)
        cls.users = []

    def add_player(cls):
        player = User()
        cls.users.append(player)
        cls.dealCards(player, cls.cards_per_player)
