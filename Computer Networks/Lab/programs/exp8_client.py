# Experiment 8 - Client to client through the server, with encryption (client side)
# uses caesar cipher (exp 1) with a shared key; both clients must use the same key

import socket
import threading

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)

HOST, PORT = "127.0.0.1", 5003
KEY = 3


def encrypt(text, key):
    out = ""
    for ch in text:
        if ch.isupper():
            out += chr((ord(ch) - 65 + key) % 26 + 65)
        elif ch.islower():
            out += chr((ord(ch) - 97 + key) % 26 + 97)
        else:
            out += ch
    return out


def decrypt(text, key):
    return encrypt(text, -key)


def receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
        except OSError:
            break
        if not data:
            break
        sender, cipher = data.split("|", 1)
        print(f"  received from {sender} (encrypted): {cipher}")
        print(f"  decrypted: {decrypt(cipher, KEY)}")


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))
user = input("\nEnter your name: ")
c.send(user.encode())
print("Connected, shared key =", KEY, "(bye to leave)")

threading.Thread(target=receive, args=(c,), daemon=True).start()

while True:
    msg = input()
    if msg.lower() == "bye":
        c.send(b"bye")
        break
    cipher = encrypt(msg, KEY)
    print("  sent (encrypted):", cipher)
    c.send(cipher.encode())

c.close()
