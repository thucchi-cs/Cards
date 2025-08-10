import pygame
from board import Board
import time

# ------------------------ Pygame setup ------------------------

WIDTH = 1200
HEIGHT = 700

pygame.init()
pygame.font.init()
font = pygame.font.Font("./assets/fonts/Orbitron-Medium.ttf", 26)

cardCount = font.render("hey", True, "white")

bg = pygame.image.load("./assets/graphics/felt.jpg")
button = pygame.image.load("./assets/graphics/button.png")
btnRect = button.get_rect()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cards")

FPS = 60
clock = pygame.time.Clock()

# Your game initialization
Board.house.shuffleHand()

for card in Board.house.hand:
    print(card, end="  ")

player = Board.add_player()
player2 = Board.add_player()
player3 = Board.add_player()

print("\nHouse")
for card in Board.house.hand:
    print(card, end="  ")

print("\nplayer")
for card in Board.users[0].hand:
    print(card, end="  ")

counter = 0 
for c in player.hand:
    c.rect.topleft = (400+counter*70, 550)
    counter += 1

counter = 0 
for c in player2.hand:
    c.rect.topleft = (1140, 50+counter*90)
    counter += 1

counter = 0 
for c in player3.hand:
    c.rect.topleft = (10, 50+counter*90)
    counter += 1
player.onTurn = True


def clicked(button, curplayer):
    pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and button.collidepoint(pos):
        curUser = Board.users.index(curplayer)
        nextUser = (curUser + 1) % len(Board.users)
        time.sleep(0.3)
        for user in Board.users:
            user.onTurn = False
        Board.users[nextUser].onTurn = True
        print(Board.users[nextUser].id)
        return True
    return False

def clicked(button, curplayer):
    pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and button.collidepoint(pos):
        curUser = Board.users.index(curplayer)
        nextUser = (curUser + 1) % len(Board.users)
        time.sleep(0.3)
        for user in Board.users:
            user.onTurn = False
        Board.users[nextUser].onTurn = True
        print(Board.users[nextUser].id)
        return True
    return False

def main():
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

        counter = 0 
        for c in player.hand:
            c.rect.topleft = (400+counter*70, 550)
            counter += 1

        counter = 0 
        for c in player2.hand:
            c.rect.topleft = (1140, 50+counter*90)
            counter += 1

        counter = 0 
        for c in player3.hand:
            c.rect.topleft = (10, 50+counter*90)
            counter += 1

        # Draw on screen
        SCREEN.fill((0,0,0))

        SCREEN.blit(bg, (0,0))
        SCREEN.blit(button, (100, 100))
        for c in Board.playing.hand:
            c.draw(SCREEN)
            if c.clicked():
                Board.playing.play_card(Board.discard, Board.playing.hand)
        for p in Board.users:
            p.update(Board)
            if p.onTurn:
                curplayer = p
                clicked(btnRect, curplayer)
            for c in p.hand:
                c.draw(SCREEN)


        for c in Board.house.hand:
            c.draw(SCREEN)

        for c in Board.playing.hand:
            c.rect.topleft = (575, 300)

        cardCount = curplayer.getCardCount()
        cardCount = font.render(f"You have {str(cardCount)} card{"" if cardCount == 1 else "s"}", True, "white")
        SCREEN.blit(cardCount, (0,0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()