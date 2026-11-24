# Experiment 5 - Two processes interacting with each other (server side)
# run this first, then exp5_client.py in another terminal

import socket

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print("\nServer process started, waiting on port", PORT)

conn, addr = s.accept()
print("Connected to process at", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print("Client:", data)
    if data.lower() == "bye":
        break
    reply = input("Server: ")
    conn.send(reply.encode())
    if reply.lower() == "bye":
        break

conn.close()
s.close()
print("Connection closed")
