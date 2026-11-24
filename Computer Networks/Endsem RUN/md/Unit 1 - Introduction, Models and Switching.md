# CN Unit 1: Introduction, Reference Models and Switching

*Endsem RUN · about 45 minutes*

**The whole unit in one breath:** a network is computers sharing data; to keep that manageable, the job is split into **layers** (OSI has 7, TCP/IP has 4–5), each doing one thing; and data crosses the network by **circuit, message or packet switching**.

**What the endsem asks from here:** Q1 is always this unit. 2025 asked what each layer does when a file goes between two LANs (data unit, address, device, delivery type), how TCP makes IP reliable, and true/false-with-reasons on packet vs circuit switching. 2024 asked encapsulation and addressing per layer. So the **layer table** below is the single most valuable thing in this unit.

---

## 1. Networks, and LAN / MAN / WAN · Quick

**Exam line:** *A computer network is a set of autonomous computers (nodes) interconnected by a communication medium so they can share data and resources.*

**Uses:** resource sharing (printers, files), communication (email, video calls), remote access, e-commerce, cloud and entertainment.

| | LAN | MAN | WAN |
| --- | --- | --- | --- |
| Covers | A room, building, campus | A city | Countries, the globe |
| Range | Up to ~1–2 km | ~5–50 km | Unlimited |
| Speed | High (100 Mbps–10 Gbps) | Medium–high | Lower, varies |
| Owner | One organisation | City / company | Many (ISPs, telcos) |
| Errors | Very few | Few | More |
| Example | JMI lab network | Cable TV network of a city | The Internet |

---

## 2. Topologies and access methods · Quick

A **topology** is the shape in which devices are connected.

| Topology | Picture it as | Plus | Minus |
| --- | --- | --- | --- |
| **Bus** | Everyone tapped onto one cable | Cheap, easy | One cable break kills all; collisions |
| **Star** | Everyone wired to a central hub/switch | Easy to add/remove; one bad cable affects one node | Hub fails → all down |
| **Ring** | Each device joined to two neighbours in a circle | No collisions (token) | One break can stop the ring |
| **Mesh** | Every device linked to every other | Very reliable, private links | Needs n(n−1)/2 cables: costly |
| **Tree / hybrid** | Stars connected in a hierarchy | Scales well | Depends on the root |

**Access methods** decide who may transmit on a shared medium: **CSMA/CD** (Ethernet: listen, transmit, detect collisions), **token passing** (token ring/bus: only the token holder talks), and **CSMA/CA** (Wi-Fi: avoid collisions). Details are in Unit 3.

---

## 3. Layers, protocols and standards · Quick

Sending data is a huge job: turning bits into signals, finding the right machine, finding the right app, fixing errors. **Layering** splits it into small jobs, like a company where the writer, the packer and the courier each do one task and hand over to the next.

- A **protocol** is the set of rules two peers on the same layer follow (syntax, semantics, timing). Examples: HTTP, TCP, IP, Ethernet.
- A **standard** is an agreed, published protocol so that equipment from different makers works together. Bodies: ISO, IEEE (802.x), ITU-T, IETF (RFCs), ANSI.
- **Network architecture** = the set of layers plus their protocols.
- **Interface / service:** each layer offers services to the layer above through an interface, and hides how it does it.

---

## 4. The OSI model · Slow down

Seven layers. Mnemonic from bottom up: **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way.

| # | Layer | Job in one line | Data unit | Address | Device |
| --- | --- | --- | --- | --- | --- |
| 7 | Application | Services to the user (HTTP, FTP, SMTP, DNS) | Message / data | URL, email address | Gateway |
| 6 | Presentation | Format, encryption, compression | Data | | |
| 5 | Session | Open, manage and close dialogs; checkpoints | Data | | |
| 4 | Transport | **Process-to-process** delivery, reliability, flow control | **Segment** | **Port number** | (end hosts) |
| 3 | Network | **Host-to-host** delivery across networks, routing | **Packet / datagram** | **IP address** (logical) | **Router** |
| 2 | Data link | **Hop-to-hop** delivery on one link, framing, error and flow control | **Frame** | **MAC address** (physical) | **Switch, bridge, NIC** |
| 1 | Physical | Bits as signals on the medium | **Bit** | none | **Hub, repeater, cable** |

**Encapsulation:** going down, each layer adds its own **header** (data link also adds a trailer, the CRC) to what came from above. **Decapsulation:** going up at the receiver, each layer strips its header and passes the rest up. Like putting a letter in an envelope, the envelope in a parcel, the parcel in a truck, then unpacking in reverse.

```
Application data                         [ DATA ]
Transport   adds port numbers        [TH| DATA ]            = segment
Network     adds IP addresses    [NH|TH| DATA ]             = packet
Data link   adds MAC + CRC   [DH|NH|TH| DATA |DT]           = frame
Physical    sends it as      0101100101110...               = bits
```

---

## 5. TCP/IP model and the comparison · Quick

The Internet actually runs on **TCP/IP**, which has 4 layers (5 if you split the bottom one):

| TCP/IP layer | Matches OSI | Protocols |
| --- | --- | --- |
| Application | Application + Presentation + Session | HTTP, FTP, SMTP, DNS |
| Transport | Transport | TCP, UDP |
| Internet | Network | IP, ICMP, ARP |
| Network access (link + physical) | Data link + Physical | Ethernet, Wi-Fi |

| OSI | TCP/IP |
| --- | --- |
| 7 layers | 4 (or 5) layers |
| A reference model, designed before the protocols | Built around protocols that already worked |
| Clear split of service, interface, protocol | Less strict |
| Transport: connection-oriented only (in the model) | Transport: TCP (connection-oriented) and UDP (connectionless) |
| Theoretical, used for teaching | Practical, runs the Internet |

---

## 6. The 2025 layer question · Slow down

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

---

## 7. How TCP makes unreliable IP reliable · Slow down

IP is like a postal service that might lose, duplicate or reorder your letters and never tells you. TCP is the careful sender on top of it who numbers every page and insists on receipts.

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

---

## 8. Circuit, message and packet switching · Slow down

**Switching** is how data gets from source to destination through intermediate nodes when there's no direct wire.

- **Circuit switching** (old telephone network): a dedicated path is reserved end to end *before* talking; then data flows with fixed delay; the path is released at the end. Like booking an entire train compartment for your trip: guaranteed, but empty seats are wasted.
- **Message switching** (old telegraph): the whole message hops node to node, each node storing it fully before forwarding (**store-and-forward**). No reserved path, but big delays and big buffers.
- **Packet switching** (the Internet): the message is cut into small **packets**, each sent independently and stored-and-forwarded. Like sending a book as numbered postcards: links are shared, but postcards may arrive late or out of order.
  - **Datagram approach:** each packet is routed on its own (connectionless, like IP).
  - **Virtual circuit approach:** a path is set up first, and all packets follow it in order (connection-oriented over packet switching, e.g. ATM, MPLS), but the links are still *shared*, not reserved.

| | Circuit | Message | Packet |
| --- | --- | --- | --- |
| Path set up first | Yes | No | No (datagram) / logical (VC) |
| Resources | Reserved | Shared | Shared |
| Unit | Continuous stream | Whole message | Small packets |
| Delay | Setup delay, then constant | High | Variable (queueing) |
| Bandwidth use | Wasteful when silent | Better | Best |
| Order | Preserved | Preserved | May be reordered (datagram) |
| Example | Telephone | Telegram, email (old) | Internet |

> **Endsem 2025 · Q1(b)(ii) · 2.5 marks**
> Comment with justification: (A) Packet switching gives better bandwidth utilization than circuit switching. (B) Packet switching results in less variation in delay than circuit switching. (C) Packet switching needs more per-packet processing than circuit switching. (D) Packet switching can lead to reordering, unlike circuit switching.

**Answer.**

**(A) True.** In circuit switching, the reserved bandwidth sits idle whenever the user is silent. Packet switching shares links among all users on demand (**statistical multiplexing**), so idle gaps get used by others.

**(B) False.** It's the opposite. Packets wait in router queues whose length keeps changing, so delay varies a lot (**jitter**). Circuit switching has a fixed path and reserved capacity, so after setup the delay is nearly constant.

**(C) True.** Every packet carries a header that each router must read, look up in the routing table and forward (store-and-forward). In circuit switching, the route is decided once at setup; afterwards data just flows with no per-unit decisions.

**(D) True.** In datagram packet switching, packets may take different routes with different delays, so they can arrive out of order (TCP reorders them). A circuit is one fixed path, so order is always preserved.

**A true, B false (packet switching has MORE delay variation), C true, D true.**

---

## 9. When layers misbehave (2025 OR question) · Quick

These two were the OR choice for Q1(b). They test whether you understand how the layers depend on each other.

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

---

## 10. Quick recap

- LAN / MAN / WAN by size; topologies: bus, star, ring, mesh (n(n−1)/2 links), tree.
- OSI 7 layers; units: bit, frame, packet, segment; addresses: MAC, IP, port.
- Delivery: physical bit-by-bit, data link hop-to-hop, network host-to-host, transport process-to-process.
- IP stays the same end to end; MAC changes every hop.
- TCP reliability: handshake, sequence numbers, ACKs, retransmission, checksum, flow and congestion control.
- Circuit = reserved path, constant delay, wasteful; packet = shared, efficient, jittery, may reorder.
