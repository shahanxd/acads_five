# DM Unit 2: Association Rule Mining

*Endsem RUN · about 60 minutes*

**The whole unit in one breath:** find items that occur together in transactions ("bread and butter"), measure how often (**support**) and how reliably (**confidence**), and do it efficiently: **Apriori** (level by level, prune using "a frequent set's subsets are all frequent"), **FP-growth** (compress into a tree, no candidates), and **Eclat** (vertical tid-lists, intersect).

**What the endsem asks from here:** Q3, all numerical-ish: generate rules with given support/confidence, enumerate frequent itemsets with Eclat or FP-growth, and how to speed up Apriori. 2025 asked exactly those three.

---

## 1. Market basket analysis and the basic terms · Quick

A supermarket looks at its bills to learn "customers who buy diapers often buy beer", then places items, plans offers and recommends. That's **market basket analysis**.

| Term | Meaning |
| --- | --- |
| **Itemset** | A set of items, e.g. {milk, bread}; a k-itemset has k items |
| **Support count** | Number of transactions containing the itemset |
| **Support** | Fraction of transactions containing it: $\text{sup}(X) = \frac{\text{count}(X)}{N}$ |
| **Frequent itemset** | Support ≥ minimum support (min_sup) |
| **Association rule** | $X \Rightarrow Y$ with X, Y disjoint itemsets |
| **Rule support** | $\text{sup}(X \cup Y)$: how often both occur |
| **Confidence** | $\text{conf}(X \Rightarrow Y) = \frac{\text{sup}(X \cup Y)}{\text{sup}(X)}$: of the bills with X, the fraction that also have Y |
| **Strong rule** | Support ≥ min_sup **and** confidence ≥ min_conf |
| **Lift** | $\frac{\text{conf}(X \Rightarrow Y)}{\text{sup}(Y)}$: > 1 positive correlation, = 1 independent, < 1 negative |

**Closed itemset:** frequent, and **no superset has the same support**. **Maximal itemset:** frequent, and **no superset is frequent** at all. Every maximal is closed; closed itemsets keep all support information in compressed form, maximal ones keep only "what is frequent".

Mining is two steps: **(1) find all frequent itemsets** (the expensive part), **(2) generate strong rules** from them.

---

## 2. Apriori · Slow down

**The Apriori property (anti-monotone):** *every subset of a frequent itemset is also frequent*. So if {beer} is infrequent, **no** set containing beer can be frequent, and we never need to count them. Like: if nobody in a class is above 6 ft, no group of them can have someone above 6 ft.

**Algorithm (level-wise):**

1. Scan the DB, count 1-itemsets, keep those ≥ min_sup: **L1**.
2. **Join** $L_{k-1}$ with itself to make candidates $C_k$ (combine sets that share their first k − 2 items).
3. **Prune** any candidate with an infrequent (k−1)-subset (the Apriori property).
4. Scan the DB to count the remaining candidates; keep the frequent ones: **Lk**.
5. Repeat until no candidates remain.

**Generating rules:** for each frequent itemset l and each non-empty proper subset s, output $s \Rightarrow (l - s)$ if $\frac{\text{count}(l)}{\text{count}(s)} \ge$ min_conf.

> **Endsem 2025 · Q3(a) · 4.5 marks**
> Transactions: T1 {F, A, D, B}, T2 {D, A, C, E, B}, T3 {C, A, B, E}, T4 {B, A, D}, T5 {D, B, C}, T6 {A, B, D, E}. What association rules can be found if minimum support is 25% and confidence is 60%?

**Answer.**

N = 6, so min support count = 25% × 6 = 1.5, i.e. an itemset must appear in **at least 2** transactions. Min confidence = 60%.

**L1** (count each item):

| A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- |
| 5 | 6 | 3 | 5 | 3 | 1 ✗ |

F (1) is infrequent and is dropped. L1 = {A, B, C, D, E}.

**C2 → L2** (all pairs of L1, then count):

| AB | AC | AD | AE | BC | BD | BE | CD | CE | DE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 2 | 4 | 3 | 3 | 5 | 3 | 2 | 2 | 2 |

All 10 pairs have count ≥ 2, so L2 = all of them.

**C3 → L3** (join, prune, count):

| ABC | ABD | ABE | ACD | ACE | ADE | BCD | BCE | BDE | CDE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 4 | 3 | 1 ✗ | 2 | 2 | 2 | 2 | 2 | 1 ✗ |

L3 = {ABC, ABD, ABE, ACE, ADE, BCD, BCE, BDE}.

**C4 → L4:** candidates whose 3-subsets are all in L3: ABCE (count 2 ✓), ABDE (count 2 ✓). (ABCD is pruned: ACD isn't frequent. BCDE: CDE isn't.) L4 = {ABCE, ABDE}. No 5-itemset can be formed, so stop.

**Maximal frequent itemsets:** {B, C, D}, {A, B, C, E}, {A, B, D, E}.

**Rules (confidence ≥ 60%).** From the 2-itemsets, all 15 strong rules:

| Rule | Conf | Rule | Conf | Rule | Conf |
| --- | --- | --- | --- | --- | --- |
| A ⇒ B | 5/5 = 100% | B ⇒ A | 5/6 = 83% | A ⇒ D | 4/5 = 80% |
| D ⇒ A | 4/5 = 80% | B ⇒ D | 5/6 = 83% | D ⇒ B | 5/5 = 100% |
| E ⇒ A | 3/3 = 100% | E ⇒ B | 3/3 = 100% | C ⇒ B | 3/3 = 100% |
| A ⇒ E | 3/5 = 60% | C ⇒ A | 2/3 = 67% | C ⇒ D | 2/3 = 67% |
| C ⇒ E | 2/3 = 67% | E ⇒ C | 2/3 = 67% | E ⇒ D | 2/3 = 67% |

(Rejected: B ⇒ C 50%, B ⇒ E 50%, A ⇒ C 40%, D ⇒ C, D ⇒ E 40%.)

The same procedure on L3 and L4 gives 51 more strong rules; the most useful (highest confidence, largest support) are:

| Rule | Support | Confidence |
| --- | --- | --- |
| AD ⇒ B | 4/6 | 4/4 = 100% |
| A ⇒ BD | 4/6 | 4/5 = 80% |
| D ⇒ AB | 4/6 | 4/5 = 80% |
| AB ⇒ D | 4/6 | 4/5 = 80% |
| BD ⇒ A | 4/6 | 4/5 = 80% |
| E ⇒ AB | 3/6 | 3/3 = 100% |
| AE ⇒ B, BE ⇒ A | 3/6 | 100% |
| AC ⇒ BE, CE ⇒ AB, ABC ⇒ E, ACE ⇒ B, BCE ⇒ A | 2/6 | 100% |
| DE ⇒ AB, ADE ⇒ B, BDE ⇒ A | 2/6 | 100% |
**Frequent: L1 = {A, B, C, D, E}, all 10 pairs, 8 triples, {ABCE, ABDE}. Strongest rules: A ⇒ B, D ⇒ B, E ⇒ A, E ⇒ B, C ⇒ B, AD ⇒ B, E ⇒ AB (all 100%).**

---

## 3. Improving Apriori's efficiency · Slow down

Apriori's two pains: **huge candidate sets** (10⁴ frequent items → ~10⁷ candidate pairs) and **many database scans** (one per level).

> **Endsem 2025 · Q3(c) · 4.5 marks**
> How can we improve the performance of the Apriori algorithm? Using an example, show how hash-based techniques can be used.

**Answer.**

**Ways to improve Apriori:**

1. **Hash-based technique (DHP):** while scanning for L1, hash every 2-itemset of each transaction into buckets of a hash table and count the bucket totals. A 2-itemset whose **bucket count < min_sup can't be frequent**, so it's removed from C2 before counting. Shrinks C2, the most expensive level.
2. **Transaction reduction:** a transaction containing no frequent k-itemset can't contain any frequent (k+1)-itemset, so drop it from later scans.
3. **Partitioning:** split the DB into partitions that fit in memory; find local frequent itemsets in each (scan 1); any globally frequent itemset must be locally frequent in at least one partition; count those candidates once (scan 2). Only **2 scans**.
4. **Sampling:** mine a random sample with a lower threshold, then verify on the whole DB. Fast; may miss a few itemsets.
5. **Dynamic itemset counting (DIC):** add new candidates at checkpoints during a scan instead of only between scans.

**Hash-based example** (Han's dataset, min support count = 3, 9 transactions over I1–I5):

T100 {I1, I2, I5}, T200 {I2, I4}, T300 {I2, I3}, T400 {I1, I2, I4}, T500 {I1, I3}, T600 {I2, I3}, T700 {I1, I3}, T800 {I1, I2, I3, I5}, T900 {I1, I2, I3}.

Hash function for an itemset {Ix, Iy}: $h(x, y) = (10x + y) \bmod 7$. During the L1 scan, every 2-itemset of every transaction is hashed:

| Bucket | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contents | {I1,I4}, {I3,I5} | {I1,I5} ×2 | {I2,I3} ×4 | {I2,I4} ×2 | {I2,I5} ×2 | {I1,I2} ×4 | {I1,I3} ×4 |
| Bucket count | 2 | 2 | **4** | 2 | 2 | **4** | **4** |
| ≥ 3? | No | No | Yes | No | No | Yes | Yes |

E.g. {I1, I4}: 10·1 + 4 = 14, 14 mod 7 = 0; {I2, I3}: 23 mod 7 = 2.

Buckets 0, 1, 3 and 4 have counts below 3, so **every itemset in them is removed** from C2 without counting. Normal Apriori would count all $\binom{5}{2} = 10$ pairs; with hashing **only 3 candidates remain**: {I2, I3}, {I1, I2}, {I1, I3}, and all 3 are indeed frequent (count 4). (A bucket count ≥ min_sup doesn't *guarantee* each item in it is frequent, since several itemsets may share a bucket, so survivors are still counted; but a low bucket guarantees infrequency.)

**Improve Apriori by hashing (prunes C2 using bucket counts), transaction reduction, partitioning (2 scans), sampling and dynamic itemset counting. In the example, hashing cuts 10 candidate pairs to 3.**

---

## 4. FP-growth · Slow down

**Idea:** skip candidate generation altogether. Compress the database into a prefix tree (**FP-tree**) where transactions sharing items share a path, then mine it recursively. Two scans total.

**Steps:**

1. Scan 1: count items; drop infrequent ones; sort the frequent items by **descending support** (the F-list).
2. Scan 2: insert each transaction (items in F-list order) into the tree, incrementing counts along shared prefixes. A **header table** links all nodes of each item.
3. Mine bottom-up: for each item (least frequent first), collect its **conditional pattern base** (the prefix paths leading to it, with counts), build its **conditional FP-tree** (keep items frequent within that base), and generate frequent patterns by adding the item as a suffix. Recurse.

**Example** (the same 9 transactions, min support count 2). F-list: I2:7, I1:6, I3:6, I4:2, I5:2.

| Item | Conditional pattern base | Conditional FP-tree | Frequent patterns |
| --- | --- | --- | --- |
| I5 | {I2, I1: 1}, {I2, I1, I3: 1} | ⟨I2: 2, I1: 2⟩ | {I2, I5}: 2, {I1, I5}: 2, {I2, I1, I5}: 2 |
| I4 | {I2, I1: 1}, {I2: 1} | ⟨I2: 2⟩ | {I2, I4}: 2 |
| I3 | {I2, I1: 2}, {I2: 2}, {I1: 2} | ⟨I2: 4, I1: 2⟩, ⟨I1: 2⟩ | {I2, I3}: 4, {I1, I3}: 4, {I2, I1, I3}: 2 |
| I1 | {I2: 4} | ⟨I2: 4⟩ | {I2, I1}: 4 |

**FP-growth vs Apriori:** no candidate generation, only 2 DB scans, a compact tree in memory; much faster on dense data. Downside: the tree may not fit in memory for huge sparse data, and recursion is complex.

---

## 5. Eclat (vertical format) · Slow down

Apriori and FP-growth use the **horizontal** format (TID → items). **Eclat** flips it to the **vertical** format: **item → set of TIDs containing it** (the tid-list). The support of an itemset is just the size of its tid-list, and the tid-list of a bigger set is the **intersection** of its parts' tid-lists. No need to rescan the database.

> **Endsem 2025 · Q3(b) · 4.5 marks**
> For the database T1 {A, B, C, D}, T2 {A, C, D, F}, T3 {A, C, D, E, G}, T4 {A, B, D, F}, T5 {B, C, G}, T6 {D, F, G}, T7 {A, B, G}, T8 {C, D, F, G}, with min_sup = 3, enumerate all frequent itemsets using the Eclat method, showing the vertical database.

**Answer.**

**Step 1: vertical database** (1-itemsets with tid-lists):

| Item | Tid-list | Support |
| --- | --- | --- |
| A | T1, T2, T3, T4, T7 | 5 |
| B | T1, T4, T5, T7 | 4 |
| C | T1, T2, T3, T5, T8 | 5 |
| D | T1, T2, T3, T4, T6, T8 | 6 |
| E | T3 | 1 ✗ |
| F | T2, T4, T6, T8 | 4 |
| G | T3, T5, T6, T7, T8 | 5 |

E (support 1) is infrequent and dropped.

**Step 2: 2-itemsets by intersecting tid-lists** (keep support ≥ 3):

| Itemset | Tid-list (intersection) | Support |
| --- | --- | --- |
| AB | T1, T4, T7 | 3 ✓ |
| AC | T1, T2, T3 | 3 ✓ |
| AD | T1, T2, T3, T4 | 4 ✓ |
| AF | T2, T4 | 2 ✗ |
| AG | T3, T7 | 2 ✗ |
| BC | T1, T5 | 2 ✗ |
| BD | T1, T4 | 2 ✗ |
| BF | T4 | 1 ✗ |
| BG | T5, T7 | 2 ✗ |
| CD | T1, T2, T3, T8 | 4 ✓ |
| CF | T2, T8 | 2 ✗ |
| CG | T3, T5, T8 | 3 ✓ |
| DF | T2, T4, T6, T8 | 4 ✓ |
| DG | T3, T6, T8 | 3 ✓ |
| FG | T6, T8 | 2 ✗ |

**Step 3: 3-itemsets** (intersect frequent 2-itemsets sharing a prefix):

| Itemset | Tid-list | Support |
| --- | --- | --- |
| ABC (AB ∩ AC) | T1 | 1 ✗ |
| ABD (AB ∩ AD) | T1, T4 | 2 ✗ |
| ACD (AC ∩ AD) | T1, T2, T3 | 3 ✓ |
| CDG (CD ∩ CG) | T3, T8 | 2 ✗ |
| DFG (DF ∩ DG) | T6, T8 | 2 ✗ |

**Step 4:** only one frequent 3-itemset (ACD), so no 4-itemsets can be formed. Stop.

**All frequent itemsets (min_sup = 3):**

- **1-itemsets:** A (5), B (4), C (5), D (6), F (4), G (5)
- **2-itemsets:** AB (3), AC (3), AD (4), CD (4), CG (3), DF (4), DG (3)
- **3-itemsets:** ACD (3)

**6 + 7 + 1 = 14 frequent itemsets, the largest being {A, C, D} with support 3.**

**Eclat's advantage:** supports come from fast set intersections, with no repeated database scans. **Drawback:** tid-lists can get long for dense data (the **diffset** variant stores differences instead).

---

## 6. Mining closed and max patterns · Quick

Mining *all* frequent itemsets explodes: a frequent 100-itemset has $2^{100} - 1$ frequent subsets. So we mine compressed forms:

- **Closed frequent itemsets** (lossless: every frequent itemset's support can be recovered). Algorithms: **CLOSET** (FP-tree based), **CHARM** (vertical, Eclat-like). Pruning tricks: **item merging** (if every transaction containing X also contains Y, merge Y into X) and **sub-itemset pruning**.
- **Maximal frequent itemsets** (lossy: tell you *what* is frequent but not each subset's support). Algorithm: **MaxMiner** (look-ahead: if a set plus all its possible extensions is frequent, skip the subsets).

In Q3(a) above, the maximal ones are {B, C, D}, {A, B, C, E}, {A, B, D, E}; for example {A, B} (5) is closed, since no superset has support 5.

---

## 7. Quick recap

- support = count/N; confidence(X ⇒ Y) = sup(X ∪ Y) / sup(X); strong = both thresholds met; lift > 1 = positive correlation.
- Apriori property: subsets of frequent sets are frequent → join, prune, count, level by level.
- Rules: for each frequent l and subset s, $s \Rightarrow l - s$ if count(l)/count(s) ≥ min_conf.
- Speed-ups: hashing (bucket count < min_sup prunes C2), transaction reduction, partitioning (2 scans), sampling, DIC.
- FP-growth: F-list order, FP-tree, conditional pattern bases, no candidates, 2 scans.
- Eclat: vertical tid-lists; support = |tid-list|; extend by intersection.
- Closed (no superset with equal support) vs maximal (no frequent superset).
