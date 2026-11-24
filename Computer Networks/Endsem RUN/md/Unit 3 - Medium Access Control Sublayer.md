# CN Unit 3: The Medium Access Control (MAC) Sublayer

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** when many stations share one channel (one cable, one Wi-Fi frequency), someone has to decide **who talks when**. This unit is the list of strategies: random (ALOHA, CSMA), collision-free (token, bitmap) and the real standards that use them (Ethernet, Wi-Fi).

**What the endsem asks from here:** Q3 every year. Expect one theory question on Wi-Fi (RTS/CTS, hidden/exposed terminals, CSMA/CA) and one numerical (ALOHA throughput, CSMA/CD frame size, TDM slots). 2025 asked all three types.

---

## 1. The channel allocation problem · Quick

Picture a classroom where everyone wants to speak and there's one microphone. Two ways to share it:

- **Static allocation:** split the channel permanently. **FDM** gives each user a frequency band; **TDM** gives each user a fixed time slot in turn. Fair and collision-free, but wasteful: an idle user's share sits empty, and bursty data traffic is mostly idle.
- **Dynamic allocation:** give the channel to whoever needs it right now. Efficient for bursty traffic, but two stations may talk at once: a **collision**. The protocols below are about handling that.

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

---

## 2. ALOHA · Slow down

The simplest random access: **just send whenever you have data**. If there's a collision (no ACK), wait a random time and resend. Invented for radio links between Hawaiian islands.

**Vulnerable time** is the window during which another transmission would collide with yours.

| | Pure ALOHA | Slotted ALOHA |
| --- | --- | --- |
| When you may send | Any time | Only at the start of a time slot |
| Vulnerable time | $2T$ (T = frame time) | $T$ |
| Throughput | $S = G e^{-2G}$ | $S = G e^{-G}$ |
| Maximum | 18.4% at $G = 0.5$ | 36.8% at $G = 1$ |

Here **G** = average number of frames attempted (new + retransmitted) **per frame time**, and **S** = average number of *successful* frames per frame time.

Why does slotting double the best throughput? In pure ALOHA a frame can be hit by one that started up to T before it *or* up to T after it; slots remove the "partly overlapping" cases, halving the danger zone.

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

---

## 3. CSMA · Quick

**Carrier Sense Multiple Access:** listen before you talk. If the channel is busy, don't transmit. Collisions still happen because of propagation delay (two stations sense "idle" at nearly the same moment).

| Variant | Channel busy → | Channel idle → | Feel |
| --- | --- | --- | --- |
| **1-persistent** | Keep listening | Send immediately (probability 1) | Greedy: many collisions when busy |
| **Non-persistent** | Wait a random time, then sense again | Send | Fewer collisions, more delay |
| **p-persistent** (slotted) | Wait for next slot | Send with probability p, else wait a slot | Balance |

---

## 4. CSMA/CD (Ethernet) · Slow down

**CSMA with Collision Detection:** listen before sending, and **keep listening while sending**. If you hear a collision, stop at once, send a short **jam signal** so everyone knows, then wait using **binary exponential backoff** (after the k-th collision, wait a random number of slots between 0 and $2^k - 1$).

**Minimum frame size:** a sender must still be transmitting when news of a collision comes back from the far end, or it would never know. The worst case is $2T_p$ (there and back), so:

```latex
T_t \ge 2T_p \quad\Rightarrow\quad L_{min} = 2 \times T_p \times B
```

Example (2024 endsem): 100 Mbps, 1 km cable, minimum frame 1250 bytes. Find the signal speed.

```latex
\begin{aligned}
T_t &= \frac{1250 \times 8}{10^8} = 100\ \mu s = 2T_p \;\Rightarrow\; T_p = 50\ \mu s \\
v &= \frac{1 \text{ km}}{50 \times 10^{-6} \text{ s}} = 20{,}000 \text{ km/s}
\end{aligned}
```

**Signal speed = 20,000 km/s.** (Classic Ethernet's 64-byte minimum comes from the same rule.)

CSMA/CD doesn't work for Wi-Fi: a radio can't hear while it transmits (its own signal drowns everything), and some collisions happen at the receiver where the sender can't hear them anyway. Hence CSMA/CA below.

---

## 5. Collision-free protocols · Quick

No collisions at all, by agreeing an order.

- **Bitmap (reservation):** a short contention period of N bit-slots; station j sets bit j if it wants to send. Then the stations that reserved transmit in order.
- **Token passing:** a special frame (the **token**) circulates; only its holder may transmit. Used in Token Ring (802.5) and Token Bus (802.4).
- **Binary countdown:** stations broadcast their address bit by bit; a station drops out when it sends a 0 and hears a 1. The highest address wins. Gives higher addresses higher priority.

---

## 6. IEEE LAN standards · Quick

IEEE 802 splits the data link layer into **LLC** (logical link control, 802.2: common interface upwards) and **MAC** (different per LAN type).

| Standard | Name | Access method | Topology |
| --- | --- | --- | --- |
| 802.3 | Ethernet | CSMA/CD | Bus / star |
| 802.4 | Token Bus | Token passing | Bus (logical ring) |
| 802.5 | Token Ring | Token passing | Ring |
| 802.6 | DQDB (MAN) | Distributed queue | Dual bus |
| 802.11 | Wireless LAN | CSMA/CA | Wireless |

**Ethernet (802.3) frame:** `Preamble (7) | SFD (1) | Dest MAC (6) | Src MAC (6) | Length/Type (2) | Data (46–1500) | CRC (4)`. Minimum frame 64 bytes, maximum 1518.

**High-speed LANs:** Fast Ethernet (100 Mbps, 100Base-TX), Gigabit Ethernet (1 Gbps, full duplex with switches so CSMA/CD is barely needed), 10 Gigabit Ethernet (full duplex only), and FDDI (100 Mbps dual counter-rotating fibre token rings, survives a cable break).

---

## 7. Wireless LAN, IEEE 802.11 · Slow down

Wi-Fi uses **CSMA/CA** (Collision **Avoidance**): since you can't detect collisions while sending, try hard to avoid them, and use ACKs to confirm success.

**How CSMA/CA works:**

1. Sense the channel. If idle for a **DIFS** (DCF inter-frame space), get ready.
2. Pick a random **backoff** and count down only while the channel is idle (freeze when busy).
3. At zero, send the frame.
4. The receiver waits a short **SIFS** and sends an **ACK**. No ACK means assume a collision: double the backoff range and retry.

**Inter-frame spacing = priority by waiting time.** Shorter wait wins the channel: **SIFS** (shortest: ACK, CTS, next fragment) < **PIFS** (point coordinator, PCF) < **DIFS** (normal data). So an ACK can never be interrupted by a new data frame.

**Virtual carrier sensing (NAV):** every frame carries a *duration* field. Other stations set their **NAV** (Network Allocation Vector) timer to it and treat the channel as busy until it expires, even if they can't hear the carrier. It's like a "Meeting in progress until 3:40" sign on a door.

### Hidden and exposed terminals

- **Hidden terminal:** A and C both talk to B, but A and C are out of each other's range. A senses idle, C senses idle, both send to B, and **they collide at B**. Carrier sensing failed because the sender can't hear the other sender.
- **Exposed terminal:** B is sending to A. C (in range of B) wants to send to D (far from B). C hears B and **wrongly stays silent**, though C → D would not have disturbed A at all. Wasted opportunity.

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

---

## 8. Quick recap

- Static (FDM/TDM) wastes idle shares; dynamic risks collisions.
- Pure ALOHA $S = Ge^{-2G}$ (max 18.4%); slotted $S = Ge^{-G}$ (max 36.8%).
- CSMA: 1-persistent, non-persistent, p-persistent.
- CSMA/CD: listen while sending, jam, binary exponential backoff; $L_{min} = 2 T_p B$.
- Collision-free: bitmap, token passing, binary countdown.
- 802.3 Ethernet (CSMA/CD), 802.4 token bus, 802.5 token ring, 802.11 Wi-Fi (CSMA/CA).
- Wi-Fi: IFS priority SIFS < PIFS < DIFS; NAV = virtual carrier sense; RTS/CTS fixes hidden, not exposed.
