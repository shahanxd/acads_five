# Experiment 3 - Columnar Transposition Cipher

import math

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)


def key_order(key):
    # column read order = alphabetical order of key letters
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def encrypt(text, key):
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    text = text + "_" * (rows * cols - len(text))   # pad with _
    grid = [text[i * cols:(i + 1) * cols] for i in range(rows)]

    print("\n  " + "  ".join(key))
    for row in grid:
        print("  " + "  ".join(row))

    cipher = ""
    for c in key_order(key):
        for r in range(rows):
            cipher += grid[r][c]
    return cipher


def decrypt(cipher, key):
    cols = len(key)
    rows = len(cipher) // cols
    grid = [[""] * cols for _ in range(rows)]
    pos = 0
    for c in key_order(key):
        for r in range(rows):
            grid[r][c] = cipher[pos]
            pos += 1
    plain = "".join("".join(row) for row in grid)
    return plain.rstrip("_")


msg = input("\nEnter the message: ")
key = input("Enter the key: ").upper()

cipher = encrypt(msg, key)
print("\nEncrypted text:", cipher)
print("Decrypted text:", decrypt(cipher, key))
