# DM Unit 3: Basic Classification: Decision Trees and Naive Bayes

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** classification learns from **labelled** examples to put new items into classes. Two classic ways: a **decision tree** (ask the most informative question first, using information gain / gain ratio / Gini) and **Naive Bayes** (use probabilities, assuming attributes are independent given the class).

**What the endsem asks from here:** one Naive Bayes numerical and one information-gain numerical, both guaranteed-style. 2025's Q4(a) and Q4(b) were exactly these.

---

## 1. Classification vs prediction · Quick

- **Classification** predicts a **categorical label**: spam/not spam, hire/don't hire.
- **Prediction (numeric prediction, regression)** predicts a **continuous value**: house price, tomorrow's temperature.

**Two-step process:**

1. **Learning (training):** build a model from a **training set** of records whose class labels are known (that's why it's called **supervised** learning).
2. **Classification (testing/use):** check the model's accuracy on a separate **test set**; if acceptable, use it on new data.

Clustering, by contrast, is **unsupervised**: no labels are given.

---

## 2. Decision tree induction · Slow down

A decision tree is a flowchart of questions: each **internal node** tests an attribute, each **branch** is an outcome, each **leaf** is a class. It's how a doctor thinks: "Fever? → yes → Cough? → yes → likely flu".

**Basic algorithm (ID3 / C4.5 / CART, greedy, top-down):**

1. Start with all training records at the root.
2. If all records have the same class → make a leaf with that class.
3. Otherwise pick the **best attribute** (by an attribute selection measure), split the records by its values, and repeat on each branch.
4. Stop when a node is pure, no attributes are left (use the majority class), or no records remain.

The whole art is in step 3: which question is "best"? The one that makes the branches **purest**.

---

## 3. Attribute selection measures · Slow down

**Entropy** measures impurity (mixedness) of a set D with class proportions $p_i$:

```latex
\text{Info}(D) = -\sum_i p_i \log_2 p_i
```

A 50/50 set has entropy 1 (maximum confusion); a pure set has 0.

**Information gain (ID3):** how much splitting on attribute A reduces entropy:

```latex
\begin{aligned}
\text{Info}_A(D) &= \sum_j \frac{|D_j|}{|D|}\,\text{Info}(D_j) \\
\text{Gain}(A) &= \text{Info}(D) - \text{Info}_A(D)
\end{aligned}
```

Pick the attribute with the **highest gain**.

**Gain ratio (C4.5):** information gain is biased towards attributes with many values (a "student ID" attribute would split into pure single-record branches, gain = maximum, yet useless). So divide by the split's own entropy:

```latex
\text{SplitInfo}_A(D) = -\sum_j \frac{|D_j|}{|D|}\log_2\frac{|D_j|}{|D|}, \qquad \text{GainRatio}(A) = \frac{\text{Gain}(A)}{\text{SplitInfo}_A(D)}
```

**Gini index (CART):** another impurity measure; CART makes **binary** splits:

```latex
\text{Gini}(D) = 1 - \sum_i p_i^2, \qquad \text{Gini}_A(D) = \sum_j \frac{|D_j|}{|D|}\,\text{Gini}(D_j)
```

Pick the split with the **lowest** Gini (largest reduction).

> **Endsem 2025 · Q4(b) · 4.5 marks**
> Data on whether a child goes out to play (12 days): attributes Weather, Temperature, Humidity, Wind; label Play. Describe and calculate the information gain for each attribute and choose the feature to split at the root of the decision tree.

| Day | Weather | Temp | Humidity | Wind | Play |
| --- | --- | --- | --- | --- | --- |
| 1 | Sunny | Hot | High | Weak | No |
| 2 | Cloudy | Hot | High | Weak | Yes |
| 3 | Sunny | Mild | Normal | Strong | Yes |
| 4 | Cloudy | Mild | High | Strong | Yes |
| 5 | Rainy | Mild | High | Strong | No |
| 6 | Rainy | Cool | Normal | Strong | No |
| 7 | Rainy | Mild | High | Weak | Yes |
| 8 | Sunny | Hot | High | Strong | No |
| 9 | Cloudy | Hot | Normal | Weak | Yes |
| 10 | Rainy | Mild | High | Strong | No |
| 11 | Rainy | Cool | Normal | Strong | No |
| 12 | Cloudy | Hot | High | Weak | Yes |

**Answer.**

**Information gain** = expected reduction in entropy from splitting on an attribute; the root should be the attribute with the highest gain.

**Entropy of the whole set:** 6 Yes, 6 No.

```latex
\text{Info}(D) = -\tfrac{6}{12}\log_2\tfrac{6}{12} - \tfrac{6}{12}\log_2\tfrac{6}{12} = 1.0
```

**Weather:** Sunny (3: 1 Yes, 2 No), Cloudy (4: 4 Yes, 0 No), Rainy (5: 1 Yes, 4 No).

```latex
\begin{aligned}
\text{Info(Sunny)} &= -\tfrac13\log_2\tfrac13 - \tfrac23\log_2\tfrac23 = 0.918 \\
\text{Info(Cloudy)} &= 0 \quad (\text{pure}) \\
\text{Info(Rainy)} &= -\tfrac15\log_2\tfrac15 - \tfrac45\log_2\tfrac45 = 0.722 \\
\text{Info}_{\text{Weather}} &= \tfrac{3}{12}(0.918) + \tfrac{4}{12}(0) + \tfrac{5}{12}(0.722) = 0.530 \\
\text{Gain(Weather)} &= 1 - 0.530 = 0.470
\end{aligned}
```

**Temperature:** Hot (5: 3 Yes, 2 No), Mild (5: 3 Yes, 2 No), Cool (2: 0 Yes, 2 No).

```latex
\begin{aligned}
\text{Info(Hot)} = \text{Info(Mild)} &= -\tfrac35\log_2\tfrac35 - \tfrac25\log_2\tfrac25 = 0.971, \quad \text{Info(Cool)} = 0 \\
\text{Info}_{\text{Temp}} &= \tfrac{5}{12}(0.971) + \tfrac{5}{12}(0.971) + 0 = 0.809 \\
\text{Gain(Temp)} &= 1 - 0.809 = 0.191
\end{aligned}
```

**Humidity:** High (8: 4 Yes, 4 No), Normal (4: 2 Yes, 2 No). Both halves are 50/50, entropy 1 each.

```latex
\text{Info}_{\text{Humidity}} = \tfrac{8}{12}(1) + \tfrac{4}{12}(1) = 1.0, \qquad \text{Gain(Humidity)} = 0
```

**Wind:** Weak (5: 4 Yes, 1 No), Strong (7: 2 Yes, 5 No).

```latex
\begin{aligned}
\text{Info(Weak)} &= 0.722, \quad \text{Info(Strong)} = -\tfrac27\log_2\tfrac27 - \tfrac57\log_2\tfrac57 = 0.863 \\
\text{Info}_{\text{Wind}} &= \tfrac{5}{12}(0.722) + \tfrac{7}{12}(0.863) = 0.804 \\
\text{Gain(Wind)} &= 1 - 0.804 = 0.196
\end{aligned}
```

| Attribute | Gain |
| --- | --- |
| **Weather** | **0.470** |
| Wind | 0.196 |
| Temperature | 0.191 |
| Humidity | 0.000 |

**Weather has the highest information gain (0.470), so it is the root.** The Cloudy branch is already pure (all Yes) and becomes a leaf; Sunny and Rainy are split further using the remaining attributes. Humidity, with zero gain, tells us nothing at this level.

For comparison: gain ratio of Weather = 0.470 / SplitInfo (1.555) = 0.302; Gini drops from 0.5 to 0.244 when splitting on Weather (Humidity leaves it at 0.5). All three measures agree on Weather.

---

## 4. Tree pruning · Quick

A fully grown tree memorises noise and outliers (**overfitting**). Pruning removes unreliable branches.

- **Pre-pruning:** stop growing early, e.g. if the gain is below a threshold or a node has too few records. Fast, but may stop too soon.
- **Post-pruning:** grow the full tree, then remove subtrees and replace them with leaves when that doesn't hurt (or improves) accuracy on validation data. Examples: **cost-complexity pruning** (CART), **pessimistic pruning** (C4.5). Usually more reliable.

Advantages of decision trees: easy to understand and convert to IF-THEN rules, no domain knowledge needed, fast. Disadvantages: unstable (small data changes → different tree), greedy (not globally optimal), overfitting without pruning.

---

## 5. Bayes' theorem · Quick

**Bayes' theorem** flips a conditional probability: from "how likely is this evidence if the hypothesis is true" to "how likely is the hypothesis given the evidence".

```latex
P(H \mid X) = \frac{P(X \mid H)\,P(H)}{P(X)}
```

- $P(H)$: **prior** (before seeing the data), $P(H \mid X)$: **posterior**, $P(X \mid H)$: **likelihood**, $P(X)$: evidence (same for all classes, so it can be ignored when comparing).

Everyday example: 1% of people have a disease, the test detects 99% of cases, but also flags 5% of healthy people. If you test positive, $P(\text{disease} \mid +) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.05 \times 0.99} \approx 17\%$, not 99%, because the disease is rare.

---

## 6. Naive Bayesian classification · Slow down

To classify a record $X = (x_1, \dots, x_n)$, compute $P(C_i \mid X)$ for every class and pick the **largest**. Since $P(X)$ is the same for all classes, compare only $P(X \mid C_i)\,P(C_i)$.

The **naive** assumption: attributes are **conditionally independent given the class**, so the likelihood is a simple product:

```latex
P(X \mid C_i) = \prod_{k=1}^{n} P(x_k \mid C_i)
```

"Naive" because in reality attributes are often related (effort and GPA probably are), but the classifier still works remarkably well.

**Zero-probability problem:** if some value never occurs with a class, one factor is 0 and wipes out the whole product. Fix: **Laplacian correction** (add 1 to each count, and the number of distinct values to the denominator).

For continuous attributes, use a Gaussian: $P(x_k \mid C_i) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ with the class's mean and standard deviation.

> **Endsem 2025 · Q4(a) · 4.5 marks**
> Hypothetical data on students and whether each should be hired:
> Sarah (Excellent, Lots, Average, Yes), Dana (Poor, Some, Average, No), Alex (Excellent, Some, Average, No), Annie (Poor, Lots, Poor, Yes), Emily (Excellent, Lots, Excellent, Yes), Pete (Poor, Lots, Excellent, No), John (Poor, Lots, Excellent, No), Kathy (Excellent, Some, Poor, No), with attributes (Attendance, Effort, GPA, Hirable).
> Use a Naive Bayes classifier to decide whether someone with **Excellent attendance, Poor GPA and Lots of effort** should be hired. Discuss your solution.

**Answer.**

X = (Attendance = Excellent, Effort = Lots, GPA = Poor). Compare $P(X \mid \text{Yes})P(\text{Yes})$ with $P(X \mid \text{No})P(\text{No})$.

**Priors:** 8 students: Yes = Sarah, Annie, Emily (3); No = Dana, Alex, Pete, John, Kathy (5).

```latex
P(\text{Yes}) = \tfrac38, \qquad P(\text{No}) = \tfrac58
```

**Likelihoods**, counted within each class:

| | Yes (3 students) | No (5 students) |
| --- | --- | --- |
| Attendance = Excellent | Sarah, Emily: 2/3 | Alex, Kathy: 2/5 |
| Effort = Lots | Sarah, Annie, Emily: 3/3 | Pete, John: 2/5 |
| GPA = Poor | Annie: 1/3 | Kathy: 1/5 |

**Products:**

```latex
\begin{aligned}
P(X \mid \text{Yes})\,P(\text{Yes}) &= \tfrac23 \times \tfrac33 \times \tfrac13 \times \tfrac38 = \tfrac{2}{9} \times \tfrac38 = 0.0833 \\
P(X \mid \text{No})\,P(\text{No}) &= \tfrac25 \times \tfrac25 \times \tfrac15 \times \tfrac58 = \tfrac{4}{125} \times \tfrac58 = 0.0200
\end{aligned}
```

0.0833 > 0.0200, so the classifier predicts **Hirable = Yes**. Normalising, $P(\text{Yes} \mid X) = \frac{0.0833}{0.0833 + 0.0200} = 0.806$, about **81%**.

**Discussion:** the poor GPA counts against the student (1/3 among hires), but **lots of effort** is decisive: every hired student had lots of effort (3/3), while only 2 of 5 rejected students did, and excellent attendance also favours hiring. No zero counts occurred, so no Laplace correction was needed. The result relies on the naive assumption that attendance, effort and GPA are independent given the class, and on a very small sample of 8, so in practice it's a weak estimate.

**Prediction: hire (Yes), with posterior ≈ 0.81 vs 0.19.**

---

## 7. Quick recap

- Classification: labels (supervised); prediction: numbers; clustering: no labels.
- Entropy $-\sum p\log_2 p$; Gain = Info(D) − weighted child entropy; pick the highest.
- Gain ratio = Gain / SplitInfo (fixes bias to many-valued attributes); Gini = $1 - \sum p^2$, pick the lowest.
- Pruning: pre (stop early) vs post (grow then cut).
- Bayes: posterior ∝ likelihood × prior.
- Naive Bayes: multiply $P(x_k \mid C)$ and $P(C)$, choose the larger; Laplace correction for zeros.
