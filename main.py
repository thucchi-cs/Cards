import pygame
from board import Board

# Screen setup
WIDTH = 1200
HEIGHT = 700

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cards")

# Frames timing
FPS = 60

# Time
clock = pygame.time.Clock()

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

    pygame.display.flip()
