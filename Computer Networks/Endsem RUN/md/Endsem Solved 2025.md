# Computer Networks Endsem 2025, Solved

**Paper:** B.Tech (CE) Sem V, Computer Networks (CSC-503 / CEN-505 Old), 3 hours, 45/60 marks. Attempt all questions; where a part has an OR, do one of the two. All parts are solved here, OR options included.

Every question of the 2025 endsem paper, solved. The same answers sit inside the unit docs at the topic they belong to; the unit is named under each question so you can jump there for the explanation.

---

## Question 1

> **Endsem 2025 · Q1(a) · 4.5 marks**
> Compare and discuss how each of the layers Physical, Data Link, Network and Transport helps in transferring a file from one laptop to another across different LANs connected by routers. Explain (i) the data unit at each layer, (ii) the address type used, (iii) the networking devices involved, (iv) the type of data delivery. Draw a simple diagram showing how data moves across layers.

**Answer.**

Laptop A (on LAN 1) sends a file to Laptop B (on LAN 2); the LANs are joined by a router.

| Layer | (i) Data unit | (ii) Address | (iii) Devices | (iv) Delivery | Role in the file transfer |
| --- | --- | --- | --- | --- | --- |
| Transport | Segment (TCP) | Port number (e.g. 21 for FTP) | End hosts only | **Process-to-process** (end-to-end), reliable | Splits the file into segments, numbers them, gets ACKs, retransmits losses, reorders |
| Network | Packet / datagram | IP address (logical, global) | **Router** | **Host-to-host** (source to destination across networks) | Puts A's and B's IP in every packet; routers pick the path between LANs |
| Data link | Frame | MAC address (physical, local) | **Switch**, bridge, NIC | **Hop-to-hop** (node-to-node on one link) | Frames each packet for the next hop; MAC addresses are rewritten at every router; CRC catches errors |
| Physical | Bit | None | Hub, repeater, cables, NIC transceiver | **Bit-by-bit** over the medium | Turns frames into electrical / radio signals |

The key idea for the "compare": **IP addresses stay the same end to end, but MAC addresses change at every hop**, because the data link layer only cares about getting to the next device. Ports pick the application on the final machine.

```
 Laptop A                     Router                     Laptop B
+-----------+                                          +-----------+
| Transport | ............ segments (ports) ........... | Transport |
| Network   | --packet-->  +---------+  --packet-->     | Network   |
| Data link | --frame--->  | Network |  --frame--->     | Data link |
| Physical  | ~~bits~~~~>  | DL | PHY|  ~~bits~~~~>     | Physical  |
+-----------+   (LAN 1,    +---------+   (LAN 2,        +-----------+
                switch)                  switch)
 Router works up to layer 3 only; switches up to layer 2.
```

**Transport = segments, ports, end-to-end; network = packets, IP, routers, host-to-host; data link = frames, MAC, switches, hop-to-hop; physical = bits, no address, hubs and cables.**

*Taught in Unit 1.*

> **Endsem 2025 · Q1(b)(i) · 2 marks**
> In the TCP/IP suite, explain how the transport layer provides reliable data delivery even when the underlying network layer (IP) is unreliable and connectionless.

**Answer.**

TCP adds reliability **end to end**, using these mechanisms:

1. **Connection setup (3-way handshake: SYN, SYN-ACK, ACK):** both sides agree on starting sequence numbers before data flows.
2. **Sequence numbers:** every byte is numbered, so the receiver can put out-of-order segments back in order and drop duplicates.
3. **Acknowledgements:** the receiver confirms what it got (cumulative ACKs).
4. **Retransmission on timeout:** if no ACK arrives in time, the segment is resent, so losses are repaired.
5. **Checksum:** detects corrupted segments, which are discarded (and later resent).
6. **Flow control (sliding window):** the receiver advertises how much it can accept, so it is never flooded.
7. **Congestion control:** TCP slows down when the network is congested, preventing mass losses.

**TCP turns IP's best-effort service into a reliable byte stream with sequence numbers, ACKs, timeouts and retransmission, checksums, and flow/congestion control.**

*Taught in Unit 1.*

> **Endsem 2025 · Q1(b)(ii) · 2.5 marks**
> Comment with justification: (A) Packet switching gives better bandwidth utilization than circuit switching. (B) Packet switching results in less variation in delay than circuit switching. (C) Packet switching needs more per-packet processing than circuit switching. (D) Packet switching can lead to reordering, unlike circuit switching.

**Answer.**

**(A) True.** In circuit switching, the reserved bandwidth sits idle whenever the user is silent. Packet switching shares links among all users on demand (**statistical multiplexing**), so idle gaps get used by others.

**(B) False.** It's the opposite. Packets wait in router queues whose length keeps changing, so delay varies a lot (**jitter**). Circuit switching has a fixed path and reserved capacity, so after setup the delay is nearly constant.

**(C) True.** Every packet carries a header that each router must read, look up in the routing table and forward (store-and-forward). In circuit switching, the route is decided once at setup; afterwards data just flows with no per-unit decisions.

**(D) True.** In datagram packet switching, packets may take different routes with different delays, so they can arrive out of order (TCP reorders them). A circuit is one fixed path, so order is always preserved.

**A true, B false (packet switching has MORE delay variation), C true, D true.**

*Taught in Unit 1.*

> **Endsem 2025 · Q1(b')(i) · 2.5 marks**
> What problems could arise if IP addressing is correct but MAC addressing is incorrectly mapped due to an outdated ARP cache? How might this affect port-based communication?

**Answer.**

**ARP** (Address Resolution Protocol) maps an IP address to the MAC address of the machine on the local link. Hosts cache these mappings. If a cache entry is stale (e.g. the target's NIC was replaced, or its IP was given to another machine by DHCP):

- Frames are sent to the **wrong MAC**: either to a different machine, which discards them because the IP isn't its own, or to no one at all.
- The packet has the **right IP**, but it never reaches the right host, because delivery on a LAN happens by MAC. So routing looks "correct" while delivery fails silently.
- **Effect on ports:** port numbers are read only by the transport layer of the *destination* host. Since the frames never reach it, no segment reaches the intended port. TCP connections time out, retransmissions pile up, and applications see the server as down. UDP data is simply lost.
- It also opens a **security** hole: an attacker can poison caches (ARP spoofing) to receive traffic meant for others.
- Fix: the entry expires (ARP timeout), or the host sends a **gratuitous ARP** to update everyone.

**A wrong ARP entry sends correct IP packets to the wrong MAC, so they never reach the destination's transport layer and its ports; connections time out.**

*Taught in Unit 1.*

> **Endsem 2025 · Q1(b')(ii) · 2 marks**
> How does the absence of flow control at the data link layer lead to buffer overflows at the transport layer? Discuss the cascading effects.

**Answer.**

Without data-link flow control, a fast sender keeps pushing frames faster than the receiving node can process. The receiver's buffers fill and **frames are dropped**. The chain reaction:

1. **Drops at the link** look like losses to the layers above.
2. **Transport retransmits:** TCP times out and resends, adding *even more* traffic onto the already overloaded link.
3. **Receiver buffers overflow further:** retransmissions plus new data arrive faster than the transport layer can hand data to the application, so its buffers overflow too.
4. **Duplicates and reordering** grow, wasting more processing.
5. **Throughput collapses** (a congestion collapse in the worst case): the link is busy, but mostly with repeated data, and delay shoots up.

**No flow control at layer 2 causes frame drops, which trigger transport retransmissions, which add more load, so buffers overflow at every level and useful throughput collapses.**

*Taught in Unit 1.*

---

## Question 2

> **Endsem 2025 · Q2(a) · 4.5 marks**
> In Go-Back-N ARQ, explain why the sender's window size is $2^n - 1$, while the receiver's window size is limited to 1. Describe how the protocol handles (i) duplicate frames, (ii) lost frames, (iii) lost acknowledgments.

**Answer.**

**Why sender window = $2^n - 1$:** with n bits, sequence numbers are 0 to $2^n - 1$, i.e. $2^n$ numbers. Suppose n = 2 (numbers 0–3) and the window were 4. The sender sends 0, 1, 2, 3, and **all four ACKs are lost**. The receiver, having received them, now expects 0 (the next round). The sender times out and resends the old 0. The receiver accepts this **old frame as a new one**: a duplicate gets through, which is a silent error. With the window at $2^n - 1$ = 3 (frames 0, 1, 2), the receiver then expects 3, so a resent 0 is recognised as a duplicate and discarded. Keeping one number unused removes the ambiguity.

**Why receiver window = 1:** GBN accepts frames **strictly in order**. The receiver only ever waits for one specific sequence number, the next expected one, and discards anything else. So it needs space for just one frame, which keeps the receiver simple (no buffering, no reordering).

**(i) Duplicate frames:** the frame's sequence number isn't the expected one, so the receiver **discards** it and re-sends an ACK for the last in-order frame (so the sender learns where it stands).

**(ii) Lost frame:** say frame 2 is lost. Frames 3, 4 … arrive out of order and are **discarded**. No ACK for 2 arrives, so the sender's **timer for frame 2 expires** and it **goes back**, resending 2 and every frame after it.

**(iii) Lost acknowledgment:** ACKs are **cumulative**, so if ACK 2 is lost but ACK 4 arrives, ACK 4 confirms frames up to 3 as well; nothing is resent. If all ACKs for the window are lost, the timer expires, the sender resends the window, and the receiver discards those as duplicates while re-ACKing.

**Sender window 2ⁿ − 1 stops an old frame being taken as new after a wrap; receiver window 1 because GBN accepts only in order. Duplicates are discarded, a lost frame makes the sender go back N, and a lost ACK is covered by a later cumulative ACK or a timeout.**

*Taught in Unit 2.*

> **Endsem 2025 · Q2(b) · 4.5 marks**
> The following character encoding is used in a data link protocol: A: 01000111; B: 11100011; FLAG: 01111110; ESC: 11100000. Show the bit sequence transmitted for the four-character frame A ESC D FLAG when using (i) character count, (ii) flag bytes with byte stuffing, (iii) starting and ending flag bytes with bit stuffing.

**Answer.**

Two typos to handle first (write these assumptions in the exam): **D has no encoding given**, so take it as **B**, the only other defined character; and ESC is printed with 9 bits, so use the 8-bit `11100000`. The frame is therefore **A ESC B FLAG**.

**(i) Character count.** 4 characters + 1 count byte = 5, so the count is `00000101`.

```
00000101  01000111  11100000  11100011  01111110
 count       A        ESC        B        FLAG
```

**(ii) Flag bytes with byte stuffing.** Add a FLAG at both ends. Inside the data, put an extra ESC before the data's ESC and before the data's FLAG.

```
01111110  01000111  11100000 11100000  11100011  11100000 01111110  01111110
  FLAG       A      ESC(add)  ESC         B      ESC(add)  FLAG       FLAG
```

**(iii) Bit stuffing.** Raw data: `01000111 11100000 11100011 01111110`. Scan for five 1s in a row and insert a 0:

- A ends in `111` and ESC starts with `111`: after the fifth 1, insert `0`.
- The data's FLAG `01111110` has six 1s: after the fifth, insert `0`.

```
raw:      01000111 11100000 11100011 01111110
stuffed:  01000111 11 0 100000 11100011 0 11111 0 10
sent:     01111110 0100011111010000011100011011111010 01111110
```

**Stuffed data is 34 bits (2 zeros added), framed by 01111110 at both ends.**

*Taught in Unit 2.*

> **Endsem 2025 · Q2(b') · 4.5 marks**
> A sliding-window protocol runs over a full-duplex, error-free link. Processing times are negligible; the sender always has frames ready. Each data frame is 2000 bits, each ACK is 10 bits. The link rate is 1 Mbps both ways. One-way propagation delay is 100 ms. Find the minimum sender window size (in frames) to achieve 50% link utilization.

**Answer.**

```latex
\begin{aligned}
T_t &= \frac{2000}{10^6} = 2 \text{ ms}, \qquad T_{ack} = \frac{10}{10^6} = 0.01 \text{ ms}, \qquad T_p = 100 \text{ ms} \\
\text{Cycle} &= T_t + 2T_p + T_{ack} = 2 + 200 + 0.01 = 202.01 \text{ ms} \\
\eta &= \frac{W \cdot T_t}{\text{Cycle}} = 0.5 \\
W &= \frac{0.5 \times 202.01}{2} = 50.5
\end{aligned}
```

W must be a whole number of frames, and 50 would give slightly under 50%, so round **up**.

**Minimum sender window = 51 frames.**

*Taught in Unit 2.*

---

## Question 3

> **Endsem 2025 · Q3(a) · 4.5 marks**
> Describe in detail how the RTS/CTS (Request to Send / Clear to Send) mechanism in IEEE 802.11 MAC helps avoid collisions caused by hidden terminals. Why can't RTS/CTS fully eliminate the exposed terminal problem?

**Answer.**

**Hidden terminal recap:** A and C are both in range of B but not of each other. Carrier sensing at A can't hear C, so both may transmit to B and collide at B.

**RTS/CTS handshake (the receiver "announces" the reservation):**

```
A (sender)          B (receiver)          C (hidden from A)
   | --- RTS (duration) ---> |                    |
   |                         | --- CTS (duration) --> (C hears CTS!)
   | <-- CTS (duration) ---- |                    C sets NAV, stays quiet
   | ------- DATA ---------> |                    |
   | <------ ACK ----------- |                    |
```

1. A sends a short **RTS** to B containing the **duration** of the whole exchange.
2. B replies with a **CTS**, also carrying the duration. The CTS is sent **by the receiver**, so it reaches **every station in B's range, including hidden C**.
3. Every station that hears the RTS or CTS sets its **NAV** for that duration and stays silent (virtual carrier sensing).
4. A sends DATA; B replies with ACK; the channel is then free.

Collisions can now only happen on the tiny RTS frames (cheap to lose), never on the long data frame. The key insight: the **receiver's** neighbourhood is what matters for collisions, and CTS informs exactly that neighbourhood.

**Why it doesn't fully solve the exposed terminal problem:**

- An exposed station C hears B's **RTS** but not A's **CTS** (A is out of its range). Strictly, C could then transmit, since it isn't near the receiver A. But C has no way to know that its transmission won't disturb things, and to be safe the basic rule makes it set its NAV and **stay silent anyway**. So the wasted opportunity remains.
- Even if C did transmit, it would be deaf to the **ACK** coming back from its own receiver D whenever B is sending, and B's ongoing data could collide with D's ACKs or CTS. Both sides' **control frames (CTS, ACK) flow in the reverse direction**, so concurrent transmissions in the "exposed" area still interfere.
- RTS/CTS also adds overhead and can't stop collisions among RTS frames themselves.

**RTS/CTS fixes hidden terminals because the receiver's CTS silences everyone near the receiver; it can't fix exposed terminals because the exposed station can't be sure its own exchange (including returning ACKs/CTS) won't collide, so it still stays quiet.**

*Taught in Unit 3.*

> **Endsem 2025 · Q3(b) · 4.5 marks**
> In a TDM medium access control bus LAN, each station gets one time slot per cycle. The length of each slot is the time to transmit 100 bits plus the end-to-end propagation delay. Propagation speed is $2 \times 10^8$ m/s, the LAN is 1 km long, bandwidth 10 Mbps. Find the maximum number of stations so that the throughput of each station can be 2/3 Mbps.

**Answer.**

```latex
\begin{aligned}
T_t &= \frac{100}{10 \times 10^6} = 10\ \mu s \\
T_p &= \frac{1000}{2 \times 10^8} = 5\ \mu s \\
\text{Slot} &= T_t + T_p = 15\ \mu s \\
\text{Cycle with } N \text{ stations} &= 15N\ \mu s \\
\text{Throughput per station} &= \frac{100 \text{ bits}}{15N\ \mu s} \ge \frac{2}{3} \times 10^6 \\
N &\le \frac{100}{15 \times 10^{-6} \times \frac{2}{3} \times 10^6} = \frac{100}{10} = 10
\end{aligned}
```

Each station sends 100 bits once per cycle, so more stations means a longer cycle and less throughput each.

**Maximum number of stations = 10.**

*Taught in Unit 3.*

> **Endsem 2025 · Q3(b') · 4.5 marks**
> A network uses pure ALOHA. Each frame is 1000 bits, the channel rate is 2 Mbps. The total transmission attempts (new + retransmissions) across all stations follow a Poisson process with rate 600 frames per second. Find the throughput in frames per second and in bits per second.

**Answer.**

```latex
\begin{aligned}
T &= \frac{1000}{2 \times 10^6} = 0.5 \text{ ms} \\
G &= 600 \times 0.5 \times 10^{-3} = 0.3 \text{ frames per frame time} \\
S &= G e^{-2G} = 0.3 \, e^{-0.6} = 0.3 \times 0.5488 = 0.1646 \\
\text{Throughput} &= \frac{S}{T} = \frac{0.1646}{0.5 \times 10^{-3}} = 329.3 \text{ frames/s} \\
&= 329.3 \times 1000 = 329{,}287 \text{ bits/s} \approx 329.3 \text{ kbps}
\end{aligned}
```

Quick sanity check: successful frames = attempts × chance of no collision = $600 \times e^{-0.6} = 329.3$. Same number.

**Throughput ≈ 329 frames per second ≈ 329.3 kbps.**

The 2024 version: 1000-bit frames at 1 Mbps (T = 1 ms) with 1000 attempts/s gives G = 1, so $S = e^{-2} = 0.135$, i.e. **135 frames/s**.

*Taught in Unit 3.*

---

## Question 4

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

*Taught in Unit 4.*

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

*Taught in Unit 4.*

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

*Taught in Unit 4.*

---

## Question 5

> **Endsem 2025 · Q5(a) · 4.5 marks**
> Six routers R1 to R6 are connected by weighted links: R1–R2 6, R1–R3 3, R2–R3 2, R2–R4 7, R3–R5 9, R4–R5 1, R4–R6 8, R5–R6 3. All routers use distance vector routing; each starts with an entry for each neighbour at the link weight. After all tables stabilise, how many links will never be used for carrying any data?

**Answer.**

When DV converges, every router has the **shortest-path** distances, and data only travels along shortest paths. So find all shortest paths, and the links on none of them are never used.

Shortest distances (computed from each router):

| From \ To | R1 | R2 | R3 | R4 | R5 | R6 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | 0 | 5 (R3) | 3 | 12 (R3) | 12 (R3) | 15 (R3) |
| R2 | 5 (R3) | 0 | 2 | 7 | 8 (R4) | 11 (R4) |
| R3 | 3 | 2 | 0 | 9 (R2) | 9 | 12 (R5) |
| R4 | 12 (R2) | 7 | 9 (R2) | 0 | 1 | 4 (R5) |
| R5 | 12 (R3) | 8 (R4) | 9 | 1 | 0 | 3 |
| R6 | 15 (R5) | 11 (R5) | 12 (R5) | 4 (R5) | 3 | 0 |

(The router in brackets is the next hop.)

Checking the two suspicious links:

- **R1–R2 (6):** R1 reaches R2 via R3 at 3 + 2 = **5 < 6**, and R2 reaches R1 the same way. No shortest path ever uses it.
- **R4–R6 (8):** R4 reaches R6 via R5 at 1 + 3 = **4 < 8**. No shortest path uses it either.

Every other link (R1–R3, R2–R3, R2–R4, R3–R5, R4–R5, R5–R6) lies on at least one shortest path. (For example R3–R5 is used by R1 → R5: 3 + 9 = 12, which beats 3 + 2 + 7 + 1 = 13.)

**2 links are never used: R1–R2 and R4–R6.**

*Taught in Unit 5.*

> **Endsem 2025 · Q5(b) · 4.5 marks**
> Explain in detail why OSPF cannot be used for inter-domain routing, while BGP is specifically designed for it. Discuss the fundamental differences in their routing policies, and how each protocol handles routing information across networks belonging to different organisations.

**Answer.**

**Why OSPF fails between domains:**

1. **Scale:** OSPF is link state: every router floods its links and stores the **entire topology**, then runs Dijkstra. Doing that for the whole Internet (tens of thousands of ASes, about a million prefixes) would need enormous memory, constant flooding and endless recomputation.
2. **Privacy:** OSPF requires every router to see every other router's internal links. Different organisations will **not reveal** their internal topology to competitors.
3. **No policy:** OSPF chooses purely by **lowest cost**. Between organisations, routes must follow **business agreements** (who pays whom, who you trust), not just shortest distance. OSPF has no way to express "don't carry my competitor's traffic" or "prefer my cheaper provider".
4. **Common metric impossible:** each organisation sets its own costs; there's no globally meaningful metric to compare across ASes.

**Why BGP fits:**

1. **Path vector:** BGP advertises reachability as an **AS path**, hiding everything inside each AS. Organisations reveal only which prefixes they can reach, not how.
2. **Policy-based routing:** each AS applies its own **import/export policies**: which routes to accept, which to prefer (local preference, shortest AS path, …) and which to advertise to whom (e.g. don't offer transit to non-customers).
3. **Loop prevention:** a router rejects any advertisement whose AS path already contains its own AS number.
4. **Scales:** only reachability to aggregated prefixes is exchanged, incrementally over reliable TCP sessions.

| | OSPF | BGP |
| --- | --- | --- |
| Scope | Intra-domain (inside one AS) | Inter-domain (between ASes) |
| Type | Link state | Path vector |
| Knows | Full topology of its area/AS | Only AS paths to prefixes |
| Route choice | Lowest cost (Dijkstra) | **Policy** first, then attributes like AS-path length |
| Information shared | All links, flooded to all routers | Selected routes, to chosen neighbours only |
| Privacy | None needed: one organisation | Internal details hidden |
| Transport | Directly over IP (protocol 89) | TCP port 179 |

**OSPF needs the whole map and picks the cheapest path, which is impossible to scale and unacceptable between rival organisations; BGP exchanges only AS-level paths and lets each organisation apply its own business policies.**

*Taught in Unit 5.*

> **Endsem 2025 · Q5(b') · 4.5 marks**
> Differentiate between static and dynamic routing. For the network given (edges A–B 4, B–C 3, C–D 4, D–F 7, E–F 7, A–E 6, B–F 5, C–E 3), obtain the routing table of router B using link state routing.

**Answer.**

**Static vs dynamic:** static routes are entered manually by an administrator, use no protocol traffic and don't adapt to failures (good for small, stable networks); dynamic routes are learnt and updated automatically by protocols such as RIP or OSPF, adapting to topology changes at the cost of overhead (needed for large networks).

**Link state:** B knows the whole graph (from flooded LSPs) and runs Dijkstra from B. (The two diagonals in the figure are B–F = 5 and C–E = 3.)

| Step | Finalised | A | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| Start | B (0) | 4 (B) | 3 (B) | ∞ | ∞ | 5 (B) |
| 1 | C (3) | 4 (B) | **3** | 3+4 = 7 (C) | 3+3 = 6 (C) | 5 (B) |
| 2 | A (4) | **4** | | 7 (C) | 6 (C), via A 10: no | 5 (B) |
| 3 | F (5) | | | 7 (C), via F 12: no | 6 (C), via F 12: no | **5** |
| 4 | E (6) | | | 7 (C) | **6** | |
| 5 | D (7) | | | **7** | | |

**Routing table of router B:**

| Destination | Cost | Next hop | Path |
| --- | --- | --- | --- |
| A | 4 | A | B → A |
| C | 3 | C | B → C |
| D | 7 | C | B → C → D |
| E | 6 | C | B → C → E |
| F | 5 | F | B → F |

**B reaches A and F directly, and C, D, E all through C (costs 3, 7, 6).**

**OSPF (Open Shortest Path First)** is the real link state protocol: it uses Dijkstra, floods LSAs only when something changes, supports **areas** (a two-level hierarchy with a backbone area 0) to keep maps small, uses costs based on bandwidth, and converges fast. Used *inside* one organisation.

*Taught in Unit 5.*

