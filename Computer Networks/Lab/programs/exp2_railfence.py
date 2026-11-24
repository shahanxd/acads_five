# Experiment 2 - Rail Fence Cipher

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)


def rail_pattern(n, rails):
    # which rail each character goes on (zig zag 0,1,2,1,0,1,2...)
    pattern = []
    row, step = 0, 1
    for i in range(n):
        pattern.append(row)
        if rails == 1:
            continue
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    return pattern


def encrypt(text, rails):
    fence = [""] * rails
    for ch, r in zip(text, rail_pattern(len(text), rails)):
        fence[r] += ch
    for i in range(rails):
        print("  rail", i + 1, ":", fence[i])
    return "".join(fence)


def decrypt(cipher, rails):
    pattern = rail_pattern(len(cipher), rails)
    # count how many letters sit on each rail, then cut the cipher into pieces
    counts = [pattern.count(r) for r in range(rails)]
    pieces, pos = [], 0
    for c in counts:
        pieces.append(list(cipher[pos:pos + c]))
        pos += c
    # read back following the zig zag
    plain = ""
    for r in pattern:
        plain += pieces[r].pop(0)
    return plain


msg = input("\nEnter the message: ")
rails = int(input("Enter number of rails: "))

cipher = encrypt(msg, rails)
print("Encrypted text:", cipher)
print("Decrypted text:", decrypt(cipher, rails))
