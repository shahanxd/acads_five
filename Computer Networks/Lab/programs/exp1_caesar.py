# Experiment 1 - Caesar Cipher

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)


def encrypt(text, key):
    result = ""
    for ch in text:
        if ch.isupper():
            result += chr((ord(ch) - 65 + key) % 26 + 65)
        elif ch.islower():
            result += chr((ord(ch) - 97 + key) % 26 + 97)
        else:
            result += ch  # spaces, digits etc stay same
    return result


def decrypt(text, key):
    # decryption is just shifting back
    return encrypt(text, -key)


msg = input("\nEnter the message: ")
key = int(input("Enter the key (shift): "))

cipher = encrypt(msg, key)
print("Encrypted text:", cipher)

plain = decrypt(cipher, key)
print("Decrypted text:", plain)
