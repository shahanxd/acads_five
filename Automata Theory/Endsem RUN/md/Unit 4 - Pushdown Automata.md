# Automata Unit 4: Pushdown Automata

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** a pushdown automaton (PDA) is a finite automaton plus a **stack**. The stack gives it unbounded memory, but only of the last-in-first-out kind, which is exactly enough to recognise **context-free languages** (things that need matching, like aⁿbⁿ or brackets). Every CFG can be turned into a PDA and vice versa.

**What the endsem asks from here:** FA vs PDA with a block diagram, "what language does this PDA accept, by final state or empty stack", and CFG → PDA conversion. 2025's whole Q4.

---

## 1. What a PDA is · Slow down

Think of a stack of plates: you can only add (**push**) or remove (**pop**) the top plate. A PDA reads its input left to right, and at every step it can look at the current input symbol (or not, an ε-move), its state, and the **top of the stack**, then change state and replace the top symbol with a string (pop = replace with ε; push = replace X with YX).

**Exam line:** *A PDA is a 7-tuple M = (Q, Σ, Γ, δ, q₀, Z₀, F): Q states, Σ input alphabet, Γ stack alphabet, δ: Q × (Σ ∪ {ε}) × Γ → finite subsets of Q × Γ\*, q₀ start state, Z₀ ∈ Γ the initial stack symbol, F ⊆ Q final states.*

δ(q, a, X) = (p, γ) means: in state q, reading a, with X on top of the stack, go to state p and **replace X by γ** (leftmost symbol of γ becomes the new top).

**Instantaneous description (ID):** (state, remaining input, stack contents), e.g. (q0, aabb, Z₀). One move: ⊢.

**Two ways to accept:**

- **By final state:** the input is used up and the PDA is in a state in F (stack contents don't matter).
- **By empty stack:** the input is used up and the stack is empty (state doesn't matter).

The two are **equivalent in power**: any PDA of one kind can be converted to the other.

**Deterministic vs non-deterministic:** an NPDA may have several choices; a DPDA at most one. Unlike finite automata, **NPDAs are more powerful than DPDAs**: wwᴿ (even palindromes) needs guessing the middle, so it needs non-determinism.

---

## 2. FA vs PDA · Slow down

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

---

## 3. Designing PDAs · Quick

| Language | Idea |
| --- | --- |
| aⁿbⁿ | Push for a, pop for b, accept on Z₀ |
| aⁿb²ⁿ | Push **two** symbols per a (or pop one per two b's) |
| wcwᴿ | Push until c, then pop and match each symbol (deterministic) |
| wwᴿ | Guess the middle with an ε-move (non-deterministic) |
| Balanced brackets | Push on (, pop on ), accept when the stack returns to Z₀ |
| equal a's and b's | Push the "excess" symbol; pop when the opposite one comes |

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

---

## 4. CFG → PDA · Slow down

**The standard construction** (the PDA simulates a leftmost derivation on its stack): one state q, start stack symbol S, acceptance by empty stack.

1. For each variable A with productions A → α₁ | α₂ | …: **δ(q, ε, A) = {(q, α₁), (q, α₂), …}** (replace A on top by one of its right sides, without reading input: "expand").
2. For each terminal a: **δ(q, a, a) = {(q, ε)}** (if the top matches the input, pop it: "match").
3. Accept when the input is consumed and the stack is empty.

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

---

## 5. PDA → CFG (idea) · Quick

The reverse is also possible: for a PDA accepting by empty stack, create variables [p X q] meaning "starting in p with X on top, the PDA can pop X and end in q", and write productions from each transition. So **PDA languages = context-free languages** exactly.

---

## 6. Quick recap

- PDA = FA + stack: 7-tuple (Q, Σ, Γ, δ, q₀, Z₀, F); δ looks at state, input (or ε), stack top.
- Accept by final state or empty stack (equal power); NPDA more powerful than DPDA (wwᴿ).
- FA: finite memory, regular; PDA: unbounded LIFO stack, context-free.
- aⁿbⁿ: push per a, pop per b; the 2025 PDA accepts aⁿbⁿ (n ≥ 1) by **final state** (Z₀ left on the stack).
- CFG → PDA: expand δ(q, ε, A) = (q, α), match δ(q, a, a) = (q, ε), accept by empty stack.
