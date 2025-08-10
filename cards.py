import pygame
from random import *

class Card(pygame.sprite.Sprite):
    suits = ["spade", "club", "heart", "diamond"]
    suits_images = {
        "spade": "assets/graphics/spade.png",
        "heart": "assets/graphics/heart.png",
        "diamond": "assets/graphics/diamond.png",
        "club": "assets/graphics/club.png"
    }

    def __init__(self, suit: str, value: int, font):
        super().__init__()

        self.suit = suit
        self.value = value
        self.image = pygame.image.load(Card.suits_images[self.suit])
        self.image = pygame.transform.scale(self.image, (50,70))
        self.back = pygame.image.load("assets/graphics/back.png")
        self.back = pygame.transform.scale(self.back, (50,70))
        self.rect = self.image.get_rect()
        self.rect.topleft = (575, 50)
        self.font = font
        self.num = self.font.render(str(self.value), True, "red" if Card.suits.index(suit) >1 else "black")
        self.show = False

    def generate_cards(font):
        cards = []
        for s in Card.suits:
            for val in range(1, 14):
                cards.append(Card(s, val, font))

        return cards

    def __str__(self):
        return str(self.value) + " " + self.suit

    def draw(self, screen):
        if self.show:
            screen.blit(self.image, self.rect.topleft)
            screen.blit(self.num, self.rect.topleft)
        else:
            screen.blit(self.back, self.rect.topleft)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos):
            return True
        return False
