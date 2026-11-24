# CN Unit 5: Routing Algorithms, Delivery and Forwarding

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** routers build tables that say "for this destination, send it out of that link"; **routing** is how those tables get built (Dijkstra / link state, Bellman-Ford / distance vector, BGP between organisations), and **forwarding** is using the table to push each packet one hop onward.

**What the endsem asks from here:** Q5 every year. A graph numerical is guaranteed (build a routing table with Dijkstra or distance vector, or count unused links), plus one theory comparison (OSPF vs BGP, static vs dynamic, hierarchical routing). 2025 asked all three.

---

## 1. Routing vs forwarding, delivery · Quick

- **Forwarding:** what a router does with each arriving packet: look up the destination in the table, send it out the right interface. Fast, per packet.
- **Routing:** the background process of building and updating that table. Slow, ongoing.
- **Delivery:** **direct** delivery when the destination is on the same network as the sender (just use ARP and send the frame); **indirect** when it goes through one or more routers (only the last router delivers directly).

**Forwarding techniques:** next-hop method (the table stores only the next router, not the full route), network-specific (one entry per network, not per host), host-specific, and **default route** (0.0.0.0/0, "everything else goes here"). With CIDR, the router picks the **longest prefix match**: the most specific entry that matches.

---

## 2. Static vs dynamic routing · Quick

| | Static routing | Dynamic routing |
| --- | --- | --- |
| Table built by | The administrator, by hand | Routing protocols, automatically |
| Adapts to failures | No (someone must edit it) | Yes, recalculates |
| Overhead | None (no routing messages) | Bandwidth and CPU for updates |
| Suits | Small, stable networks; default routes | Large or changing networks |
| Examples | `ip route` commands | RIP, OSPF, BGP |

---

## 3. Dijkstra and link state routing · Slow down

In **link state routing**, every router learns the **entire map**: each router floods a small packet (a **Link State Packet**: "I am B, my neighbours are A at cost 4, C at 3…") to all routers. With the full map, each router runs **Dijkstra's shortest-path algorithm** with itself as the source. Like everyone having the same Google Maps and finding their own best routes.

**Dijkstra, in plain steps:**

1. Distance to the source is 0, to everyone else ∞.
2. Pick the **closest unfinished** node; mark it finished (its distance is now final).
3. **Relax** its neighbours: if going through it gives a shorter distance, update them (and remember it as the previous hop).
4. Repeat until all nodes are finished. The **next hop** for each destination is the first node on its path.

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

---

## 4. Distance vector routing · Slow down

In **distance vector (DV)** routing, a router does **not** know the map. It only knows its neighbours, and periodically tells each of them its whole table: "here's how far I am from everyone". Each router then uses the **Bellman-Ford** rule:

```latex
D_x(y) = \min_{v \in \text{neighbours}} \{\, c(x, v) + D_v(y) \,\}
```

In words: my distance to y = the best over my neighbours v of (cost to reach v + v's claimed distance to y). Like asking friends "how far is the station from you?" and adding how far you are from each friend.

**Example (2024 endsem, Tanenbaum's network):** router C receives vectors (for destinations A, B, C, D, E, F) from B: (5, 0, 8, 12, 6, 2), from D: (16, 12, 6, 0, 9, 10), from E: (7, 6, 3, 9, 0, 4). C's link delays: to B 6, to D 3, to E 5.

| Dest | via B (6 + …) | via D (3 + …) | via E (5 + …) | Best | Line |
| --- | --- | --- | --- | --- | --- |
| A | 11 | 19 | 12 | **11** | B |
| B | 6 | 15 | 11 | **6** | B |
| C | – | – | – | **0** | – |
| D | 18 | 3 | 14 | **3** | D |
| E | 12 | 12 | 5 | **5** | E |
| F | 8 | 13 | 9 | **8** | B |

**C's new table: (11, 6, 0, 3, 5, 8) via (B, B, –, D, E, B).**

**The count-to-infinity problem:** good news (a shorter path) spreads fast, but **bad news** (a link going down) spreads slowly, because routers keep believing each other's stale claims and bump the distance up by one per exchange, possibly forever. Fixes: a maximum hop count (RIP uses 16 = infinity), **split horizon** (don't advertise a route back to the neighbour you learnt it from), and **poison reverse** (advertise it back as infinity).

**RIP (Routing Information Protocol)** is the classic DV protocol: metric = **hop count**, maximum 15 (16 = unreachable), tables sent every **30 s**, runs over UDP port 520. Simple but slow to converge and only for small networks.

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

---

## 5. Link state vs distance vector · Quick

| | Distance vector | Link state |
| --- | --- | --- |
| Knows | Only neighbours' distance claims | The whole topology |
| Shares | Its whole table, with neighbours only | Its links, flooded to everyone |
| Algorithm | Bellman-Ford | Dijkstra |
| Updates | Periodic | On change |
| Convergence | Slow, count-to-infinity | Fast |
| Resources | Light on CPU/memory | More memory and CPU |
| Protocol | RIP | OSPF |

---

## 6. Hierarchical routing · Quick

As networks grow, every router keeping an entry for every other router becomes impossible. Split routers into **regions** (and regions into clusters): a router knows every router in its **own region**, but only one entry per *other* region. Exactly how postal addresses work: the Delhi post office doesn't know every house in Chennai, just "send to Chennai".

**Example (2024 endsem):** 720 routers; three levels: 8 clusters × 9 regions × 10 routers.

```latex
\text{Entries} = \underbrace{10}_{\text{own region}} + \underbrace{(9 - 1)}_{\text{other regions, own cluster}} + \underbrace{(8 - 1)}_{\text{other clusters}} = 25
```

**25 entries instead of 720.** The price is slightly longer (non-optimal) paths. OSPF areas and BGP's autonomous systems are real-world hierarchical routing.

---

## 7. BGP and inter-domain routing · Slow down

The Internet is a network of **autonomous systems (ASes)**: networks each run by one organisation (an ISP, a university, Google), with its own AS number. Routing **inside** an AS uses an **interior** protocol (RIP, OSPF); routing **between** ASes uses the **exterior** protocol **BGP (Border Gateway Protocol)**.

BGP is a **path vector** protocol: routers advertise the **full AS path** to each destination (e.g. "to 8.8.8.0/24: AS100 → AS15169"), not just a distance. Two flavours: **eBGP** between border routers of different ASes, **iBGP** to share those routes inside an AS. It runs over **TCP port 179** and sends incremental updates.

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

---

## 8. Multicast routing · Quick

**Multicast** sends one stream to a **group** of receivers (address 224/4) without sending separate copies from the source. Routers build a **distribution tree** and copy the packet only where branches split.

- **Source-based trees:** one shortest-path tree per source (e.g. **DVMRP**, using reverse path forwarding: accept a packet only if it came in on the interface leading back to the source; and **MOSPF**). Efficient paths, but many trees.
- **Group-shared trees:** one tree per group rooted at a core / rendezvous point (e.g. **CBT**, **PIM-SM**). Fewer trees, slightly longer paths.
- **IGMP** lets hosts tell their local router which groups they want to join.

---

## 9. The IPv4 datagram and fragmentation · Quick

**IPv4 header (20–60 bytes):** Version (4), Header length, Type of service, Total length, **Identification, Flags (DF, MF), Fragment offset** (for fragmentation), **TTL** (decremented each hop; dropped at 0, so loops can't go on forever), Protocol (6 = TCP, 17 = UDP), Header checksum, Source IP, Destination IP, Options.

**Fragmentation:** if a datagram is bigger than the next link's **MTU**, the router splits it. Each fragment gets its own header; the data in each fragment (except the last) must be a **multiple of 8 bytes**, because the offset is counted in 8-byte units. **MF = 1** on all but the last fragment. Only the final destination reassembles.

Example (2024 endsem): a 1000-byte datagram (20-byte header, so 980 bytes of data) meets an MTU of 100 bytes.

```latex
\begin{aligned}
\text{Data per fragment} &= 100 - 20 = 80 \text{ bytes (a multiple of 8)} \\
\text{Fragments} &= \lceil 980 / 80 \rceil = 13 \quad (12 \times 80 = 960) \\
\text{Last fragment} &= 20 \text{ bytes of data} + 20 \text{ header} = 40 \text{ bytes}
\end{aligned}
```

**13 fragments; the last one is 40 bytes.**

---

## 10. Quick recap

- Forwarding = use the table per packet (longest prefix match); routing = build the table.
- Static: manual, no adaptation; dynamic: protocols, adapts.
- Link state: flood LSPs, everyone has the map, Dijkstra (OSPF, areas).
- Distance vector: Bellman-Ford with neighbours' vectors (RIP: hops, max 15, 30 s); count-to-infinity, fixed by split horizon / poison reverse.
- Hierarchical routing: own region in full + one entry per other region/cluster.
- BGP: path vector between ASes, policy-driven, hides internals, TCP 179.
- Multicast: source-based trees (DVMRP, MOSPF) vs shared trees (CBT, PIM-SM); IGMP for membership.
- Fragment data in multiples of 8 bytes; MF flag; offset in 8-byte units.
