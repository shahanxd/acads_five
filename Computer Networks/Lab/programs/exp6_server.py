# Experiment 6 - One server, multiple clients (server side)
# every client gets its own thread, so many clients can talk at the same time

import socket
import threading

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5001
count = 0
lock = threading.Lock()


def handle(conn, addr, cid):
    print(f"[client {cid}] connected from {addr}, active clients: {threading.active_count() - 1}")
    while True:
        data = conn.recv(1024).decode()
        if not data or data.lower() == "bye":
            break
        print(f"[client {cid}] says: {data}")
        conn.send(f"server got your message '{data}' ({len(data)} chars)".encode())
    conn.close()
    print(f"[client {cid}] disconnected")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print("\nServer listening on port", PORT)

while True:
    conn, addr = s.accept()
    with lock:
        count += 1
        cid = count
    threading.Thread(target=handle, args=(conn, addr, cid), daemon=True).start()
