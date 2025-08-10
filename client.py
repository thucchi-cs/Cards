import socket
import pygame
import threading

# Network functions (decode join code, same as before)
def base36_to_int(code: str) -> int:
    return int(code, 36)

def int_to_ip(num: int) -> str:
    return '.'.join(str((num >> (8 * i)) & 0xFF) for i in reversed(range(4)))

def decode_join_code(code: str) -> str:
    return int_to_ip(base36_to_int(code.strip().upper()))

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        sock.sendall(input_text.encode())
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill((30, 30, 30))

        # Render messages
        y = 10
        for msg in messages:
            msg_surface = font.render(msg, True, (255, 255, 255))
            screen.blit(msg_surface, (20, y))
            y += 22

        # Render input box
        pygame.draw.rect(screen, (50, 50, 50), input_box)
        txt_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        clock.tick(30)

    sock.close()
    pygame.quit()

if __name__ == "__main__":
    main()
