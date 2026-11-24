# Experiment 6 - One server, multiple clients (client side)
# open this in 2-3 terminals at once

import socket

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5001

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))
print("\nConnected to server, type bye to exit")

while True:
    msg = input("You: ")
    c.send(msg.encode())
    if msg.lower() == "bye":
        break
    print("Server:", c.recv(1024).decode())

c.close()
print("Disconnected")
