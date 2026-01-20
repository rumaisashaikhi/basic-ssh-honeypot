import socket
from datetime import datetime

def recv_line(client):
    data = b""
    while not data.endswith(b"\n"):
        chunk = client.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()

HOST = "0.0.0.0"
PORT = 2222

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print("[+] Honeypot running on port 2222...")

while True:
    client, addr = sock.accept()
    print(f"[!] Connection from {addr[0]}")

    client.sendall(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
    client.sendall(b"Username: ")
    username = recv_line(client)

    client.sendall(b"Password: ")
    password = recv_line(client)

    with open("logs.txt", "a") as log:
        log.write(
            f"{datetime.now()} | IP: {addr[0]} | User: {username} | Pass: {password}\n"
        )

    client.sendall(b"\r\nLogin failed!\r\n")
    client.close()

