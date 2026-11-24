# Automata Theory Endsem 2025, Solved

**Paper:** B.Tech (CE) Sem V, Automata Theory (CSC-505 / CEN-502 Old), 2025, 3 hours, 45/60 marks. Attempt any two parts from each question; each part is 4.5/6 marks. All 15 parts are solved; the DFA, grammar and Turing machine answers were checked by computer.

Every question of the 2025 endsem paper, solved. The same answers sit inside the unit docs at the topic they belong to; the unit is named under each question so you can jump there for the explanation.

---

## Question 1

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

*Taught in Unit 1.*

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

*Taught in Unit 1.*

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

*Taught in Unit 1.*

---

## Question 2

> **Endsem 2025 · Q2(a) · 4.5 marks**
> Simplify the regular expression ((a+b)\*a(a+b)\*) + ((a+b)\*b(a+b)\*) using regular expression identities.

**Answer.**

Let R = (a + b). The expression is R\*aR\* + R\*bR\*.

```latex
\begin{aligned}
R^*aR^* + R^*bR^* &= R^*(a + b)R^* && \text{(I13: distributive law, taking } R^* \text{ out on both sides)} \\
&= R^*RR^* && (a + b = R) \\
&= R^+R^* && (R^*R = R^+, \text{ I9}) \\
&= RR^*R^* && (R^+ = RR^*) \\
&= RR^* && (R^*R^* = R^*, \text{ I7}) \\
&= R^+ = (a + b)(a + b)^* = (a+b)^+
\end{aligned}
```

**Meaning check:** the first part is "strings containing at least one a", the second "strings containing at least one b"; their union is "strings containing at least one symbol", i.e. every string except ε. That is exactly $(a+b)^+$.

**The expression simplifies to (a + b)⁺ = (a + b)(a + b)\*: all non-empty strings over {a, b}.**

*Taught in Unit 2.*

> **Endsem 2025 · Q2(b) · 4.5 marks**
> State and define the Pumping Lemma for regular languages. Also evaluate its effectiveness and limitations in proving non-regularity of languages.

**Answer.**

**Statement:** if L is a **regular** language, then there is a constant **p ≥ 1** (the pumping length, at most the number of states of a DFA for L) such that **every** string w ∈ L with **|w| ≥ p** can be divided as **w = xyz** satisfying:

1. **|y| ≥ 1** (the pumped part is non-empty),
2. **|xy| ≤ p** (the loop occurs within the first p symbols),
3. **xyⁱz ∈ L for every i ≥ 0** (repeating y, or deleting it, stays in L).

**Why it's true:** reading the first p symbols visits p + 1 states, so some state repeats; y is the part read between the two visits (a loop), x before it and z after.

**Using it to prove non-regularity (by contradiction):** assume L is regular with pumping length p; **choose** a cleverly picked w ∈ L with |w| ≥ p; show that for **every** split xyz satisfying conditions 1 and 2, some i makes xyⁱz ∉ L; contradiction, so L is not regular.

**Example:** L = {aⁿbⁿ | n ≥ 0}. Take w = aᵖbᵖ. Since |xy| ≤ p, y lies within the a's: y = aᵏ, k ≥ 1. Then xy²z = aᵖ⁺ᵏbᵖ has more a's than b's, so it's not in L. Contradiction: L is not regular.

**Effectiveness:**

- A simple, general, mechanical tool: works for many classic non-regular languages (aⁿbⁿ, palindromes, ww, a^(n²), a^prime).
- Captures exactly the limitation of finite memory: a DFA can't count without bound.
- Needs no construction of automata; one well-chosen string suffices.

**Limitations:**

- It is only a **necessary** condition, not sufficient: every regular language satisfies it, but **some non-regular languages also satisfy it**, so it can **never prove that a language is regular**, and it fails to prove non-regularity for those languages (e.g. {aⁱbʲcᵏ | i = 0 or j = k} pumps fine but isn't regular).
- Success depends on **choosing the right string**; a bad choice proves nothing.
- You must handle **every** possible split, which can get messy (case analysis).
- For such cases stronger tools are needed: the **Myhill–Nerode theorem** (exact characterisation), **closure properties** (e.g. intersect with a regular language to reach a known non-regular one), or Ogden-style variants.

**If L is regular, every long enough string in it can be pumped (w = xyz, |y| ≥ 1, |xy| ≤ p, xyⁱz ∈ L); it's effective for proving non-regularity by contradiction, but it's only a necessary condition, can't prove regularity, and depends on choosing the right string.**

*Taught in Unit 2.*

> **Endsem 2025 · Q2(c) · 4.5 marks**
> Apply the pumping lemma to analyse the regularity of L = {w ∈ {a, b}\* | w contains an equal number of occurrences of the substrings "ab" and "ba"}.

**Answer.**

At first sight it looks like counting (non-regular), but **this language is regular**, so the pumping lemma cannot prove it non-regular. The right analysis is to understand the structure, show the lemma is satisfied, and prove regularity with an automaton.

**Key observation:** read the string left to right. Every switch from a to b creates one "ab", every switch from b to a creates one "ba", and switches **alternate** (a→b, then b→a, then a→b, …). So the counts of ab and ba are either equal or differ by exactly 1:

- If the string **starts and ends with the same letter**, the switches pair up: #ab = #ba. E.g. abba: ab, ba → 1 and 1 ✓; aba: 1 and 1 ✓.
- If it starts and ends with **different** letters, there is one extra switch: e.g. ab: #ab = 1, #ba = 0 ✗; abab: 2 and 1 ✗.

So **L = {ε, a, b} ∪ {strings that begin and end with the same symbol}**:

```latex
L = \varepsilon + a + b + a(a+b)^*a + b(a+b)^*b
```

**Applying the pumping lemma:** take the DFA below (5 states), so p = 5. Any w ∈ L with |w| ≥ 5 can be split with y = **one symbol in the middle**, not the first and not the last (e.g. x = w₁, y = w₂, z = the rest; |xy| = 2 ≤ p, |y| = 1). Pumping y up or down never changes the first or the last symbol, so xyⁱz still begins and ends with the same letter: **xyⁱz ∈ L for all i**. Hence L **satisfies** the pumping lemma: no contradiction can be found, which is consistent with L being regular. (The lemma alone can't prove regularity; the automaton does.)

**DFA proving regularity** (remember the first letter and the last letter):

| State | Meaning | a | b | Final? |
| --- | --- | --- | --- | --- |
| → q0 | empty string | qa | qb | Yes |
| qa | started with a, last letter a | qa | qa′ | Yes |
| qa′ | started with a, last letter b | qa | qa′ | No |
| qb | started with b, last letter b | qb′ | qb | Yes |
| qb′ | started with b, last letter a | qb′ | qb | No |

(Checked by computer against the definition for every string up to length 12.)

**Verification:** abba → q0 → qa → qa′ → qa′ → qa: accept (#ab = #ba = 1). abab → … → qa′: reject (2 vs 1). baab → qb → qb′ → qb′ → qb: accept (#ba = #ab = 1).

**L is regular (strings that start and end with the same symbol, plus ε, a, b): it satisfies the pumping lemma, so the lemma cannot show non-regularity, and the 5-state DFA / the RE ε + a + b + a(a+b)\*a + b(a+b)\*b proves it regular.**

*Taught in Unit 2.*

---

## Question 3

> **Endsem 2025 · Q3(a) · 4.5 marks**
> Design a context-free grammar for L = {aⁿbᵐ | n ≥ 1, m ≥ 1, n = m or n = 2m}. Verify your answer using suitable sentences.

**Answer.**

L is the **union** of two languages:

- L₁ = {aⁿbⁿ | n ≥ 1}: equal a's and b's: one a for every b.
- L₂ = {a²ᵐbᵐ | m ≥ 1}: two a's for every b.

Generate each with its own variable and join them at S:

```
S → A | B
A → aAb | ab         (n = m:  adds one a and one b per step)
B → aaBb | aab       (n = 2m: adds two a's and one b per step)
```

G = ({S, A, B}, {a, b}, P, S).

**Verification:**

| Sentence | n, m | Derivation |
| --- | --- | --- |
| ab | 1, 1 (n = m) | S ⇒ A ⇒ ab |
| aabb | 2, 2 (n = m) | S ⇒ A ⇒ aAb ⇒ aabb |
| aab | 2, 1 (n = 2m) | S ⇒ B ⇒ aab |
| aaaabb | 4, 2 (n = 2m) | S ⇒ B ⇒ aaBb ⇒ aaaabb |
| aaabbb | 3, 3 | S ⇒ A ⇒ aAb ⇒ aaAbb ⇒ aaabbb |

Strings **not** generated: aaab (n = 3, m = 1: neither equal nor double), abb (n = 1, m = 2), ε (n, m ≥ 1).

Correctness: A generates exactly aⁿbⁿ (n ≥ 1) and B exactly a²ᵐbᵐ (m ≥ 1), so S generates their union. (Checked by computer: the grammar generates exactly L for all strings up to length 12.)

**S → A | B, A → aAb | ab, B → aaBb | aab.**

*Taught in Unit 3.*

> **Endsem 2025 · Q3(b) · 4.5 marks**
> CFG with variables {S, NP, VP, Det, N, V}: S → NP VP, NP → Det N, VP → V NP, Det → the, N → man | telescope, V → saw. Give the LMD, RMD and derivation tree for "the man saw the telescope", and comment on the grammar's ambiguity.

**Answer.**

**Leftmost derivation** (always expand the leftmost variable):

```
S ⇒ NP VP
  ⇒ Det N VP
  ⇒ the N VP
  ⇒ the man VP
  ⇒ the man V NP
  ⇒ the man saw NP
  ⇒ the man saw Det N
  ⇒ the man saw the N
  ⇒ the man saw the telescope
```

**Rightmost derivation** (always expand the rightmost variable):

```
S ⇒ NP VP
  ⇒ NP V NP
  ⇒ NP V Det N
  ⇒ NP V Det telescope
  ⇒ NP V the telescope
  ⇒ NP saw the telescope
  ⇒ Det N saw the telescope
  ⇒ Det man saw the telescope
  ⇒ the man saw the telescope
```

**Derivation tree:**

```
                    S
               ┌────┴─────┐
               NP          VP
             ┌─┴─┐      ┌──┴───┐
            Det   N     V       NP
             │    │     │     ┌──┴──┐
            the  man   saw   Det     N
                              │      │
                             the  telescope
```

**Ambiguity:** for this sentence there is **only one** parse tree: S has one production, NP has one, VP has one, and at each N and V only the alternative matching the next word can be used. The LMD and RMD above are just two orders of building the **same** tree. In fact the whole grammar is **unambiguous**: it generates only four sentences (the man / the telescope saw the man / the telescope), each with exactly one tree.

(The famous ambiguity "the man saw the man **with the telescope**" (who has the telescope?) appears only if we add prepositional-phrase rules like NP → NP PP and VP → VP PP. Then one string gets two trees, PP attached to the noun or to the verb, and the grammar becomes ambiguous.)

**One LMD, one RMD, one parse tree: the given grammar is unambiguous; ambiguity would need PP-attachment rules.**

*Taught in Unit 3.*

> **Endsem 2025 · Q3(c) · 4.5 marks**
> Compare and contrast the computational power and grammar restrictions of the four Chomsky language types.

**Answer.**

Noam Chomsky classified grammars into four types by the **restrictions on their productions**. Each type is a proper subset of the one above it, and each corresponds to a class of machines with increasing computational power:

**Type 3 ⊂ Type 2 ⊂ Type 1 ⊂ Type 0**

| Type | Grammar | Production restriction | Language class | Machine | Example language |
| --- | --- | --- | --- | --- | --- |
| **0** | Unrestricted (phrase-structure) | α → β, α contains at least one variable; **no restriction** on β | Recursively enumerable | **Turing machine** | Any language a TM can list, e.g. halting-problem related languages |
| **1** | Context-sensitive | αAβ → αγβ with γ ≠ ε (equivalently \|lhs\| ≤ \|rhs\|): A can be replaced **only in the context** α…β | Context-sensitive | **Linear bounded automaton** (TM with tape limited to the input) | aⁿbⁿcⁿ |
| **2** | Context-free | **A → γ**: a single variable on the left, anything on the right | Context-free | **Pushdown automaton** (FA + stack) | aⁿbⁿ, balanced brackets, palindromes |
| **3** | Regular | **A → aB or A → a** (right-linear; or all left-linear), at most one variable, at the end | Regular | **Finite automaton** (no extra memory) | a\*b\*, strings ending in 01 |

**Computational power, compared:**

- **Type 3 / FA:** only a fixed, finite memory (the state). Can't count without bound, so can't match aⁿ with bⁿ.
- **Type 2 / PDA:** adds a **stack** (unbounded but last-in-first-out). Can match one pair of counts or nesting (aⁿbⁿ, brackets), but not two independent counts (aⁿbⁿcⁿ).
- **Type 1 / LBA:** a tape as long as the input, read and written freely. Can handle aⁿbⁿcⁿ; membership is decidable.
- **Type 0 / TM:** unbounded tape: the most powerful model of computation (Church–Turing thesis). Membership may be undecidable (the machine may never halt).

As restrictions decrease (Type 3 → 0), grammars become more expressive, machines more powerful, and questions about them harder (emptiness and equivalence are decidable for regular languages, but undecidable for Type 0).

**Type 3 (regular, A → aB, FA) ⊂ Type 2 (context-free, A → γ, PDA) ⊂ Type 1 (context-sensitive, |α| ≤ |β|, LBA) ⊂ Type 0 (unrestricted, TM): fewer restrictions, more power.**

*Taught in Unit 3.*

---

## Question 4

> **Endsem 2025 · Q4(a) · 4.5 marks**
> Using a labelled block diagram, explain the differences between finite automata (FA) and pushdown automata (PDA) in terms of memory and language recognition power. Also describe how the stack in a PDA helps recognise non-regular languages, with an example.

**Answer.**

```
   FINITE AUTOMATON                         PUSHDOWN AUTOMATON

  input tape: | a | a | b | b |            input tape: | a | a | b | b |
                ^ read head (L→R)                        ^ read head (L→R)
                |                                        |
       +-------------------+                  +-------------------+     push / pop
       |  finite control   |                  |  finite control   |<------------+
       |  (current state)  |                  |  (current state)  |             |
       +-------------------+                  +-------------------+         +-------+
         accept / reject                        accept / reject      top -> |   a   |
                                                                            |   a   |
         memory = the state only                                            |  Z0   |
                                                                            +-------+
                                                                              STACK
                                                                          (unbounded, LIFO)
```

| Basis | Finite automaton | Pushdown automaton |
| --- | --- | --- |
| Components | Input tape, read head, finite control | Same **plus a stack** |
| Memory | Only the current state: **finite**, fixed in advance | State + **unbounded stack** (but only the top is accessible) |
| Tuple | 5-tuple (Q, Σ, δ, q₀, F) | 7-tuple (adds Γ and Z₀) |
| Transition depends on | State, input symbol | State, input symbol (or ε), **top of stack** |
| Languages | **Regular** (Type 3) | **Context-free** (Type 2), a strict superset |
| Grammar | Regular grammar | Context-free grammar |
| Determinism | DFA = NFA in power | DPDA weaker than NPDA |
| Example it can't do / can do | Can't do aⁿbⁿ | Can do aⁿbⁿ, balanced brackets, wcwᴿ |

**How the stack recognises non-regular languages.** A regular language can't need unbounded counting, because the FA has only finitely many states to remember a count with. **L = {aⁿbⁿ | n ≥ 1}** needs to remember n, which can be arbitrarily large, so no FA can do it (by the pumping lemma). A PDA uses the stack as a **counter/matcher**:

1. While reading a's, **push** one a for each a read.
2. On the first b, switch state; for each b, **pop** one a.
3. If the input ends exactly when only Z₀ is left, every b matched an a: **accept**.

Trace for aabb: (q0, aabb, Z₀) ⊢ (q0, abb, aZ₀) ⊢ (q0, bb, aaZ₀) ⊢ (q1, b, aZ₀) ⊢ (q1, ε, Z₀) ⊢ (qf, ε, Z₀): **accept**. For aab, the input ends with an a still on the stack: reject. The stack's LIFO order is exactly right for **nesting**: the last thing opened is the first thing closed, as in brackets.

**An FA's memory is only its finite state, so it recognises regular languages; a PDA adds an unbounded LIFO stack, so it recognises context-free languages, e.g. aⁿbⁿ by pushing a's and popping one per b.**

*Taught in Unit 4.*

> **Endsem 2025 · Q4(b) · 4.5 marks**
> PDA transitions: δ(q0, a, Z₀) = (q0, aZ₀); δ(q0, a, a) = (q0, aa); δ(q0, b, a) = (q1, ε); δ(q1, b, a) = (q1, ε); δ(q1, ε, Z₀) = (qf, Z₀). Analyse the language accepted and whether it accepts by final state or by empty stack.

**Answer.**

**What each move does:**

| Transition | Meaning |
| --- | --- |
| δ(q0, a, Z₀) = (q0, aZ₀) | First a: push a |
| δ(q0, a, a) = (q0, aa) | Each further a: push another a |
| δ(q0, b, a) = (q1, ε) | First b: pop one a, switch to q1 (no more a's allowed: there's no a-move in q1) |
| δ(q1, b, a) = (q1, ε) | Each further b: pop one a |
| δ(q1, ε, Z₀) = (qf, Z₀) | When only Z₀ is left: go to qf **without popping Z₀** |

So the PDA pushes one a per a, pops one a per b, and reaches qf exactly when the number of b's equals the number of a's. There's no move from q0 on Z₀ with input b, so a string can't start with b; and no move reaches qf without at least one a and one b.

**Language:** **L = {aⁿbⁿ | n ≥ 1}**.

**Acceptance mode: by final state.** The last move goes to **qf** but leaves **Z₀ on the stack** (it's never popped), so the stack is never empty; acceptance must be by reaching the final state qf with the input consumed.

**Traces:**

- aabb: (q0, aabb, Z₀) ⊢ (q0, abb, aZ₀) ⊢ (q0, bb, aaZ₀) ⊢ (q1, b, aZ₀) ⊢ (q1, ε, Z₀) ⊢ (qf, ε, Z₀) → **accepted** (final state, stack = Z₀).
- aab: … ⊢ (q1, ε, aZ₀): no move possible, not in qf → **rejected**.
- abb: (q0, abb, Z₀) ⊢ (q0, bb, aZ₀) ⊢ (q1, b, Z₀) → (qf, b, Z₀), but input b remains and qf has no moves → **rejected**.
- ε or ba: no applicable first move → rejected.

**The PDA accepts {aⁿbⁿ | n ≥ 1} by final state (qf is reached with Z₀ still on the stack).**

(To accept by empty stack instead, the last move would be δ(q1, ε, Z₀) = (q1, ε).)

*Taught in Unit 4.*

> **Endsem 2025 · Q4(c) · 4.5 marks**
> Convert the CFG S → aSb | bSa | ε into an equivalent PDA, showing all steps and rules of the standard CFG-to-PDA algorithm. Highlight the merits and demerits of this method for this CFG.

**Answer.**

**Grammar:** V = {S}, T = {a, b}, productions S → aSb | bSa | ε.

**PDA:** M = ({q}, {a, b}, {S, a, b}, δ, q, S, ∅), accepting by **empty stack**:

**Step 1 (expand rules, one per production of S):**

```latex
\delta(q, \varepsilon, S) = \{(q, aSb),\ (q, bSa),\ (q, \varepsilon)\}
```

**Step 2 (match rules, one per terminal):**

```latex
\delta(q, a, a) = \{(q, \varepsilon)\}, \qquad \delta(q, b, b) = \{(q, \varepsilon)\}
```

(For acceptance by final state, add a start state p and a final state f: δ(p, ε, Z₀) = (q, SZ₀) and δ(q, ε, Z₀) = (f, Z₀).)

**Trace for abab**, which the grammar derives as S ⇒ aSb ⇒ abSab ⇒ abab:

| Step | ID (state, input left, stack) | Rule used |
| --- | --- | --- |
| 0 | (q, abab, S) | start |
| 1 | (q, abab, aSb) | expand S → aSb |
| 2 | (q, bab, Sb) | match a |
| 3 | (q, bab, bSab) | expand S → bSa |
| 4 | (q, ab, Sab) | match b |
| 5 | (q, ab, ab) | expand S → ε |
| 6 | (q, b, b) | match a |
| 7 | (q, ε, ε) | match b → empty stack: **accept** |

The stack always holds the not-yet-matched part of the current leftmost sentential form, so each accepting run mirrors a leftmost derivation.

**Merits of the method:**

- **Mechanical and always works:** any CFG gives a PDA immediately, proving every CFL is accepted by a PDA.
- **Only one state** and few rules (here 5 transitions), easy to write.
- The run directly corresponds to a **leftmost derivation**, so correctness is obvious; the PDA is the basis of **top-down (LL) parsing**.

**Demerits (seen with this grammar):**

- **Non-deterministic:** with S on top there are three choices (aSb, bSa, ε) and the PDA must **guess**. For abab it had to choose S → ε at exactly the right moment (step 5); a real implementation needs backtracking or lookahead.
- **ε-moves**: the expand steps read no input, so the number of moves isn't bounded by the input length, and ε-productions add extra guessing.
- Acceptance by **empty stack** needs an extra conversion if final-state acceptance is wanted.
- Inefficient as a parser for ambiguous or left-recursive grammars (left recursion like A → Aa can loop forever).

**PDA: δ(q, ε, S) = {(q, aSb), (q, bSa), (q, ε)}, δ(q, a, a) = δ(q, b, b) = {(q, ε)}, accept by empty stack; simple and systematic, but non-deterministic (it must guess which S-production to use).**

*Taught in Unit 4.*

---

## Question 5

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

*Taught in Unit 5.*

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

*Taught in Unit 5.*

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

*Taught in Unit 5.*

