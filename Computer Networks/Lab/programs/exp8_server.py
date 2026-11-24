# Experiment 8 - Client to client through the server, with encryption (server side)
# clients encrypt before sending, so the server only ever sees cipher text

import socket
import threading

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5003
clients = {}


def forward(sender, text):
    for sock in list(clients):
        if sock is not sender:
            sock.send(text.encode())


def handle(conn):
    user = conn.recv(1024).decode()
    clients[conn] = user
    print(f"{user} joined ({len(clients)} online)")
    while True:
        try:
            msg = conn.recv(1024).decode()
        except OSError:
            break
        if not msg or msg == "bye":
            break
        # server can't read it, it just passes the cipher text along
        print(f"relaying from {user} (encrypted): {msg}")
        forward(conn, f"{user}|{msg}")
    del clients[conn]
    print(f"{user} left")
    conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)
print("\nSecure relay server running on port", PORT)

while True:
    conn, addr = s.accept()
    print("connection from", addr)
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
