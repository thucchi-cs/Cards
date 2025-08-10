import pygame

class Card(pygame.sprite.Sprite):
    suits = ["spade", "heart", "diamond", "club"]
    suits_images = {
        "spade": "assets/graphics/spade.png",
        "heart": "assets/graphics/heart.png",
        "diamond": "assets/graphics/diamond.png",
        "club": "assets/graphics/club.png"
    }
    
    def __init__(self, suit: str, value: int):
        super().__init__()

        self.suit = suit
        self.value = value
        self.image = pygame.image.load(Card.suits_images[self.suit])
        self.image = pygame.transform.scale(self.image, (200,280))
        self.rect = self.image.get_rect()

    def generate_cards():
        cards = []
        for s in Card.suits:
            for val in range(1, 14):
                cards.append(Card(s, val))

        return cards

    def __str__(self):
        return str(self.value) + " " + self.suit 
    
    def shuffle_cards():
        pass
