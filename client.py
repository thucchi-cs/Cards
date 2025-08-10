import socket

# Ask user for server IP and do NOT connect before this input
server_ip = input("Enter server IP to connect to: ").strip()

port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((server_ip, port))
except Exception as e:
    print(f"Could not connect to server at {server_ip}:{port}. Error: {e}")
    exit()

while True:
    data = s.recv(1024).decode()
    if data:
        print(data, end='')
        if "Enter" in data:
            user_input = input()
            s.send(user_input.encode())
