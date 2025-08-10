import pygame
from cards import Card
from users import User

class Board():
    cards = Card.generate_cards()
    house = User(cards)
    player_num = 0 # get user input
    cards_per_player = 0 # get user input

    def pass_cards():
        pass

    def reset():
        pass