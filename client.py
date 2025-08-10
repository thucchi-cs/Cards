import socket
import json
import threading

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

join_code = input("Enter join code to connect: ").strip()
server_ip = decode_join_code(join_code)

port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((server_ip, port))
except Exception as e:
    print(f"❌ Could not connect to server at {server_ip}:{port}. Error: {e}")
    exit()

# Start listener thread
threading.Thread(target=listen_for_updates, args=(s,), daemon=True).start()

while True:
    # For now, just allow manual input
    msg = input()
    try:
        # If user types JSON-like, send as JSON
        if msg.startswith("{") and msg.endswith("}"):
            s.send(msg.encode())
        else:
            s.send(msg.encode())
    except:
        break
