# Automata Unit 2: Regular Expressions, Arden's Theorem and the Pumping Lemma

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** a regular expression is a compact formula for a regular language (the same languages finite automata accept). Identities simplify them, **Arden's theorem** converts an automaton into one, and the **pumping lemma** is the tool for proving that a language is **not** regular.

**What the endsem asks from here:** simplify an RE with identities, state and judge the pumping lemma, and apply it to a language. 2025's whole Q2. Watch out: the 2025 Q2(c) language is actually regular, which is a trap.

---

## 1. Regular expressions · Quick

**Exam line:** *A regular expression over Σ is built from ∅, ε and each symbol a ∈ Σ, using union (+), concatenation (·) and Kleene star (\*). Each RE r denotes a language L(r).*

| RE | Language |
| --- | --- |
| a + b | {a, b} |
| ab | {ab} |
| a\* | {ε, a, aa, aaa, …} |
| (a + b)\* | All strings over {a, b} |
| (a + b)\*abb | Strings ending in abb |
| a⁺ = aa\* | One or more a's |

Precedence: \* first, then concatenation, then +.

**Identities** (the toolkit for simplification):

| # | Identity | # | Identity |
| --- | --- | --- | --- |
| I1 | ∅ + R = R | I7 | R\*R\* = R\* |
| I2 | ∅R = R∅ = ∅ | I8 | (R\*)\* = R\* |
| I3 | εR = Rε = R | I9 | RR\* = R\*R = R⁺ |
| I4 | ε\* = ε, ∅\* = ε | I10 | ε + RR\* = ε + R\*R = R\* |
| I5 | R + R = R | I11 | (PQ)\*P = P(QP)\* |
| I6 | R + R\* = R\* | I12 | (P + Q)\* = (P\*Q\*)\* = (P\* + Q\*)\* |
| | | I13 | PR + QR = (P + Q)R, RP + RQ = R(P + Q) |

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

---

## 2. Arden's theorem and FA → RE · Slow down

**Arden's theorem:** if P and Q are regular expressions over Σ and P does not contain ε, then the equation

```latex
R = Q + RP \quad \text{has the unique solution} \quad R = QP^*
```

Why it makes sense: R = Q + RP means "R is Q followed by any number of P's": Q, QP, QPP, … = QP\*.

**Converting a DFA to an RE:**

1. For each state, write an equation: the state = sum of (previous state · symbol) over all incoming arrows; add ε to the start state's equation.
2. Solve them by substitution and Arden's theorem.
3. The RE = the sum of the expressions for the final states.

**Example:** DFA: q0 (start) –0→ q0, q0 –1→ q1, q1 –1→ q1, q1 –0→ q0; final q1 (strings ending in 1).

```latex
\begin{aligned}
q_1 &= q_0 1 + q_1 1 \;\Rightarrow\; q_1 = q_0 1 1^* && \text{(Arden: } Q = q_0 1,\ P = 1) \\
q_0 &= \varepsilon + q_0 0 + q_1 0 = \varepsilon + q_0 0 + q_0 1 1^* 0 = \varepsilon + q_0 (0 + 11^*0) \\
\Rightarrow q_0 &= (0 + 11^*0)^* && \text{(Arden: } Q = \varepsilon) \\
q_1 &= (0 + 11^*0)^*\, 1 1^*
\end{aligned}
```

**RE = (0 + 11\*0)\*11\***, which is equivalent to (0 + 1)\*1.

(The other direction, RE → ε-NFA, uses Thompson's construction: small machines for a, R₁ + R₂, R₁R₂ and R\*, joined by ε-moves.)

---

## 3. Properties of regular languages · Quick

Regular languages are **closed** under: union, concatenation, Kleene star, **complement** (swap final and non-final states of a DFA), **intersection** (product automaton), difference, reversal, homomorphism. "Closed" means doing the operation to regular languages always gives a regular language.

**Decision properties** (algorithms exist): is L empty? finite? is w ∈ L? are two regular languages equal (minimise both and compare)?

---

## 4. The pumping lemma · Slow down

A DFA has only finitely many states, say p. Feed it a string longer than p, and by the **pigeonhole principle** some state must repeat: the path contains a **loop**. Whatever was read around that loop can be repeated ("pumped") any number of times, or skipped, and the DFA will still accept. That's the pumping lemma.

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

---

## 5. Quick recap

- RE operators: +, ·, \*; identities R + R = R, R\*R\* = R\*, RR\* = R⁺, ε + RR\* = R\*, distributive law.
- 2025 simplification: R\*aR\* + R\*bR\* = (a + b)⁺.
- Arden: R = Q + RP ⇒ R = QP\* (P without ε); DFA → equations → solve.
- Closure: union, concatenation, star, complement, intersection, reversal.
- Pumping lemma: |y| ≥ 1, |xy| ≤ p, xyⁱz ∈ L; proves non-regularity by contradiction; necessary, not sufficient.
- #ab = #ba ⇔ first = last letter: a regular language (trap question).
