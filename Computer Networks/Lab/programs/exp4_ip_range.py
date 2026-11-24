# Experiment 4 - First address, last address and total number of addresses
# from a given IP address in CIDR form (eg 205.16.37.39/28)

name = "Mohd Shahan Shah Ayyubi"
roll = "24BCS064"
print(name)
print(roll)


def to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def to_ip(n):
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def to_bin(n):
    b = format(n, "032b")
    return ".".join(b[i:i + 8] for i in range(0, 32, 8))


while True:
    addr = input("\nEnter IP address with prefix (or q to quit): ").strip()
    if addr == "q":
        break
    ip, n = addr.split("/")
    n = int(n)

    ip_val = to_int(ip)
    mask = (0xFFFFFFFF << (32 - n)) & 0xFFFFFFFF

    first = ip_val & mask                  # host bits -> 0
    last = first | (~mask & 0xFFFFFFFF)    # host bits -> 1
    total = 2 ** (32 - n)

    print("Given address  :", to_bin(ip_val))
    print("Mask (/%d)     :" % n, to_bin(mask), "=", to_ip(mask))
    print("First address  :", to_ip(first))
    print("Last address   :", to_ip(last))
    print("Total addresses:", total)
