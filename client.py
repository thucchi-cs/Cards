import socket

def base36_to_int(code: str) -> int:
    return int(code, 36)

def int_to_ip(num: int) -> str:
    return '.'.join(str((num >> (8 * i)) & 0xFF) for i in reversed(range(4)))

def decode_join_code(code: str) -> str:
    return int_to_ip(base36_to_int(code.strip().upper()))


join_code = input("Enter join code to connect: ").strip()
server_ip = decode_join_code(join_code)

port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((server_ip, port))
except Exception as e:
    print(f"❌ Could not connect to server at {server_ip}:{port}. Error: {e}")
    exit()

while True:
    data = s.recv(1024).decode()
    if data:
        print(data, end='')
        if "Enter" in data:
            user_input = input()
            s.send(user_input.encode())
