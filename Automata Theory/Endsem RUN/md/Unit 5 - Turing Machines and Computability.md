# Automata Unit 5: Turing Machines and Computability

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** a Turing machine is a finite control with an **infinite tape it can read and write in both directions**. That makes it as powerful as any computer (Church–Turing thesis). Some problems it can always answer (**decidable/recursive**), some it can only confirm "yes" for (**recursively enumerable**), and some it can't handle at all; the **halting problem** is the famous undecidable one.

**What the endsem asks from here:** TM architecture vs PDA, design a TM (aⁿbⁿcⁿ is the favourite), and recursive vs RE vs non-RE. 2025's whole Q5. **The TM below was simulated on every string up to length 7.**

---

## 1. The Turing machine · Slow down

Picture a person with a pencil and eraser, working on an endless strip of paper divided into squares, following a fixed rulebook that only looks at their current "mood" (state) and the one square under their eye. Alan Turing (1936) argued that this captures **everything** that can be computed mechanically.

> **Endsem 2025 · Q5(a) · 4.5 marks**
> Explain the architecture, components and salient features of a Turing Machine. Analyse how it differs from a pushdown automaton in terms of computational power.

**Answer.**

**Architecture:**

```
   ... | B | B | a | a | b | b | B | B | ...      <- infinite tape (cells), B = blank
                     ^
                     |  read/write head (moves L or R one cell per step)
             +--------------------+
             |   finite control   |  current state q, transition function δ
             +--------------------+
```

**Formal definition:** a TM is a 7-tuple **M = (Q, Σ, Γ, δ, q₀, B, F)**:

| Component | Meaning |
| --- | --- |
| Q | Finite set of states |
| Σ | Input alphabet (B ∉ Σ) |
| Γ | Tape alphabet (Σ ⊂ Γ, B ∈ Γ; extra marker symbols like X, Y) |
| δ | Transition function δ: Q × Γ → Q × Γ × {L, R} (partial) |
| q₀ | Start state |
| B | Blank symbol, filling all cells except the input |
| F | Final (accepting/halting) states |

**One move:** δ(q, X) = (p, Y, D): in state q reading X, **write Y**, **move** the head one cell left or right (D), and go to state p. The machine **halts** when no move is defined; it accepts if it halts in a final state. An **instantaneous description** is written like `XaY[q2]bZc` (tape with the state just before the scanned cell).

**Salient features:**

- **Unbounded memory:** an infinite tape, used as both input and working storage.
- **Read and write anywhere:** the head moves both ways, so data can be revisited and modified any number of times.
- **Can loop forever:** on some inputs it may never halt; this is what makes some questions undecidable.
- **Universal:** a **universal TM** can simulate any other TM given its description (the idea of the stored-program computer).
- **Robust:** multi-tape, multi-track, two-way infinite and non-deterministic TMs all have the **same** power as the basic TM (just faster or more convenient).
- **Church–Turing thesis:** anything computable by an algorithm is computable by a TM.
- Recognises Type 0 (recursively enumerable) languages; computes functions (e.g. unary addition: 111 0 11 → 11111).

**TM vs PDA, computational power:**

| Basis | Pushdown automaton | Turing machine |
| --- | --- | --- |
| Memory | Stack: unbounded but **LIFO**, only the top is accessible; **read-only input**, one pass left to right | Tape: unbounded, **random access by moving**; input on the tape, **read and write**, move both ways |
| Languages | Context-free (Type 2) | Recursively enumerable (Type 0), a strict superset |
| Example beyond the other | — | aⁿbⁿcⁿ, ww, a^(2ⁿ) (not context-free) |
| Determinism | NPDA > DPDA | NTM = DTM in power |
| Halting | Always halts on finite input (one pass) | May loop forever |
| Decidability | Membership decidable | Membership undecidable in general (halting problem) |

**Why the TM is stronger:** the PDA can only see its stack top, and popping destroys information, so it can match **one** pair of counts (aⁿbⁿ) but not **two** (aⁿbⁿcⁿ): after using the stack to match a's with b's, the count is gone. A TM can go back and re-read and mark its tape as often as needed, so it can check any number of counts; in fact a PDA with **two** stacks is already as powerful as a TM.

**A TM is a finite control plus an infinite read/write tape with a two-way head, defined by (Q, Σ, Γ, δ, q₀, B, F); its rewritable, revisitable tape makes it strictly more powerful than a PDA (Type 0 vs Type 2 languages).**

---

## 2. Designing a TM for aⁿbⁿcⁿ · Slow down

> **Endsem 2025 · Q5(b) · 4.5 marks**
> Design a Turing machine that accepts L = {aⁿbⁿcⁿ | n ≥ 1}. Verify your answer with suitable examples.

**Answer.**

**Idea (match one a, one b and one c per round):** mark the leftmost unmarked a as X, move right and mark the first unmarked b as Y, move right and mark the first unmarked c as Z, then go back left to the X and repeat. When no a's are left, check that only Y's and Z's remain.

**States:**

- q0: look for an a to mark (or, if only Y's are left, go check the end).
- q1: moving right past a's and Y's to find a b.
- q2: moving right past b's and Z's to find a c.
- q3: moving left back to the last X.
- q4: final check: only Y's and Z's until the blank.
- qf: accept.

**Transition table** (blank = B; empty cell = no move, so the TM halts and rejects):

| State | a | b | c | X | Y | Z | B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| q0 | (q1, X, R) | | | | (q4, Y, R) | | |
| q1 | (q1, a, R) | (q2, Y, R) | | | (q1, Y, R) | | |
| q2 | | (q2, b, R) | (q3, Z, L) | | | (q2, Z, R) | |
| q3 | (q3, a, L) | (q3, b, L) | | (q0, X, R) | (q3, Y, L) | (q3, Z, L) | |
| q4 | | | | | (q4, Y, R) | (q4, Z, R) | (qf, B, R) |
| qf | | | | | | | |

M = ({q0, q1, q2, q3, q4, qf}, {a, b, c}, {a, b, c, X, Y, Z, B}, δ, q0, B, {qf}).

**Verification: aabbcc (accept)**, the state shown just before the scanned symbol:

```
[q0]aabbcc  ->  X[q1]abbcc  ->  Xa[q1]bbcc  ->  XaY[q2]bcc  ->  XaYb[q2]cc
            ->  XaY[q3]bZc  ->  Xa[q3]YbZc  ->  X[q3]aYbZc  ->  [q3]XaYbZc
            ->  X[q0]aYbZc  ->  XX[q1]YbZc  ->  XXY[q1]bZc  ->  XXYY[q2]Zc
            ->  XXYYZ[q2]c  ->  XXYY[q3]ZZ  ->  XXY[q3]YZZ  ->  XX[q3]YYZZ
            ->  X[q3]XYYZZ  ->  XX[q0]YYZZ  ->  XXY[q4]YZZ  ->  XXYY[q4]ZZ
            ->  XXYYZ[q4]Z  ->  XXYYZZ[q4]B ->  XXYYZZB[qf]          ACCEPT
```

**aabbc (reject):** after the first round the tape is XaYbZ…; in the second round q2 passes b and Z and reaches the blank looking for a c: no move for (q2, B), so it halts in a non-final state: **reject** (fewer c's).

**abcc (reject):** after one round, XYZc; q0 sees Y and enters q4, which reads Y, Z and then **c**: no move for (q4, c): **reject** (extra c).

**aabc, abbc, acb, ε (reject):** each gets stuck in a state with no move for the symbol under the head (e.g. q1 sees c with no b, or q0 sees a blank at the start).

(Simulated: the machine accepts exactly the strings aⁿbⁿcⁿ, n ≥ 1, among all strings over {a, b, c} up to length 7.)

**Mark a → X, b → Y, c → Z in rounds, return to the last X, and finally check that only Y's and Z's remain: the TM accepts exactly aⁿbⁿcⁿ (n ≥ 1).**

---

## 3. Non-deterministic TMs and computing functions · Quick

- **Non-deterministic TM (NTM):** δ gives a set of possible moves; it accepts if **any** branch accepts. NTMs are **no more powerful** than DTMs: a DTM can simulate one by trying all branches breadth-first (possibly exponentially slower; that gap is the P vs NP question).
- **TM as a function computer:** the input is written on the tape, and the content when the TM halts is the output. E.g. unary addition: input 111011 (3 + 2), the TM replaces the 0 by 1 and erases the last 1 → 11111 (5).
- **Primitive recursive functions:** built from the basic functions (zero Z(x) = 0, successor S(x) = x + 1, projections) using **composition** and **primitive recursion** (f(x, 0) = g(x), f(x, y + 1) = h(x, y, f(x, y))). Examples: addition, multiplication, factorial, exponentiation. All are **total** and **TM-computable**, but not every computable function is primitive recursive (the **Ackermann function** grows too fast); adding the **μ (minimisation) operator** gives the partial recursive functions, exactly the TM-computable ones.

---

## 4. Recursive, RE and non-RE languages · Slow down

> **Endsem 2025 · Q5(c) · 4.5 marks**
> Analyse the differences between recursive, recursively enumerable and non-recursively enumerable languages. How are these related to Turing machines?

**Answer.**

These classes are defined by **what a Turing machine can do** with the language:

**Recursive (decidable) languages:** there is a TM that **halts on every input**, accepting strings in L and **rejecting** (halting) strings not in L. Such a TM is a **decider**: membership is always answered yes or no. Examples: all regular and context-free languages, aⁿbⁿcⁿ, "is n prime", "does a DFA accept w".

**Recursively enumerable (RE, semi-decidable, Turing-recognisable) languages:** there is a TM that **halts and accepts every string in L**, but on strings **not** in L it may **reject or loop forever**. You'll always hear "yes" eventually, but you may never hear "no". Equivalently, some TM can **enumerate** (list) all strings of L. Example: the halting language **H = {⟨M, w⟩ | M halts on w}**, and A_TM = {⟨M, w⟩ | M accepts w}: just simulate M on w; if it halts/accepts, say yes; if it runs forever, so do we.

**Non-recursively enumerable languages:** **no TM** can even recognise them; for some strings in L, every TM fails to say yes. Example: the **complement of the halting language**, {⟨M, w⟩ | M does **not** halt on w}, and the diagonal language L_d = {wᵢ | the i-th TM does not accept wᵢ}. There are uncountably many languages but only countably many TMs, so most languages are not RE.

**Relationships:**

```
   +------------------------------------------------------------+
   |  All languages                                             |
   |   +--------------------------------------------------+     |
   |   |  Recursively enumerable (TM recognises)          |     |
   |   |     +------------------------------------+       |     |
   |   |     |  Recursive (TM decides, always halts) |    |     |
   |   |     |   CSL ⊃ CFL ⊃ Regular              |       |     |
   |   |     +------------------------------------+       |     |
   |   |   e.g. HALT, A_TM (RE but not recursive)         |     |
   |   +--------------------------------------------------+     |
   |   e.g. complement of HALT, L_d (not RE)                     |
   +------------------------------------------------------------+
```

| | Recursive | RE but not recursive | Not RE |
| --- | --- | --- | --- |
| TM exists that… | always halts (decides) | halts on yes-instances only (recognises) | — none |
| On w ∉ L | halts, rejects | may loop forever | — |
| Also called | Decidable | Semi-decidable, Turing-recognisable | Non-recognisable |
| Example | aⁿbⁿcⁿ, CFL membership | Halting problem, A_TM | Complement of HALT, L_d |
| Closed under complement | **Yes** | **No** | — |

**Key theorems:**

- Recursive ⊂ RE (every decider is a recogniser), and the inclusion is **strict** (HALT is RE but not recursive).
- If both L and its complement are RE, then L is recursive (run both recognisers in parallel; one must halt).
- Hence, if L is RE but not recursive, its complement is **not RE**. (That's why the complement of HALT is non-RE.)
- Recursive languages are closed under union, intersection and complement; RE languages under union and intersection but **not** complement.
- Type 0 grammars generate exactly the RE languages.

**Recursive = decided by a TM that always halts; RE = recognised by a TM that halts on all members but may loop on non-members; non-RE = no TM can recognise it. Recursive ⊂ RE ⊂ all languages; L is recursive iff both L and its complement are RE.**

---

## 5. The halting problem and types of problems · Quick

**Halting problem:** given a TM M and an input w, does M halt on w? **Undecidable** (Turing, 1936).

**Proof idea (diagonalisation):** suppose a decider H(M, w) always answers correctly. Build D(M): run H(M, ⟨M⟩); if it says "halts", loop forever; if it says "loops", halt. Now ask what D(⟨D⟩) does: if it halts, H said "halts", so D loops; if it loops, H said "loops", so D halts. Contradiction either way, so H can't exist.

**Types of problems:**

- **Decidable:** an algorithm always halts with the answer (DFA acceptance, CFG membership via CYK, emptiness of a CFL).
- **Undecidable:** no algorithm can always answer: halting problem, **Post's correspondence problem**, whether a CFG is ambiguous, whether two CFGs generate the same language, **Rice's theorem** (every non-trivial property of the language of a TM is undecidable).
- **Tractable vs intractable** (among decidable problems): **P** = solvable in polynomial time by a DTM; **NP** = verifiable in polynomial time (solvable by an NTM in polynomial time); **NP-complete** = the hardest problems in NP (SAT, travelling salesman decision version); whether P = NP is open.

---

## 6. Quick recap

- TM = (Q, Σ, Γ, δ, q₀, B, F); δ(q, X) = (p, Y, L/R); infinite tape, read/write, two-way head.
- TM > PDA: rewritable, revisitable tape (two stacks = a TM); Type 0 vs Type 2.
- aⁿbⁿcⁿ: mark a → X, b → Y, c → Z, return, repeat; finally only Y, Z, then blank → accept.
- NTM = DTM in power; primitive recursive functions are total and computable (Ackermann isn't primitive recursive).
- Recursive (decidable, always halts) ⊂ RE (recognisable) ⊂ all; complement of HALT is non-RE.
- Halting problem undecidable by diagonalisation; Rice's theorem; P, NP, NP-complete.
