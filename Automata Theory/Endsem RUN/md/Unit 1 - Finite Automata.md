# Automata Unit 1: Finite Automata

*Endsem RUN · about 60 minutes*

**The whole unit in one breath:** a finite automaton is a machine with a **fixed, finite memory** (its current state) that reads a string one symbol at a time and says yes or no at the end. DFAs follow exactly one path, NFAs may branch, and both recognise exactly the same languages; we can convert NFA → DFA and shrink a DFA to its minimum size. Mealy and Moore machines are automata that produce **output**.

**What the endsem asks from here:** NFA → DFA conversion and DFA minimisation (both numerical, both in 2025), plus theory on state diagrams/tables and Mealy/Moore. 2025's whole Q1.

---

## 1. Basic terms · Quick

| Term | Meaning | Example |
| --- | --- | --- |
| **Alphabet** Σ | A finite, non-empty set of symbols | Σ = {0, 1} |
| **String** | A finite sequence of symbols from Σ | 0110; **ε** = the empty string (length 0) |
| **Length** \|w\| | Number of symbols | \|0110\| = 4 |
| **Σ\*** | All strings over Σ, including ε | {ε, 0, 1, 00, 01, …} |
| **Σ⁺** | Σ\* without ε | |
| **Language** | Any set of strings over Σ (a subset of Σ\*) | L = {strings ending in 1} |

**Graphs and trees** appear because an automaton is drawn as a **directed graph** (states = nodes, transitions = labelled edges), and derivations later are **trees** (a connected graph with no cycles, one root).

---

## 2. DFA, state diagrams and state tables · Slow down

**A DFA (deterministic finite automaton)** is a 5-tuple $M = (Q, \Sigma, \delta, q_0, F)$: a finite set of **states** Q, an **alphabet** Σ, a **transition function** $\delta: Q \times \Sigma \to Q$ (exactly one next state for every state and symbol), a **start state** $q_0$, and a set of **final (accepting) states** F ⊆ Q.

It's like a turnstile at the metro: it's always in exactly one state (locked/unlocked), each input (coin/push) moves it to exactly one next state, and it remembers nothing else.

The DFA **accepts** w if, starting at $q_0$ and following w symbol by symbol, it ends in a final state. The **language** of M is the set of all strings it accepts.

> **Endsem 2025 · Q1(a) · 4.5 marks**
> Explain the role of state diagrams and state tables in representing finite automata. How does each representation help in understanding the behaviour of the automaton?

**Answer.**

A finite automaton is the 5-tuple (Q, Σ, δ, q₀, F); the transition function δ is its behaviour. **State diagrams and state tables are two equivalent ways of writing δ** (together with the start and final states), one visual and one tabular.

**State (transition) diagram:** a directed graph in which

- each **state** is a circle labelled with its name;
- each **transition** δ(p, a) = q is an arrow from p to q labelled a;
- the **start state** has an incoming arrow from nowhere;
- **final states** are double circles.

Example: a DFA over {0, 1} accepting strings that **end in 1**:

```
        0                1
      ┌───┐            ┌───┐
      v   │     1      v   │
 --> (q0) ────────>  ((q1))
       ^                │
       └───────0────────┘
```

**How it helps:** you can **see** the behaviour at a glance: follow the arrows for any input string, spot loops (repetition), dead states and unreachable states, and understand the pattern being recognised ("whenever a 1 arrives, we're in the accepting state"). Best for **design and intuition**.

**State (transition) table:** a table with one **row per state**, one **column per input symbol**, and each cell = the next state. The start state is marked → and final states \*.

| State | 0 | 1 |
| --- | --- | --- |
| → q0 | q0 | q1 |
| \* q1 | q0 | q1 |

**How it helps:** it is **complete and precise**: you can check that every state has a transition for every symbol (DFA condition), compute runs mechanically, and it is the form used by **algorithms**: NFA → DFA conversion, minimisation, and computer implementation (a 2-D array lookup). Best for **analysis and computation**.

| State diagram | State table |
| --- | --- |
| Graphical | Tabular |
| Intuitive; shows paths, loops, structure | Precise; easy to check completeness |
| Good for design and small machines | Good for algorithms, large machines, programs |
| Hard to read when there are many states | Hard to "see" the pattern |

**Both represent the same transition function: the diagram gives intuition about how strings move through states; the table gives a precise, checkable form for conversion, minimisation and implementation.**

---

## 3. NFA and NFA → DFA · Slow down

**An NFA (non-deterministic finite automaton)** is the same 5-tuple, except $\delta: Q \times \Sigma \to 2^Q$: from a state, a symbol may lead to **several** states, or **none**. (An ε-NFA also allows moves on ε, without reading input.) The NFA accepts w if **at least one** path ends in a final state. Picture it as cloning yourself at every fork and accepting if any clone wins.

**NFAs are not more powerful than DFAs:** every NFA has an equivalent DFA (Rabin–Scott). The DFA just keeps track of **the set of states** the NFA could be in. That's the **subset construction**:

1. The DFA's start state = {start state of the NFA}.
2. For each new DFA state S (a set) and each symbol a: next state = the union of δ(q, a) over all q in S.
3. Repeat until no new sets appear. (∅ becomes a dead state if it appears.)
4. A DFA state is final if it **contains** an NFA final state.

> **Endsem 2025 · Q1(b) · 4.5 marks**
> Given an NDFA with states {q0, q1, q2}, alphabet {0, 1}: δ(q0, 0) = {q0, q1}, δ(q0, 1) = {q0}, δ(q1, 1) = {q2}, δ(q2, 0) = {q2, q1}; q0 initial, q2 final. Convert it to its equivalent DFA and give the state table.

**Answer.**

**NFA table** (missing entries are ∅):

| State | 0 | 1 |
| --- | --- | --- |
| → q0 | {q0, q1} | {q0} |
| q1 | ∅ | {q2} |
| \* q2 | {q1, q2} | ∅ |

**Subset construction**, starting from [q0]:

| DFA state | on 0 | on 1 |
| --- | --- | --- |
| [q0] | δ(q0,0) = {q0, q1} → **[q0, q1]** (new) | δ(q0,1) = {q0} → [q0] |
| [q0, q1] | {q0, q1} ∪ ∅ = [q0, q1] | {q0} ∪ {q2} → **[q0, q2]** (new) |
| [q0, q2] | {q0, q1} ∪ {q1, q2} → **[q0, q1, q2]** (new) | {q0} ∪ ∅ = [q0] |
| [q0, q1, q2] | {q0, q1} ∪ ∅ ∪ {q1, q2} = [q0, q1, q2] | {q0} ∪ {q2} ∪ ∅ = [q0, q2] |

No new states appear, so we stop. Final states = those containing q2: [q0, q2] and [q0, q1, q2].

**DFA state table** (renaming A = [q0], B = [q0, q1], C = [q0, q2], D = [q0, q1, q2]):

| State | 0 | 1 |
| --- | --- | --- |
| → A = [q0] | B | A |
| B = [q0, q1] | B | C |
| \* C = [q0, q2] | D | A |
| \* D = [q0, q1, q2] | D | C |

**Check with strings:**

| String | DFA run | Result | NFA reason |
| --- | --- | --- | --- |
| 01 | A → B → C | Accept | path q0 → q1 → q2 |
| 010 | A → B → C → D | Accept | q0 → q1 → q2 → q2 |
| 011 | A → B → C → A | Reject | the path in q2 dies on 1 (δ(q2, 1) = ∅); every other path is in q0 or q1 |
| 1 | A → A | Reject | only q0 is reachable |

**The equivalent DFA has 4 states: [q0], [q0,q1], [q0,q2]\*, [q0,q1,q2]\*, with the table above.**

---

## 4. DFA minimisation · Slow down

Two states are **equivalent** if, for every input string, they both lead to acceptance or both to rejection. Merging equivalent states gives the **minimum DFA** (unique up to renaming).

**Partition (Myhill–Nerode / Moore) method:**

1. Remove unreachable states.
2. **0-equivalence:** split into two groups: final and non-final.
3. **k-equivalence:** within each group, two states stay together only if, for **each** symbol, they go into the **same group** of the previous partition. Split otherwise.
4. Repeat until a partition doesn't change. Each group becomes one state.

> **Endsem 2025 · Q1(c) · 4.5 marks**
> Minimise the DFA over {0, 1}: A (0→B, 1→C, non-final), B (0→A, 1→D, non-final), C (0→E, 1→F, final), D (0→E, 1→F, non-final), E (0→E, 1→F, final), F (0→F, 1→F, non-final), with A the start state. Verify your answer using suitable strings.

**Answer.**

**Reachability:** from A we reach B, C; from B: D; from C: E, F. All six states are reachable.

**0-equivalence (final vs non-final):** P₀ = { {C, E}, {A, B, D, F} }.

**1-equivalence:** check where each state goes, by group of P₀ (G1 = {C, E} final, G2 = {A, B, D, F}):

| State | on 0 → group | on 1 → group |
| --- | --- | --- |
| C | E → G1 | F → G2 |
| E | E → G1 | F → G2 |
| A | B → G2 | C → **G1** |
| B | A → G2 | D → G2 |
| D | E → **G1** | F → G2 |
| F | F → G2 | F → G2 |

C and E behave alike → stay together. In G2, A (G2, G1), B (G2, G2), D (G1, G2) and F (G2, G2) give three patterns: A alone, D alone, and {B, F} together.

P₁ = { {C, E}, {A}, {D}, {B, F} }.

**2-equivalence:** check B and F against P₁: B –0→ A (group {A}), F –0→ F (group {B, F}). Different, so **split B and F**. C and E: both go 0 → E ({C, E}), 1 → F ({B, F}): still together.

P₂ = { {C, E}, {A}, {B}, {D}, {F} }.

**3-equivalence:** only {C, E} could split: C → (E, F), E → (E, F): identical. No change, so **stop**.

**Minimised DFA** (5 states; CE = merged C and E):

| State | 0 | 1 |
| --- | --- | --- |
| → A | B | CE |
| B | A | D |
| \* CE | CE | F |
| D | CE | F |
| F | F | F |

(F is a **dead/trap state**: once there, never accept.)

**Verification with strings** (original vs minimised give the same answers):

| String | Original run | Minimised run | Result |
| --- | --- | --- | --- |
| 1 | A → C (final) | A → CE | Accept |
| 10 | A → C → E (final) | A → CE → CE | Accept |
| 11 | A → C → F | A → CE → F | Reject |
| 011 | A → B → D → F | A → B → D → F | Reject |
| 010 | A → B → D → E (final) | A → B → D → CE | Accept |
| 001 | A → B → A → C (final) | A → B → A → CE | Accept |

**Only C and E are equivalent; the minimum DFA has 5 states: A, B, {C,E}, D, F.**

---

## 5. Mealy and Moore machines · Quick

Finite automata with **output** instead of accept/reject (e.g. a vending machine, a traffic light controller).

| | Moore machine | Mealy machine |
| --- | --- | --- |
| Output depends on | **Current state only** | **Current state and current input** |
| Output written | Inside each state | On each transition (a/0) |
| Output length for input of length n | n + 1 (includes the start state's output) | n |
| Reacts | One step later | Immediately |
| Tuple | (Q, Σ, Δ, δ, λ, q₀) with λ: Q → Δ | (Q, Σ, Δ, δ, λ, q₀) with λ: Q × Σ → Δ |

**Moore → Mealy:** for each transition δ(p, a) = q, output on that transition = λ(q) (the output of the state it enters). Same number of states.

**Mealy → Moore:** a state q that is entered with **different** outputs must be split into copies (q/0, q/1), one per output; then copy the transitions. The Moore machine may have more states.

Example: Moore machine to count 1s mod 3 (output = remainder): states q0/0, q1/1, q2/2; on 1 move to the next, on 0 stay. Input 1011 → states q0 q1 q1 q2 q0 → output 0 1 1 2 0.

---

## 6. Quick recap

- DFA = (Q, Σ, δ, q₀, F), one next state per symbol; NFA may have many or none.
- State diagram = visual graph (design, intuition); state table = precise grid (algorithms, implementation).
- Subset construction: DFA states are sets of NFA states; final if the set contains an NFA final state.
- 2025 DFA: [q0], [q0,q1], [q0,q2]\*, [q0,q1,q2]\*.
- Minimisation: split final/non-final, refine until stable. 2025: only C ≡ E (5 states).
- Moore: output per state (n + 1 outputs); Mealy: output per transition (n outputs).
