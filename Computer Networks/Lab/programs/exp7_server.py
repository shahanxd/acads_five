# Experiment 7 - One client talks to another client through the server (server side)
# server just receives a message from one client and forwards it to the other

import socket
import threading

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5002
clients = {}          # socket -> username


def forward(sender, text):
    for sock in list(clients):
        if sock is not sender:
            sock.send(text.encode())


def handle(conn):
    user = conn.recv(1024).decode()
    clients[conn] = user
    print(f"{user} joined ({len(clients)} online)")
    forward(conn, f"* {user} joined the chat")
    while True:
        try:
            msg = conn.recv(1024).decode()
        except OSError:
            break
        if not msg or msg.lower() == "bye":
            break
        print(f"forwarding {user} -> others : {msg}")
        forward(conn, f"{user}: {msg}")
    del clients[conn]
    forward(conn, f"* {user} left the chat")
    print(f"{user} left")
    conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)
print("\nRelay server running on port", PORT)

while True:
    conn, addr = s.accept()
    print("connection from", addr)
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
