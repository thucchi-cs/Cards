import socket
from _thread import start_new_thread

class Board:
    player_num = 0
    cards_per_player = 0

def get_local_ip():
    # This trick gets your local IP even if you have multiple interfaces
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect to an external IP, doesn't send data but picks the right interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def initialize_game_from_player(conn):
    try:
        conn.sendall(b"Enter number of players: ")
        player_num = conn.recv(1024).decode().strip()

        if not player_num.isdigit():
            conn.sendall(b"Invalid input. Disconnecting.\n")
            conn.close()
            return False

        Board.player_num = int(player_num)

        conn.sendall(b"Enter number of cards per player: ")
        cards = conn.recv(1024).decode().strip()

        if not cards.isdigit():
            conn.sendall(b"Invalid input. Disconnecting.\n")
            conn.close()
            return False

        Board.cards_per_player = int(cards)

        conn.sendall(b"Game initialized successfully.\n")
        print(f"SETUP COMPLETE: {Board.player_num} players, {Board.cards_per_player} cards each.")
        return True
    except Exception as e:
        print("Error:", e)
        return False

def client_thread(conn, player_id):
    conn.sendall(f"You are Player {player_id}\n".encode())

    if player_id == 0:
        success = initialize_game_from_player(conn)
        if not success:
            return

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Player {player_id} says: {data}")
        except:
            break

    conn.close()

if __name__ == "__main__":
    server_ip = get_local_ip()
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, port))
    s.listen(5)

    print(f"Server is running on IP: {server_ip}, port: {port}")
    print("Waiting for players to connect...")

    player_id = 0
    while True:
        conn, addr = s.accept()
        print(f"Player {player_id} connected from {addr}")
        start_new_thread(client_thread, (conn, player_id))
        player_id += 1
