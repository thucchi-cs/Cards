import socket
import pygame
import threading
import json
import threading
from board import Board

# Network functions (decode join code, same as before)
def base36_to_int(code: str) -> int:
    return int(code, 36)

def int_to_ip(num: int) -> str:
    return '.'.join(str((num >> (8 * i)) & 0xFF) for i in reversed(range(4)))

def decode_join_code(code: str) -> str:
    return int_to_ip(base36_to_int(code.strip().upper()))

def listen_for_updates(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            try:
                # Try parsing as JSON
                packet = json.loads(data)
                if packet.get("type") == "update_state":
                    print("\n📡 Game state updated:", packet["state"])
            except json.JSONDecodeError:
                # Otherwise just treat it as plain text
                print(data, end='')
        except:
            break
# Pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client Game Window")

font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# Input box and message display
input_box = pygame.Rect(20, HEIGHT - 40, WIDTH - 40, 30)
input_text = ''
messages = []

def add_message(text):
    messages.append(text)
    if len(messages) > 15:
        messages.pop(0)

# Thread to listen for server messages
def listen_to_server(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                add_message("[Disconnected from server]")
                break
            add_message(data.strip())
        except:
            add_message("[Connection lost]")
            break

# ------------------------ Pygame setup ------------------------

WIDTH = 1200
HEIGHT = 700

pygame.init()
pygame.font.init()
font = pygame.font.Font("./assets/fonts/Orbitron-Medium.ttf", 26)

pygame.font.init()
font = pygame.font.Font("./assets/fonts/Orbitron-Medium.ttf", 26)
cardCount = font.render("hey", True, "white")

bg = pygame.image.load("./assets/graphics/felt.jpg")

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

print("\nHouse")
for card in Board.house.hand:
    print(card, end="  ")

print("\nplayer")
for card in Board.users[0].hand:
    print(card, end="  ")


def main():
    global input_text

    join_code = input("Enter join code to connect: ").strip()
    server_ip = decode_join_code(join_code)
    port = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, port))
    except Exception as e:
        print(f"Could not connect: {e}")
        return

    threading.Thread(target=listen_to_server, args=(sock,), daemon=True).start()


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
        print("game exited cleanly")

    pygame.quit()

if __name__ == "__main__":
    main()
