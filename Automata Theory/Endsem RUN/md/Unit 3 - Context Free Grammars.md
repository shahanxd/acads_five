# Automata Unit 3: Context-Free Grammars and Languages

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** a grammar is a set of rewriting rules that **generates** a language. Chomsky ranked grammars into four types by how restricted their rules are; **context-free grammars (CFGs)** sit in the middle and describe nested structure (brackets, programming languages). This unit covers derivations, parse trees, ambiguity, simplifying a CFG, and converting it to **Chomsky Normal Form**.

**What the endsem asks from here:** design a CFG for a language, LMD/RMD/parse tree with an ambiguity comment, and the Chomsky hierarchy. 2025's whole Q3. CNF conversion is the other favourite.

---

## 1. Grammars and the Chomsky hierarchy · Slow down

**Exam line:** *A grammar is a 4-tuple G = (V, T, P, S): V a finite set of variables (non-terminals), T a finite set of terminals, P a finite set of productions α → β, and S ∈ V the start symbol. The language L(G) is the set of terminal strings derivable from S.*

Think of a grammar as a recipe book: S is "make a sentence", and each production says how one ingredient can be replaced by others, until only real words (terminals) are left.

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

---

## 2. Designing a CFG · Slow down

A **context-free grammar** has every production of the form **A → γ** (one variable on the left). Design tip: think about **what must match what**, and generate matched pieces **together**, from the outside in.

- aⁿbⁿ: S → aSb | ab (each step adds one a on the left and one b on the right).
- aⁿb²ⁿ: S → aSbb | abb.
- Palindromes over {a, b}: S → aSa | bSb | a | b | ε.
- Union of two languages: S → S₁ | S₂, with separate grammars for each.

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

---

## 3. Derivations, parse trees and ambiguity · Slow down

- **Derivation:** a sequence of rewrites from S to a string (⇒ one step, ⇒\* many).
- **Leftmost derivation (LMD):** always rewrite the **leftmost** variable.
- **Rightmost derivation (RMD):** always rewrite the **rightmost** variable.
- **Derivation (parse) tree:** root S, internal nodes = variables, children of a node = the right side of the production used, leaves read left to right = the string (the **yield**).

A grammar is **ambiguous** if some string has **two or more different parse trees** (equivalently, two different LMDs or two RMDs). Example: E → E + E | E \* E | id is ambiguous: id + id \* id has two trees, (id + id) \* id and id + (id \* id). Ambiguity is bad for compilers (two meanings). Some CFLs are **inherently ambiguous** (every grammar for them is ambiguous), e.g. {aⁱbʲcᵏ | i = j or j = k}.

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

---

## 4. Simplifying a CFG · Quick

Three clean-ups, done in this order: **ε-productions → unit productions → useless symbols**.

1. **Remove ε-productions (A → ε):** find **nullable** variables (those that can derive ε). For every production containing nullable variables, add versions with each combination of them deleted (but don't create a new A → ε). (If ε ∈ L, keep S → ε with a new start symbol.)
2. **Remove unit productions (A → B):** for each A ⇒\* B through units, add A → (every non-unit right side of B), then delete the units.
3. **Remove useless symbols:** delete **non-generating** variables (can't derive any terminal string), then **unreachable** symbols (can't be reached from S).

**Example:** S → aA | B, A → aA | ε, B → b.

- Nullable: A. Remove A → ε: S → aA | a | B, A → aA | a.
- Unit S → B with B → b: S → aA | a | b.
- B is now unreachable: remove it.

**Result: S → aA | a | b, A → aA | a.** (Language: a⁺ ∪ {b}.)

---

## 5. Chomsky Normal Form · Slow down

**CNF:** every production is either **A → BC** (two variables) or **A → a** (one terminal) (plus S → ε if ε ∈ L, with S not on any right side). Why bother? Parse trees become binary, which makes proofs and the **CYK parsing algorithm** work.

**Conversion steps:**

1. Simplify (remove ε-productions, unit productions, useless symbols).
2. **Terminals in long bodies:** for each terminal a appearing in a body of length ≥ 2, add Cₐ → a and replace a by Cₐ.
3. **Long bodies:** break A → B₁B₂…Bₖ (k ≥ 3) into a chain: A → B₁X₁, X₁ → B₂X₂, …, Xₖ₋₂ → Bₖ₋₁Bₖ.

**Example:** S → aSb | ab.

- Step 2: A → a, B → b: S → ASB | AB.
- Step 3: S → ASB becomes S → AX, X → SB.

**CNF: S → AX | AB, X → SB, A → a, B → b.**

(Check aabb: S ⇒ AX ⇒ aX ⇒ aSB ⇒ aABB ⇒ aaBB ⇒ aabB ⇒ aabb ✓.)

---

## 6. Quick recap

- Grammar G = (V, T, P, S). Chomsky: Type 3 regular (FA) ⊂ 2 context-free (PDA) ⊂ 1 context-sensitive (LBA) ⊂ 0 unrestricted (TM).
- CFG design: generate matched parts together; union = S → S₁ | S₂.
- 2025 CFG: S → A | B, A → aAb | ab, B → aaBb | aab.
- LMD expands the leftmost variable, RMD the rightmost; same tree ≠ ambiguity.
- Ambiguous = some string has two parse trees (E → E + E | E \* E | id).
- Simplify: ε → unit → useless. CNF: A → BC or A → a.
