# CN Unit 4: The Network Layer, IPv4 Addressing, NAT and IPv6

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** every device on the Internet needs a 32-bit IPv4 address; this unit is about how those addresses are split into a **network part and a host part** (classes, then CIDR), how networks are cut smaller (**subnetting**) or merged (**supernetting**), how many devices share one public address (**NAT**), and the 128-bit fix for running out (**IPv6**).

**What the endsem asks from here:** Q4 every year. Expect a subnet/CIDR numerical (which hosts share a subnet, split a block between organisations), NAT, and special addresses. All three came in 2025.

---

## 1. IPv4 addresses · Quick

**Exam line:** *An IPv4 address is a 32-bit logical address that uniquely identifies a host interface on an IP network, written in dotted-decimal notation as four octets, e.g. 192.168.10.5.*

Think of it like a postal address: the **network part** is the city and street (routers only care about this), and the **host part** is the house number (used only once the packet reaches the right network).

Total possible addresses: $2^{32} \approx 4.3$ billion. Not enough for today's devices, hence CIDR, NAT and IPv6.

---

## 2. Classful addressing · Quick

The original scheme: the first few bits decide the class, and the class fixes where the network part ends.

| Class | First bits | First octet | Default mask | Networks | Hosts per network | Use |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0 | 0–127 | 255.0.0.0 (/8) | 128 | $2^{24} - 2$ | Huge orgs |
| B | 10 | 128–191 | 255.255.0.0 (/16) | 16,384 | $2^{16} - 2$ = 65,534 | Medium |
| C | 110 | 192–223 | 255.255.255.0 (/24) | ~2 million | $2^8 - 2$ = 254 | Small |
| D | 1110 | 224–239 | none | | | Multicast |
| E | 1111 | 240–255 | none | | | Reserved |

The "− 2" is because the all-0s host part is the **network address** and the all-1s host part is the **broadcast address**.

**Why classful failed:** huge waste. A company needing 300 hosts was too big for C (254), so it got a whole B (65,534) and wasted 65,000 addresses. Too few size choices.

---

## 3. Classless addressing and CIDR · Slow down

**CIDR (Classless Inter-Domain Routing)** throws away the classes: the network part can be **any** length, written after a slash.

**Exam line:** *In CIDR notation a.b.c.d/n, the first n bits are the network prefix and the remaining 32 − n bits identify hosts; a block contains $2^{32-n}$ addresses.*

Rules for a valid block: the size is a power of 2, the addresses are contiguous, and the first address is divisible by the block size.

**From any address and prefix, find the block:**

- **Mask:** n ones then zeros. /26 → 255.255.255.192.
- **First (network) address:** set the host bits to 0 (address AND mask).
- **Last (broadcast) address:** set the host bits to 1.
- **Usable hosts:** $2^{32-n} - 2$.

Example: 205.16.37.39/28. Block size $2^4 = 16$. 39 lies in 32–47. **Network 205.16.37.32, broadcast 205.16.37.47, hosts .33 to .46.**

### Dividing a block between organisations (2024 endsem)

ISP has 245.248.128.0/20 ($2^{12}$ = 4096 addresses). Give half to A and a quarter to B.

| Who | Size | Prefix | Range |
| --- | --- | --- | --- |
| A (half) | 2048 | /21 | 245.248.128.0 – 245.248.135.255 |
| B (quarter) | 1024 | /22 | 245.248.136.0 – 245.248.139.255 |
| ISP keeps | 1024 | /22 | 245.248.140.0 – 245.248.143.255 |

Each step: half of /20 is /21 (one more prefix bit), and 2048 addresses span 8 values in the third octet (2048 / 256 = 8), so 128 to 135.

**ISP keeps 1024 addresses.**

---

## 4. Subnetting and supernetting · Slow down

**Subnetting** = cutting one network into smaller ones by **borrowing host bits** for a subnet number. Like dividing a big hostel floor into wings: fewer rooms per wing, but each wing is managed separately, and broadcast noise stays inside a wing.

Borrow s bits: you get $2^s$ subnets, each with $2^{h-s} - 2$ usable hosts.

Example: 192.168.1.0/24 split into 4 subnets: borrow 2 bits → /26, 64 addresses each:

| Subnet | Network | Hosts | Broadcast |
| --- | --- | --- | --- |
| 1 | 192.168.1.0 | .1 – .62 | .63 |
| 2 | 192.168.1.64 | .65 – .126 | .127 |
| 3 | 192.168.1.128 | .129 – .190 | .191 |
| 4 | 192.168.1.192 | .193 – .254 | .255 |

**Supernetting (route aggregation)** = the opposite: combine several contiguous blocks into one bigger block with a **shorter** prefix, so routers need one entry instead of many. Example: 200.10.0.0/24, 200.10.1.0/24, 200.10.2.0/24, 200.10.3.0/24 → **200.10.0.0/22**. Condition: the blocks are contiguous, their count is a power of 2, and the first one is divisible by the total size.

> **Endsem 2025 · Q4(a) · 4.5 marks**
> Machines M, N and P have IP addresses 100.10.5.2, 100.10.5.5 and 100.10.5.6. The subnet mask is 255.255.255.252 for all three. Which is true? (A) M, N and P are in the same subnet. (B) M and N are in the same subnet; P is in a different one. (C) M and P are in the same subnet; N is in a different one. (D) M, N and P are all in different subnets. Justify.

**Answer.**

Mask 255.255.255.252 = **/30**: the last octet's mask is `11111100`, so each subnet has $2^2 = 4$ addresses (2 usable). AND only the last octet, since the first three are equal for all:

| Machine | Last octet | Binary | AND 11111100 | Subnet |
| --- | --- | --- | --- | --- |
| M | 2 | 000000**10** | 00000000 = 0 | 100.10.5.0/30 (block .0–.3) |
| N | 5 | 000001**01** | 00000100 = 4 | 100.10.5.4/30 (block .4–.7) |
| P | 6 | 000001**10** | 00000100 = 4 | 100.10.5.4/30 (block .4–.7) |

So **N and P share the subnet 100.10.5.4/30, and M is alone in 100.10.5.0/30.**

None of the four printed options says exactly this, and that's worth writing in the answer. The question is from GATE 2006, whose options were "only N and P belong to the same subnet", so the paper's options look misprinted. As printed, all four options are false; write the correct statement: "**N and P are in the same subnet, M is in a different subnet**".

**N and P are on 100.10.5.4/30; M is on 100.10.5.0/30.**

---

## 5. Special addresses · Slow down

| Address | Meaning |
| --- | --- |
| **0.0.0.0** | "This host / unspecified". Used as a *source* by a host that doesn't know its IP yet (DHCP). Also the "default route" 0.0.0.0/0 |
| **127.0.0.0/8** (e.g. 127.0.0.1) | **Loopback**: the packet never leaves the machine; used to test the local TCP/IP stack |
| **255.255.255.255** | **Limited broadcast**: all hosts on *this* local network; routers never forward it |
| Host bits all 1 (e.g. 192.168.1.255/24) | **Directed broadcast**: all hosts on *that specific* network; can be routed to it |
| **10.0.0.0/8, 172.16.0.0/12 (172.16–172.31), 192.168.0.0/16** | **Private** addresses: used inside organisations, not routed on the Internet (need NAT) |
| **224.0.0.0/4** (224–239) | **Multicast** (class D) |
| **169.254.0.0/16** | Link-local / APIPA: self-assigned when DHCP fails |
| 240.0.0.0/4 | Reserved (class E) |

> **Endsem 2025 · Q4(b') · 4.5 marks**
> Answer based on IPv4: (i) What is the purpose of 127.0.0.1? Can it be used to communicate with another host? (ii) A host sends a packet with destination 0.0.0.0. What happens? (iii) Differentiate 255.255.255.255 from a subnet-directed broadcast such as 192.168.1.255 in a /24. (iv) Explain the purpose of the 224.0.0.0/4 range. (v) Is 172.32.5.1 a special address or not?

**Answer.**

**(i)** 127.0.0.1 is the **loopback** address: a packet sent to it is handed straight back up the host's own TCP/IP stack without ever reaching the network card. It's used to test networking software and to reach services running on the same machine (e.g. a local web server). It **cannot** be used to communicate with another host: routers and the NIC never send loopback traffic out.

**(ii)** 0.0.0.0 means "this host / unspecified address". It is valid only as a **source** (e.g. a DHCP client that has no IP yet). As a **destination** it is invalid: it isn't routable, so routers drop it and the packet never leaves the network (some operating systems treat it as "this machine" and loop it back locally). It's never delivered to another host.

**(iii)**

| 255.255.255.255 (limited broadcast) | 192.168.1.255 /24 (directed broadcast) |
| --- | --- |
| All hosts on the **local** network the sender is on | All hosts on a **specific** network, 192.168.1.0/24 |
| Sender needn't know its own network address | Needs the network address and mask |
| **Never forwarded** by routers | **Can be routed** to that network (though usually blocked today for security, e.g. smurf attacks) |
| Used by DHCP discovery | Used to reach every host of a remote subnet |

**(iv)** 224.0.0.0/4 (224.0.0.0 to 239.255.255.255, old class D) is for **multicast**: one sender delivers to a **group** of interested receivers with a single stream (video streaming, routing protocols like OSPF on 224.0.0.5, IPTV). A multicast address names a group, never a single host.

**(v)** The private block is 172.**16**.0.0 – 172.**31**.255.255 (172.16.0.0/12). **172.32.5.1 lies just outside it**, so it is **not private and not special**. It's an ordinary public (classful class B) unicast address.

**127.0.0.1 is loopback (local only); 0.0.0.0 as a destination is invalid and dropped; limited broadcast stays local while directed broadcast targets a remote network; 224/4 is multicast; 172.32.5.1 is a normal public address.**

---

## 6. NAT · Slow down

Your hostel has one public IP from the ISP, but 300 laptops. **NAT (Network Address Translation)** lets all of them share it. The NAT router rewrites addresses on the way out and back, like a hostel reception that sends everyone's letters with the hostel's address and hands replies to the right room using a register.

**Exam line:** *NAT is a technique in which a router replaces the private source IP address (and port) of outgoing packets with its own public IP address (and a new port), recording the mapping in a translation table so that replies can be mapped back to the correct internal host.*

The most common form is **PAT / NAPT** (port address translation), which uses **port numbers** to tell the internal hosts apart. That's how thousands of hosts share one public IP.

> **Endsem 2025 · Q4(b) · 4.5 marks**
> Where multiple devices are behind a NAT, explain how IP addresses and port numbers are translated. Show the scenario of a packet going out of a NAT device from the internal network to an external network.

**Answer.**

**Setup:** internal network 192.168.1.0/24; NAT router's public IP 200.24.5.8. Two laptops open web pages on server 25.8.2.10, port 80.

**Outgoing packet (inside → outside):**

1. Host A sends: source **192.168.1.10 : 3345**, destination 25.8.2.10 : 80.
2. The NAT router replaces the **source IP** with its public IP and the **source port** with a unique port it picks (because many inside hosts may use the same port), and records the mapping.
3. The packet leaves as: source **200.24.5.8 : 5001**, destination 25.8.2.10 : 80. The IP and TCP checksums are recomputed.

```
 Inside                           NAT router                         Outside
 192.168.1.10:3345 --> 25.8.2.10:80  ==>  200.24.5.8:5001 --> 25.8.2.10:80
 192.168.1.11:3345 --> 25.8.2.10:80  ==>  200.24.5.8:5002 --> 25.8.2.10:80
```

**Translation table (built as packets go out):**

| Private IP | Private port | Public IP | Public port | Destination |
| --- | --- | --- | --- | --- |
| 192.168.1.10 | 3345 | 200.24.5.8 | 5001 | 25.8.2.10:80 |
| 192.168.1.11 | 3345 | 200.24.5.8 | 5002 | 25.8.2.10:80 |

Both laptops used port 3345, but NAT gave them different public ports, so the replies can't get mixed up.

**Reply (outside → inside):** the server answers to 200.24.5.8 : 5002. NAT looks up port 5002 in the table, rewrites the destination to **192.168.1.11 : 3345**, and forwards it inside.

**Benefits:** saves public IPv4 addresses, hides internal structure (some security). **Drawbacks:** outsiders can't start connections to inside hosts without port forwarding, it breaks the end-to-end principle, and it adds processing.

**NAT swaps the private source IP:port for the public IP and a unique port, stores the mapping, and reverses it for replies.**

---

## 7. IPv6 · Quick

**Why:** IPv4 ran out. IPv6 uses **128-bit** addresses ($2^{128} \approx 3.4 \times 10^{38}$).

**Notation:** 8 groups of 4 hex digits, e.g. `2001:0DB8:0000:0000:0000:0000:1428:57AB`. Shorten by dropping leading zeros in a group and replacing **one** run of all-zero groups with `::` → `2001:DB8::1428:57AB`.

**What changed vs IPv4:**

| IPv4 | IPv6 |
| --- | --- |
| 32-bit address | 128-bit address |
| Variable header (20–60 bytes) with options | Fixed 40-byte base header, options in extension headers |
| Header checksum | No header checksum (upper layers check) |
| Routers may fragment | Only the source fragments |
| Broadcast | No broadcast: multicast and anycast instead |
| Manual / DHCP config | Stateless auto-configuration too |
| IPSec optional | IPSec built in |

**Address types:** unicast (one host), multicast (a group), anycast (the nearest of a group). Loopback is `::1`.

**Moving from IPv4 to IPv6:** **dual stack** (devices run both), **tunnelling** (IPv6 packets carried inside IPv4 packets across IPv4 networks), and **header translation** (NAT64, when one side speaks only IPv4).

---

## 8. Quick recap

- IPv4: 32 bits; classes A (/8), B (/16), C (/24), D multicast, E reserved.
- CIDR /n: block = $2^{32-n}$; network = host bits 0; broadcast = host bits 1; hosts = block − 2.
- Same subnet ⇔ same (address AND mask).
- Subnetting borrows host bits; supernetting merges contiguous blocks into a shorter prefix.
- Specials: 127/8 loopback, 0.0.0.0 unspecified, 255.255.255.255 limited broadcast, private 10/8, 172.16/12, 192.168/16, multicast 224/4.
- NAT/PAT: rewrite source IP:port, keep a table, reverse for replies.
- IPv6: 128 bits, `::`, fixed 40-byte header, no broadcast, dual stack / tunnelling / translation.
