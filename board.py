import pygame
from cards import Card
from users import User

class Board():
    cards = Card.generate_cards()
    house = User(cards)
    users = []
    player_num = 3 # get user input
    cards_per_player = 7 # get user input

    def dealCards(to: User, count: int):
        cards = Board.house.hand.sprites()[:count]
        to.take_card(Board.house, cards)

    def reset():
        Board.house = User(Board.cards)
        Board.cards = Card.generate_cards()
        Board.users = []

    def add_player():
        Board.users.append(User())
        Board.dealCards(Board.users[-1], Board.cards_per_player)
