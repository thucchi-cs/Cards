import pygame
import socket
import threading
from _thread import start_new_thread
from board import Board  # Your Board module, assumed to exist
import json, time

# ------------------------ Server utilities ------------------------

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


clients = []  # store all connected clients
game_state = {
    "player_positions": {},  # example variable to share
    "turn": 1
}

def broadcast(data, exclude=None):
    """Send data to all connected clients, except one if exclude is set."""
    for c in clients:
        if c != exclude:
            try:
                c.sendall(json.dumps(data).encode())
            except:
                pass

def client_thread(conn, player_id):
    clients.append(conn)
    conn.sendall(f"You are Player {player_id}\n".encode())

    if player_id == 1:
        success = initialize_game_from_player(conn)
        if not success:
            clients.remove(conn)
            return

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            try:
                # Expecting JSON from clients
                packet = json.loads(data)
                print(f"Player {player_id} sent: {packet}")

                # Update server game state
                if "position" in packet:
                    game_state["player_positions"][player_id] = packet["position"]

                # Send updated game state to all players
                broadcast({"type": "update_state", "state": game_state}, exclude=conn)

            except json.JSONDecodeError:
                print(f"Invalid JSON from Player {player_id}: {data}")

        except:
            break

    conn.close()
    clients.remove(conn)


# ------------------------ Server Thread ------------------------

server_running = True  # global flag to control server loop

def server_loop():
    global server_running

    server_ip = get_local_ip()
    join_code = encode_ip(server_ip)
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Add this line
    s.bind((server_ip, port))
    s.listen(5)

    print("\n🎮 Server is running!")
    print(f"🔗 Join code: {join_code}")
    print(f"(This maps to IP: {server_ip})")
    print("Waiting for players to connect...\n")

    player_id = 1

    s.settimeout(1.0)  # 1 second timeout to allow clean shutdown checking

    while server_running:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue  # check server_running flag again

        if Board.player_num > 0 and player_id > Board.player_num:
            conn.sendall(b"Game is full. Try again later.\n")
            conn.close()
            print(f"Connection from {addr} rejected: game full.")
            continue

        print(f"Player {player_id} connected from {addr}")
        start_new_thread(client_thread, (conn, player_id))
        player_id += 1
        time.sleep(0.05)

    s.close()
    print("Server stopped.")

if __name__ == "__main__":
    server_loop()