import socket
from _thread import start_new_thread
from board import Board

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def ip_to_int(ip: str) -> int:
    parts = list(map(int, ip.split('.')))
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def int_to_base36(num: int) -> str:
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while num > 0:
        result = chars[num % 36] + result
        num //= 36
    return result or '0'

def encode_ip(ip: str) -> str:
    return int_to_base36(ip_to_int(ip))


def initialize_game_from_player(conn):
    try:
        conn.sendall(b"Enter number of players: ")
        player_num = conn.recv(1024).decode().strip()

        if not player_num.isdigit():
            conn.sendall(b"Invalid input. Disconnecting.\n")
            conn.close()
            return False

        conn.sendall(b"Enter number of cards per player: ")
        cards = conn.recv(1024).decode().strip()

        if not cards.isdigit():
            conn.sendall(b"Invalid input. Disconnecting.\n")
            conn.close()
            return False

        Board.player_num = int(player_num)
        Board.cards_per_player = int(cards)

        conn.sendall(b"Game setup received.\n")
        print(f"SETUP COMPLETE: {Board.player_num} players, {Board.cards_per_player} cards each.")
        return True
    except Exception as e:
        print("Error:", e)
        return False


def client_thread(conn, player_id):
    conn.sendall(f"You are Player {player_id}\n".encode())

    if player_id == 1:
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
    join_code = encode_ip(server_ip)
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, port))
    s.listen(5)

    print("\n🎮 Server is running!")
    print(f"🔗 Join code: {join_code}")
    print(f"(This maps to IP: {server_ip})")
    print("Waiting for players to connect...\n")

    player_id = 1
    while True:
        conn, addr = s.accept()

        if Board.player_num > 0 and player_id > Board.player_num:
            conn.sendall(b"Game is full. Try again later.\n")
            conn.close()
            print(f"Connection from {addr} rejected: game full.")
            continue

        print(f"Player {player_id} connected from {addr}")
        start_new_thread(client_thread, (conn, player_id))
        player_id += 1