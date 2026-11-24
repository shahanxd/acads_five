# CN Unit 2: The Data Link Layer

*Endsem RUN · about 70 minutes*

**The whole unit in one breath:** the physical layer just throws bits on a wire; the data link layer turns them into **frames**, catches **errors**, and makes sure a fast sender doesn't drown a slow receiver (**flow control**), resending what got lost (**ARQ**).

**What the endsem asks from here:** Q2 is always this unit, and it's numerical-heavy: framing/stuffing, CRC, checksum, Hamming, and sliding-window efficiency. 2025 asked Go-Back-N theory, framing with stuffing, and a window-size-for-50%-utilization numerical.

---

## 1. Design issues · Quick

The data link layer gives the network layer a "nice" link. Its jobs:

1. **Framing:** split the bit stream into frames with clear boundaries.
2. **Error control:** detect (and sometimes correct) bit errors; resend damaged frames.
3. **Flow control:** stop a fast sender overwhelming a slow receiver.
4. **Services to the network layer:** unacknowledged connectionless (Ethernet), acknowledged connectionless (Wi-Fi), acknowledged connection-oriented.
5. **Physical addressing** (MAC) and, on shared links, medium access (the MAC sublayer, Unit 3).

---

## 2. Framing · Slow down

The receiver sees an endless river of 0s and 1s. How does it know where one frame ends and the next starts? Framing adds the "punctuation".

| Method | How it works | Problem |
| --- | --- | --- |
| **Character count** | The first byte says how many bytes the frame has (counting itself) | If the count gets corrupted, the receiver loses sync for every later frame |
| **Flag bytes + byte stuffing** | Frame starts and ends with a special FLAG byte. If FLAG or ESC appears in the data, put an ESC before it | Tied to 8-bit characters; overhead with many FLAG/ESC |
| **Flag bits + bit stuffing** | Frame starts and ends with `01111110`. In the data, after **five consecutive 1s, insert a 0**. The receiver deletes any 0 that follows five 1s | Small overhead; works with any bit length |
| Physical layer coding violations | Use signal patterns that never occur in data | Needs special encoding |

Why insert a 0 after five 1s? The flag has **six** 1s in a row. Stuffing guarantees the data never contains six 1s, so the flag can't appear by accident.

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

---

## 3. Error detection: parity and checksum · Quick

Noise flips bits. Errors are **single-bit** (one bit flipped) or **burst** (several bits in a row, the common case).

**Parity:** add one bit so the number of 1s is even (even parity). Detects any odd number of errors, misses even numbers. **2-D parity** (rows and columns) detects more and can correct single errors.

**Checksum (Internet checksum):** split data into 16-bit words, add them in **1's complement** arithmetic (wrap any carry back into the sum), and send the **complement** of the sum. The receiver adds everything including the checksum; the result's complement must be **0**.

Example: words `0x4365, 0xABD1, 0x02BC, 0x35FE`.

```latex
\begin{aligned}
\text{4365 + ABD1} &= \text{EF36} \\
\text{EF36 + 02BC} &= \text{F1F2} \\
\text{F1F2 + 35FE} &= \text{127F0} \;\rightarrow\; \text{27F0 + 1} = \text{27F1} \\
\text{checksum} &= \sim\text{27F1} = \text{D80E}
\end{aligned}
```

**Checksum = 0xD80E.** At the receiver, 27F1 + D80E = FFFF, whose complement is 0000: no error.

---

## 4. CRC · Slow down

CRC (cyclic redundancy check) is the strong one, used in Ethernet. The idea: treat bits as a polynomial and divide by an agreed **generator**; send the remainder along so the whole thing divides exactly.

**Steps (generator of degree r, i.e. r + 1 bits):**

1. Append **r zeros** to the message.
2. Divide by the generator using **XOR** (modulo-2: no carries, no borrows).
3. The **r-bit remainder** is the CRC; replace the appended zeros with it and send.
4. Receiver divides the received bits by the same generator: remainder **0 = no error**, non-zero = error.

Example: generator $x^3 + x + 1$ = `1011` (r = 3), message `11000`.

Each step XORs the generator under the leftmost remaining 1:

```
11000000      message 11000 + three zeros
1011
--------
01110000
 1011
--------
00101000
  1011
--------
00000100      remainder = last 3 bits = 100
```

**Transmitted = 11000 100.** At the receiver, `11000100 ÷ 1011` leaves remainder `000`, so it's accepted. If a bit flips on the way (say the third bit, giving `11100100`), the remainder comes out non-zero, so the error is detected.

CRC catches all single-bit errors, all double errors (with a good generator), all odd numbers of errors (if the generator has factor $x+1$), and all bursts up to r bits long.

---

## 5. Hamming code: error correction · Slow down

Detection says "something's wrong"; **correction** says "bit 6 is wrong, flip it". Hamming code puts parity bits at positions **1, 2, 4, 8 …** (powers of 2). Each parity bit checks the positions whose binary number contains that power of 2:

| Parity bit | Checks positions |
| --- | --- |
| P1 | 1, 3, 5, 7, 9, 11 (binary ends in 1) |
| P2 | 2, 3, 6, 7, 10, 11 |
| P4 | 4, 5, 6, 7, 12 |
| P8 | 8, 9, 10, 11, 12 |

**Number of parity bits r** for m data bits: smallest r with $2^r \ge m + r + 1$. For 7 data bits, r = 4 (11-bit code); for 8 data bits, r = 4 (12-bit code).

**At the receiver:** recompute each parity check. Write the failing checks as a binary number (P8 P4 P2 P1): that number is the **position of the wrong bit**. 0 means no error.

Example: in a 7-bit code word, checks P4 and P2 fail and P1 passes → syndrome = 110 = **6**, so bit 6 is flipped; correct it and drop the parity bits.

---

## 6. Flow control and Stop-and-Wait · Slow down

The two delays everything is built from:

```latex
\begin{aligned}
T_t &= \frac{\text{frame size (bits)}}{\text{bandwidth (bits/s)}} && \text{(transmission time: pushing the bits out)} \\
T_p &= \frac{\text{distance}}{\text{signal speed}} && \text{(propagation time: travelling the wire)} \\
a &= \frac{T_p}{T_t}
\end{aligned}
```

**Stop-and-Wait:** send one frame, then wait for its ACK before sending the next. Like a shopkeeper who serves one customer, walks them to the door, and only then calls the next.

```latex
\eta_{\text{SW}} = \frac{T_t}{T_t + 2T_p} = \frac{1}{1 + 2a}
```

Utilization is worst when $a$ is big: **long links and high bandwidth** (the sender finishes sending quickly and then waits ages). That was a 2024 MCQ: answer "longer link, higher transmission rate".

**Stop-and-Wait ARQ** adds error recovery: a **timer** (resend if no ACK in time), **1-bit sequence numbers** (0/1) so a resent frame isn't mistaken for a new one, and numbered ACKs.

---

## 7. Sliding window · Slow down

Fix for Stop-and-Wait's waiting: let the sender have **W frames in flight** before needing an ACK. While the first ACK is on its way back, the sender keeps sending.

```latex
\eta = \frac{W \cdot T_t}{T_t + 2T_p} \quad (\text{capped at } 1), \qquad \text{for 100\%: } W \ge 1 + 2a
```

With **n-bit sequence numbers**, numbers run 0 to $2^n - 1$ and wrap around.

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

---

## 8. Go-Back-N and Selective Repeat · Slow down

Both are sliding-window ARQ. The difference is how they handle a lost frame.

**Go-Back-N (GBN):** the receiver accepts frames **only in order** (receiver window = 1). If frame 3 is lost, it discards 4, 5, 6 even if they arrive fine. The sender times out on 3 and **goes back**, resending 3, 4, 5, 6. Simple receiver, wasted bandwidth. ACKs are **cumulative** (ACK 5 means "everything up to 4 received").

**Selective Repeat (SR):** the receiver **buffers** out-of-order frames and asks only for the missing one (NAK / individual ACKs). Only frame 3 is resent. Efficient, but needs buffers and more logic.

| | Stop-and-Wait | Go-Back-N | Selective Repeat |
| --- | --- | --- | --- |
| Sender window | 1 | $2^n - 1$ | $2^{n-1}$ |
| Receiver window | 1 | 1 | $2^{n-1}$ |
| On a loss, resend | That frame | That frame and **all after it** | **Only** that frame |
| Receiver buffering | No | No | Yes |
| ACKs | Individual | Cumulative | Individual |
| Efficiency | Lowest | Medium | Highest |

> **Endsem 2025 · Q2(a) · 4.5 marks**
> In Go-Back-N ARQ, explain why the sender's window size is $2^n - 1$, while the receiver's window size is limited to 1. Describe how the protocol handles (i) duplicate frames, (ii) lost frames, (iii) lost acknowledgments.

**Answer.**

**Why sender window = $2^n - 1$:** with n bits, sequence numbers are 0 to $2^n - 1$, i.e. $2^n$ numbers. Suppose n = 2 (numbers 0–3) and the window were 4. The sender sends 0, 1, 2, 3, and **all four ACKs are lost**. The receiver, having received them, now expects 0 (the next round). The sender times out and resends the old 0. The receiver accepts this **old frame as a new one**: a duplicate gets through, which is a silent error. With the window at $2^n - 1$ = 3 (frames 0, 1, 2), the receiver then expects 3, so a resent 0 is recognised as a duplicate and discarded. Keeping one number unused removes the ambiguity.

**Why receiver window = 1:** GBN accepts frames **strictly in order**. The receiver only ever waits for one specific sequence number, the next expected one, and discards anything else. So it needs space for just one frame, which keeps the receiver simple (no buffering, no reordering).

**(i) Duplicate frames:** the frame's sequence number isn't the expected one, so the receiver **discards** it and re-sends an ACK for the last in-order frame (so the sender learns where it stands).

**(ii) Lost frame:** say frame 2 is lost. Frames 3, 4 … arrive out of order and are **discarded**. No ACK for 2 arrives, so the sender's **timer for frame 2 expires** and it **goes back**, resending 2 and every frame after it.

**(iii) Lost acknowledgment:** ACKs are **cumulative**, so if ACK 2 is lost but ACK 4 arrives, ACK 4 confirms frames up to 3 as well; nothing is resent. If all ACKs for the window are lost, the timer expires, the sender resends the window, and the receiver discards those as duplicates while re-ACKing.

**Sender window 2ⁿ − 1 stops an old frame being taken as new after a wrap; receiver window 1 because GBN accepts only in order. Duplicates are discarded, a lost frame makes the sender go back N, and a lost ACK is covered by a later cumulative ACK or a timeout.**

---

## 9. HDLC · Quick

**HDLC (High-Level Data Link Control)** is a classic bit-oriented data link protocol (ISO standard); PPP and Ethernet's LLC come from it.

- **Frame:** `Flag (01111110) | Address | Control | Information | FCS (CRC) | Flag`. Uses **bit stuffing**.
- **Three frame types** (decided by the control field): **I-frames** (information: user data + piggybacked ACK), **S-frames** (supervisory: RR receive ready, RNR receive not ready, REJ reject = Go-Back-N, SREJ selective reject = Selective Repeat), **U-frames** (unnumbered: link setup/teardown like SABM, DISC, UA).
- **Station types:** primary, secondary, combined. **Modes:** NRM (normal response, primary polls), ABM (asynchronous balanced, combined stations, most common), ARM.

---

## 10. Quick recap

- Framing: character count, byte stuffing (ESC before FLAG/ESC), bit stuffing (0 after five 1s).
- Checksum: 1's complement sum, then complement; receiver gets 0.
- CRC: append r zeros, XOR-divide, remainder replaces zeros; receiver remainder 0 = OK.
- Hamming: parity at 1, 2, 4, 8; failing checks spell the wrong bit's position.
- $\eta_{SW} = 1/(1+2a)$; sliding window $\eta = W T_t / (T_t + 2T_p)$.
- GBN: sender $2^n-1$, receiver 1, resend from the lost one. SR: both $2^{n-1}$, resend only the lost one.
- HDLC: I, S, U frames; bit stuffing; REJ = GBN, SREJ = SR.
