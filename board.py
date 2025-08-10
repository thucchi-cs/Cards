import pygame
from cards import Card
from users import User

class Board():
	cards = Card.generate_cards()
	house = User(cards)
	users = []
	player_num = 0 # get user input
	cards_per_player = 0 # get user input

	def dealCards(to: User, count: int):
		to.cards.append(Board.house.cards.pop(count))

	def reset():
		Board.house = User(Board.cards)
		Board.cards = Card.generate_cards()
		Board.users = []
