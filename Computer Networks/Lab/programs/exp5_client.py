# Experiment 5 - Two processes interacting with each other (client side)

import socket

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5000

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))
print("\nConnected to server process on port", PORT)

while True:
    msg = input("Client: ")
    c.send(msg.encode())
    if msg.lower() == "bye":
        break
    data = c.recv(1024).decode()
    if not data:
        break
    print("Server:", data)
    if data.lower() == "bye":
        break

c.close()
print("Connection closed")
