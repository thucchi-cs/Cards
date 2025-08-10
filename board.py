import pygame
from cards import Card
from users import User

class Board():
	cards = Card.generate_cards()
	house = User(cards)
	users = []
	player_num = 0 # get user input
	cards_per_player = 0 # get user input

	def dealCards(to: User, count: Int):
		to.cards.append(house.cards.pop(count))

	def reset():
		house = User(cards)
		cards = Card.generate_cards()
		users = []
