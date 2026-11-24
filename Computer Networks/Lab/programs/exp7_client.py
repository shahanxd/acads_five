# Experiment 7 - One client talks to another client through the server (client side)
# run two of these; whatever one types reaches the other via the server

import socket
import threading

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5002


def receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
        except OSError:
            break
        if not data:
            break
        print(data)


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))
user = input("\nEnter your name: ")
c.send(user.encode())
print("Connected. Start typing (bye to leave)")

threading.Thread(target=receive, args=(c,), daemon=True).start()

while True:
    msg = input()
    c.send(msg.encode())
    if msg.lower() == "bye":
        break

c.close()
