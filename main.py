import pygame
from board import Board

# Screen setup
WIDTH = 1200
HEIGHT = 700

pygame.font.init()
font = pygame.font.Font("./assets/fonts/Orbitron-Medium.ttf", 26)
cardCount = font.render("hey", True, "white")

bg = pygame.image.load("./assets/graphics/felt.jpg")

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cards")

# Frames timing
FPS = 60

# Time
clock = pygame.time.Clock()

Board.house.shufleHand()

for card in Board.house.hand:
    print(card, end="  ")

player = Board.add_player()
player2 = Board.add_player()

print("\nHouse")
for card in Board.house.hand:
    print(card, end="  ")

print("\nplayer")
for card in Board.users[0].hand:
    print(card, end="  ")

# Runner variable
run = True
while run:
    # Update fps
    clock.tick(FPS)

    for event in pygame.event.get():
        # Check to close game
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    # Draw on screen
    SCREEN.fill((0,0,0))

    SCREEN.blit(bg, (0,0))

    cardCount = player.getCardCount()
    cardCount = font.render(f"You have {str(cardCount)} card{"" if cardCount == 1 else "s"}", True, "white")
    SCREEN.blit(cardCount, (0,0))

    pygame.display.flip()
