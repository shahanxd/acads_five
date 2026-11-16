# RUN: DM Classification and Clustering

Nov 6, 2026 · @shahan

Supervised learning and clustering for Sessional-2, with every recent question solved where it belongs. Allow about 2.5 hours. **Every numerical was recomputed with a script.**

## How this run works

Read the idea, try the PYQ in its box, then check the solution right under it. The line to write in the exam is in bold.

**Scope:** "Supervised Learning and Clustering" maps to syllabus Units 3, 4 and 5 (basic classification, advanced classification and prediction, cluster analysis). This run covers **every topic those three units list**, plus SVM and DBSCAN, which aren't in the syllabus text but were asked in last year's papers. Sir stopped somewhere, so anything past that point is free endsem prep.

**What the paper likes:** an entropy and information gain table, a Naive Bayes prediction, a k-means run shown round by round, and a single-link dendrogram. All four are pure arithmetic once you know the recipe, and arithmetic can't surprise you.

**Videos:** StatQuest on YouTube, for Decision Trees, Naive Bayes, Support Vector Machines, K-means and Hierarchical Clustering. Notes are in `Data Mining/Notes/`. Sir's own slides for Units 3, 4 and 5 by Mr. Hannan Mansoor (the files Unit 3 IDM P1 and P2, Unit 4 IDM P1 and Unit 5 IDM) are now in that folder. On 16 Nov this run was realigned to them: every slide topic is covered, and every worked example on the slides is solved here too, checked by script. Sections added from the slides are written for a first read.

**Papers used:** CSE-501 Sessional-2 2025 and Endsem 2025, the Data Analytics Honours Sessional-2 2025 (the same clustering syllabus), and the CSDS Sessional-2 2026 paper from this year.

## Stop 1: Classification basics

**Classification** learns a model from labelled training data, then predicts the class label of new data. It's **supervised** because the labels are given. Clustering, from Stop 6 on, has no labels, so it's **unsupervised**.

**The vocabulary from the slides.** The training data is a set of records, each written as a pair **(x, y)**:

- **x** is the **attribute set**, the inputs describing the record. Other names: predictors, independent variables.
- **y** is the **class label**, the answer you want to learn. Other names: response, dependent variable, decision attribute, output.

The task is to learn a **model** (a rule, a tree or a formula) that maps any x to one of the predefined labels y.

**Classification vs numeric prediction:**

|  | Classification | Numeric prediction |
| --- | --- | --- |
| Predicts | A **category** (discrete label): spam or not, yes or no | A **number** (continuous value): price, temperature |
| Examples | Decision tree, Naive Bayes, SVM | Regression (Stop 5) |

The two steps:

1. **Learning:** build the model from the training set.
2. **Classification:** check accuracy on a separate test set, then use the model on new tuples.

The slides spell out the details of the two steps:

- **Step 1, model construction:** every training tuple already has its class label. The model is expressed as classification rules, a decision tree or a mathematical formula.
- **Step 2, model usage:** compare the model's predictions on a **test set** with the known labels. The test set must be **independent** of the training set; testing on the training data rewards memorising and gives an over-optimistic score (overfitting). If the accuracy is acceptable, use the model on new data.
- If a held-out set is used to **choose between models**, it's called a **validation set**.

**Classification techniques** named on the slides:

| Kind | Methods |
| --- | --- |
| Base classifiers | Decision trees, rule-based methods, nearest neighbour, Naive Bayes and Bayesian belief networks, SVM, neural networks |
| Ensemble classifiers (many models voting) | Boosting, bagging, random forests (Stop 5C) |

```latex
\text{Accuracy} = \frac{\text{correctly classified test tuples}}{\text{total test tuples}}
```

| Learner | When it works | Examples |
| --- | --- | --- |
| Eager | Builds a general model during training | Decision tree, Naive Bayes, SVM |
| Lazy | Stores the training data, and works only when a query arrives | k-nearest neighbour, case-based reasoning |

> **PYQ, Sessional-2 2025 Q3(ii), 1 mark.** Compare the advantages and disadvantages of eager classification versus lazy classification.

**Answer:**

| Basis | Eager | Lazy |
| --- | --- | --- |
| Training time | High, the model is built up front | Almost none, data is just stored |
| Prediction time | Fast | Slow, all the work happens per query |
| Storage | Only the model | The whole training set |
| Hypothesis | One global model | Local, built around each query |
| Adapts to new data | Needs retraining | Just add the tuple |

**Eager learners pay at training time and predict fast. Lazy learners train instantly and pay at every prediction.** It's the difference between studying all semester and starting the night before, except here both actually work.

## Stop 2: Decision trees

A decision tree asks one attribute question at each node, splitting the data until each leaf is (nearly) one class. The whole game is picking the **best attribute to split on**: the one that leaves the children purest.

**Anatomy of a decision tree** (it looks like a flowchart):

- The **root node** is the first question asked, at the top.
- Each **internal node** tests one attribute ("Home Owner?").
- Each **branch** is one outcome of that test (Yes or No).
- Each **leaf node** holds a class label, the final answer.

The tree is built **top-down, recursively, by divide and conquer**: split the data, then treat each piece as a smaller problem of the same kind.

**Why decision trees are popular** (straight from the slides): they need no domain knowledge or parameter tuning, they handle many attributes, they're easy for humans to read, learning and classifying are fast, and accuracy is generally good. They're used in medicine, manufacturing, finance, astronomy and molecular biology.

**The slides' example tree** predicts whether a borrower defaults on a loan. It was learned from 10 records with Home Owner, Marital Status (MarSt) and Annual Income:

```
                 Home Owner?
                /           \
             Yes             No
              |               |
        Defaulted = No     MarSt?
                         /        \
              Single, Divorced     Married
                      |               |
                Income < 80K?    Defaulted = No
                 /         \
              Yes           No
               |             |
        Defaulted = No   Defaulted = Yes
```

To classify a test record (Home Owner = No, MarSt = Married, Income = 80K), start at the root. Home Owner is No, so go right. MarSt is Married, so go right. That's a leaf: **Defaulted = No**. Income was never even looked at.

**Decision tree algorithms named on the slides:** Hunt's algorithm (one of the earliest, and the base of the others), ID3 (Iterative Dichotomiser 3), C4.5 (ID3's successor), CART (Classification and Regression Trees), SLIQ and SPRINT (both built for large, scalable datasets).

**Hunt's algorithm.** Let Dₜ be the training records that reach node t.

1. If every record in Dₜ has the same class y, then t is a **leaf** labelled y.
2. Otherwise, choose an **attribute test** to split Dₜ into smaller subsets, make a child node for each, and apply the same procedure to each child (recursion).

The slides grow the loan tree in four stages. The pair (a, b) means a records with Defaulted = No and b with Yes:

| Stage | What happens | Counts |
| --- | --- | --- |
| (a) | One leaf holding all 10 records, labelled with the majority, Defaulted = No | (7, 3): mixed, so it must be split |
| (b) | Split on Home Owner. Yes branch: all No, so it becomes a leaf. No branch: still mixed | Yes (3, 0), No (4, 3) |
| (c) | Split the No branch on MarSt. Married: all No, a leaf. Single or Divorced: mixed | Married (3, 0), Single/Divorced (1, 3) |
| (d) | Split Single/Divorced on Income. Below 80K: No. At or above 80K: Yes. Every node is pure, so stop | \< 80K (1, 0), ≥ 80K (0, 3) |

**Two special cases** need extra rules:

- **An empty child** (no training record has that combination of values): make it a leaf with the **majority class of its parent**.
- **Records with identical attribute values but different classes** can't be split any further: make the node a leaf with the **majority class of its own records**.

**Design issues** for any tree-growing algorithm:

1. **How to split:** how to express a test for each attribute type, and how to measure which test is best (the next part).
2. **When to stop:** stop when all records share a class or have identical attribute values, or stop early (pre-pruning, below).

**Test conditions by attribute type:**

| Attribute type | Multi-way split | Binary split |
| --- | --- | --- |
| **Binary** (Yes/No) | Same as binary | Two outcomes |
| **Nominal** (unordered categories: Single, Married, Divorced) | One branch per value | Any grouping into two sets, such as {Married} vs {Single, Divorced} |
| **Ordinal** (ordered categories: Small \< Medium \< Large \< Extra Large) | One branch per value | Two groups that **keep the order**: {Small, Medium} vs {Large, Extra Large} is fine, but {Small, Large} vs {Medium, Extra Large} breaks the order and isn't allowed |
| **Continuous** (Income) | Discretise into ranges: \< 10K, 10K to 25K, 25K to 50K, 50K to 80K, > 80K | A threshold test: Income > 80K? Yes or No |

**Attribute selection measures** (also called **splitting rules**) are the heuristics that rank every candidate attribute; the best-scoring one becomes the split. The three on the syllabus are information gain, gain ratio and the Gini index, coming up next.

**The impurity measures**, where pᵢ is the fraction of class i in a node:

```latex
\begin{aligned}
\text{Entropy}(D) &= -\sum_i p_i \log_2 p_i \\
\text{Gini}(D) &= 1 - \sum_i p_i^2 \\
\text{Error}(D) &= 1 - \max_i p_i
\end{aligned}
```

All three are 0 for a pure node. For two classes, entropy peaks at 1, and Gini and error both peak at 0.5, when the split is 50:50.

**Information gain** is how much a split lowers entropy, weighting each child by its size:

```latex
\text{Gain}(A) = \text{Entropy}(D) - \sum_{v} \frac{|D_v|}{|D|}\,\text{Entropy}(D_v)
```

ID3 picks the highest gain. C4.5 uses **gain ratio**, which divides by the split information to stop many-valued attributes like ID numbers from winning. CART uses Gini.

**Handy entropy values** to save calculator time: a 1:1 split gives 1, 1:3 gives 0.8113, 2:3 gives 0.9710, 1:4 gives 0.7219, 1:2 gives 0.9183, 2:5 gives 0.8631.

> **The slides' worked example (buys\_computer, from Han and Kamber).** 14 customers, class = buys\_computer. Which attribute goes at the root?

| # | age | income | student | credit\_rating | buys\_computer |
| --- | --- | --- | --- | --- | --- |
| 1 | ≤30 | high | no | fair | no |
| 2 | ≤30 | high | no | excellent | no |
| 3 | 31…40 | high | no | fair | yes |
| 4 | >40 | medium | no | fair | yes |
| 5 | >40 | low | yes | fair | yes |
| 6 | >40 | low | yes | excellent | no |
| 7 | 31…40 | low | yes | excellent | yes |
| 8 | ≤30 | medium | no | fair | no |
| 9 | ≤30 | low | yes | fair | yes |
| 10 | >40 | medium | yes | fair | yes |
| 11 | ≤30 | medium | yes | excellent | yes |
| 12 | 31…40 | medium | no | excellent | yes |
| 13 | 31…40 | high | yes | fair | yes |
| 14 | >40 | medium | no | excellent | no |

**Answer:** 9 yes and 5 no. The slides write I(p, n) for the entropy of a node with p yes and n no.

```latex
\text{Info}(D) = I(9, 5) = -\tfrac{9}{14}\log_2\tfrac{9}{14} - \tfrac{5}{14}\log_2\tfrac{5}{14} = 0.940
```

| age | yes | no | I(yes, no) |
| --- | --- | --- | --- |
| ≤30 (5) | 2 | 3 | 0.971 |
| 31…40 (4) | 4 | 0 | 0 |
| >40 (5) | 3 | 2 | 0.971 |

```latex
\begin{aligned}
\text{Info}_{\text{age}}(D) &= \tfrac{5}{14} I(2,3) + \tfrac{4}{14} I(4,0) + \tfrac{5}{14} I(3,2) = 0.694 \\
\text{Gain(age)} &= 0.940 - 0.694 = 0.246
\end{aligned}
```

The same steps for the other three attributes:

| Attribute | Split counts (yes, no) | Info after split | Gain |
| --- | --- | --- | --- |
| **age** | ≤30 (2, 3), 31…40 (4, 0), >40 (3, 2) | 0.694 | **0.246** |
| income | high (2, 2), medium (4, 2), low (3, 1) | 0.911 | 0.029 |
| student | yes (6, 1), no (3, 4) | 0.789 | 0.151 |
| credit\_rating | fair (6, 2), excellent (3, 3) | 0.892 | 0.048 |

**age has the highest information gain (0.246), so it's the root.** The 31…40 branch is pure (all yes) and becomes a leaf at once.

**Continuous-valued attributes** (like an exact age or income, not ranges). You need a **split point**:

1. Sort the attribute's values in increasing order.
2. Each midpoint between neighbours, (aᵢ + aᵢ₊₁) / 2, is a candidate split point.
3. For each candidate, split into D₁ (A ≤ split point) and D₂ (A > split point), and compute the expected information.
4. Pick the split point with the **minimum** expected information, which is the same as the maximum gain.

For example, incomes 60, 70, 75, 85 give candidate split points 65, 72.5 and 80.

> **PYQ, Sessional-2 2025 Q1, 4 marks.** Ten training examples with attributes A1, A2 and a class (+ or −). (i) What is the entropy of this collection with respect to the positive class? (ii) Calculate the information gains, and which is the best split according to the classification error rate?

| Instance | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | T | T | T | F | F | F | F | T | F | F |
| A2 | T | T | F | F | T | T | F | F | T | F |
| Class | + | + | − | + | − | + | − | + | + | − |

**Answer:** There are 6 positives and 4 negatives. (The A3 column in our copy is scribbled over; if it's numeric, sort its values and test a split point between each pair, the same way.)

**(i) Entropy:**

```latex
\text{Entropy}(D) = -\frac{6}{10}\log_2\frac{6}{10} - \frac{4}{10}\log_2\frac{4}{10} = 0.442 + 0.529 = 0.9710
```

**(ii) Gains.** Split each attribute and count the classes in each branch.

| Split | Branch | + | − | Entropy | Error |
| --- | --- | --- | --- | --- | --- |
| A1 | T (4) | 3 | 1 | 0.8113 | 1/4 |
| A1 | F (6) | 3 | 3 | 1.0000 | 3/6 |
| A2 | T (5) | 4 | 1 | 0.7219 | 1/5 |
| A2 | F (5) | 2 | 3 | 0.9710 | 2/5 |

```latex
\begin{aligned}
\text{Gain}(A1) &= 0.9710 - \left[\tfrac{4}{10}(0.8113) + \tfrac{6}{10}(1.0)\right] = 0.9710 - 0.9245 = 0.0464 \\
\text{Gain}(A2) &= 0.9710 - \left[\tfrac{5}{10}(0.7219) + \tfrac{5}{10}(0.9710)\right] = 0.9710 - 0.8464 = 0.1245
\end{aligned}
```

Now the classification error. Before any split the error is 1 − 6/10 = 0.4.

```latex
\begin{aligned}
\text{Error after A1} &= \tfrac{4}{10}\cdot\tfrac{1}{4} + \tfrac{6}{10}\cdot\tfrac{3}{6} = 0.1 + 0.3 = 0.4 \quad (\text{gain } 0) \\
\text{Error after A2} &= \tfrac{5}{10}\cdot\tfrac{1}{5} + \tfrac{5}{10}\cdot\tfrac{2}{5} = 0.1 + 0.2 = 0.3 \quad (\text{gain } 0.1)
\end{aligned}
```

**Entropy = 0.971. Gain(A1) = 0.046, Gain(A2) = 0.125. A2 is the best split by both information gain and classification error (0.3 vs 0.4).**

> **PYQ, Endsem 2025 Q4(b), 4.5 marks.** For the 12-day data below, where Play? is the class, describe and calculate the information gain for each attribute, and choose the feature to split at the root of the decision tree.

| Day | Weather | Temperature | Humidity | Wind | Play? |
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

**Answer:** There are 6 Yes and 6 No, so Entropy(D) = 1. Now count each value's Yes and No.

| Attribute | Value (count) | Yes | No | Entropy |
| --- | --- | --- | --- | --- |
| Weather | Sunny (3) | 1 | 2 | 0.9183 |
| Weather | Cloudy (4) | 4 | 0 | 0 |
| Weather | Rainy (5) | 1 | 4 | 0.7219 |
| Temperature | Hot (5) | 3 | 2 | 0.9710 |
| Temperature | Mild (5) | 3 | 2 | 0.9710 |
| Temperature | Cool (2) | 0 | 2 | 0 |
| Humidity | High (8) | 4 | 4 | 1 |
| Humidity | Normal (4) | 2 | 2 | 1 |
| Wind | Weak (5) | 4 | 1 | 0.7219 |
| Wind | Strong (7) | 2 | 5 | 0.8631 |

```latex
\begin{aligned}
\text{Gain(Weather)} &= 1 - \left[\tfrac{3}{12}(0.9183) + \tfrac{4}{12}(0) + \tfrac{5}{12}(0.7219)\right] = 1 - 0.5304 = 0.4696 \\
\text{Gain(Temperature)} &= 1 - \left[\tfrac{5}{12}(0.9710) + \tfrac{5}{12}(0.9710) + \tfrac{2}{12}(0)\right] = 1 - 0.8091 = 0.1909 \\
\text{Gain(Humidity)} &= 1 - \left[\tfrac{8}{12}(1) + \tfrac{4}{12}(1)\right] = 0 \\
\text{Gain(Wind)} &= 1 - \left[\tfrac{5}{12}(0.7219) + \tfrac{7}{12}(0.8631)\right] = 1 - 0.8043 = 0.1957
\end{aligned}
```

**Weather has the highest gain, 0.470, so it's the root.** The Cloudy branch is already pure (all Yes), so it becomes a leaf straight away. Humidity, with gain 0, is useless here: both its branches are exactly 50:50.

**Gain ratio (C4.5).** Information gain favours attributes with many values: an ID column would split into pure single-row leaves and score a perfect gain while predicting nothing. Gain ratio divides by the split information, which is large for many-valued splits.

```latex
\text{SplitInfo}(A) = -\sum_v \frac{|D_v|}{|D|}\log_2\frac{|D_v|}{|D|}, \qquad \text{GainRatio}(A) = \frac{\text{Gain}(A)}{\text{SplitInfo}(A)}
```

**Gini index (CART).** CART uses Gini impurity, and the best split gives the largest drop in impurity.

```latex
\text{Gini}_A(D) = \sum_v \frac{|D_v|}{|D|}\,\text{Gini}(D_v), \qquad \Delta\text{Gini}(A) = \text{Gini}(D) - \text{Gini}_A(D)
```

**The slides' numbers on the buys\_computer data.** Gain ratio for income: income splits the 14 records into high 4, medium 6, low 4.

```latex
\begin{aligned}
\text{SplitInfo}_{\text{income}}(D) &= -\tfrac{4}{14}\log_2\tfrac{4}{14} - \tfrac{6}{14}\log_2\tfrac{6}{14} - \tfrac{4}{14}\log_2\tfrac{4}{14} = 1.557 \\
\text{GainRatio(income)} &= \frac{0.029}{1.557} = 0.019
\end{aligned}
```

The attribute with the **maximum** gain ratio is chosen.

Gini index: CART considers only **binary** splits, so a 3-valued attribute like income has three ways to split into two groups. First the impurity before any split:

```latex
\text{gini}(D) = 1 - \left(\tfrac{9}{14}\right)^2 - \left(\tfrac{5}{14}\right)^2 = 0.459
```

| Income split | Sizes | Gini after split |
| --- | --- | --- |
| **{low, medium} vs {high}** | 10, 4 | **0.443** |
| {low, high} vs {medium} | 8, 6 | 0.458 |
| {medium, high} vs {low} | 10, 4 | 0.450 |

```latex
\text{gini}_{\text{income} \in \{low, medium\}}(D) = \tfrac{10}{14}\,\text{gini}(D_1) + \tfrac{4}{14}\,\text{gini}(D_2) = 0.443
```

**The lowest Gini (largest reduction in impurity) wins, so income splits as {low, medium} vs {high}.** For a continuous attribute, every candidate split point is tried the same way.

> **Practice, same 12-day data.** Find the gain ratio and the Gini reduction for each attribute. Does the root change?

**Answer:** Gini(D) = 1 − (0.5² + 0.5²) = 0.5.

| Attribute | Gain | SplitInfo | Gain ratio | Gini after split | Gini reduction |
| --- | --- | --- | --- | --- | --- |
| Weather (3/4/5) | 0.4696 | 1.5546 | **0.3021** | 0.2444 | **0.2556** |
| Temperature (5/5/2) | 0.1909 | 1.4834 | 0.1287 | 0.4000 | 0.1000 |
| Humidity (8/4) | 0 | 0.9183 | 0 | 0.5000 | 0 |
| Wind (5/7) | 0.1957 | 0.9799 | 0.1997 | 0.3714 | 0.1286 |

For example, the Weather row works out as:

```latex
\begin{aligned}
\text{SplitInfo(Weather)} &= -\tfrac{3}{12}\log_2\tfrac{3}{12} - \tfrac{4}{12}\log_2\tfrac{4}{12} - \tfrac{5}{12}\log_2\tfrac{5}{12} = 1.5546 \\
\text{GainRatio} &= \frac{0.4696}{1.5546} = 0.3021 \\
\text{Gini}_{\text{Weather}} &= \tfrac{3}{12}\left(1 - \tfrac{1}{9} - \tfrac{4}{9}\right) + \tfrac{4}{12}(0) + \tfrac{5}{12}\left(1 - \tfrac{1}{25} - \tfrac{16}{25}\right) = 0.2444
\end{aligned}
```

**Weather wins on all three measures, so the root stays Weather.** Notice Wind overtakes Temperature under gain ratio, because Temperature's three-way split gets penalised.

**Tree pruning.** A fully grown tree memorises noise and outliers, which is overfitting. Pruning cuts away branches that don't help on unseen data.

| Type | How | Trade-off |
| --- | --- | --- |
| Pre-pruning | Stop growing early, when a split's gain falls below a threshold | Fast, but a good split hiding behind a weak one gets missed |
| Post-pruning | Grow the full tree, then replace subtrees with leaves if the error doesn't rise (cost complexity in CART, pessimistic pruning in C4.5) | More accurate, more computation |

**Pruned trees are smaller, faster and more accurate on test data.**

Two details from the slides: pre-pruning's weak spot is that a good **threshold is hard to choose**. Post-pruning produces a sequence of progressively pruned trees, then uses a **separate set of data** (not the training data) to pick the best one.

**Comparing the three measures** (a common short question). All three usually give good results, but each has a bias:

| Measure | Used by | Bias |
| --- | --- | --- |
| Information gain | ID3 | Favours attributes with **many values** |
| Gain ratio | C4.5 | Fixes that, but tends to prefer **unbalanced** splits, where one partition is much smaller than the others |
| Gini index | CART | Also favours many-valued attributes; struggles when the **number of classes is large**; favours **equal-sized**, pure partitions |

**Other attribute selection measures** the slides name, one line each:

- **CHAID:** a popular tree algorithm whose measure is the χ² (chi-square) test of independence between the attribute and the class.
- **C-SEP:** beats information gain and Gini in some cases.
- **G-statistic:** closely approximates the χ² distribution.
- **MDL (Minimum Description Length):** the simplest solution wins. The best tree is the one needing the fewest bits to encode both the tree and its exceptions (the records it gets wrong).
- **Multivariate splits:** test a combination of attributes at once; CART can split on a linear combination.

Which measure is best? None is significantly better than the others.

**Enhancements to basic tree induction:**

- **Continuous attributes:** define new discrete attributes on the fly by cutting the range into intervals.
- **Missing values:** fill in the attribute's most common value, or assign a probability to each possible value.
- **Attribute construction:** build new attributes from sparsely represented ones. This reduces **fragmentation** (too few records left at deep nodes), **repetition** (the same attribute tested again and again down a branch) and **replication** (the same subtree copied in several places).

**Classification in large databases.** Real data can have millions of records and hundreds of attributes, more than fits in memory. Decision trees are popular here because they learn relatively fast, convert into simple IF-THEN rules, can use SQL queries to read the database, and match other methods on accuracy.

- **RainForest** keeps the expensive part, the class counts, separate from the tree logic. An **AVC-set** (Attribute, Value, Class label) of attribute X lists, for each value of X, how many records of each class have it. The **AVC-group** of a node is the set of AVC-sets of all its attributes. Only these small count tables need to fit in memory, not the data.

| AVC-set on age | buys = yes | buys = no |
| --- | --- | --- |
| ≤30 | 2 | 3 |
| 31…40 | 4 | 0 |
| >40 | 3 | 2 |

The AVC-sets on income, student and credit\_rating are the yes/no count columns from the buys\_computer table above.

- **BOAT (Bootstrapped Optimistic Algorithm for Tree construction)** uses **bootstrapping** (random sampling with replacement) to make several small samples that each fit in memory, builds a tree on each, and combines them into a tree T′ that turns out very close to the tree the full data would give. Its advantages: only **two scans** of the database, and it's **incremental** (new data can be added without starting over).

The slides close Unit 3's tree part with **presenting results visually**: SGI MineSet draws the tree in 3-D, and PBC (Perception-Based Classification) lets a user build the tree interactively from a visual display of the data.

## Stop 3: Naive Bayes

Bayes' theorem flips "how likely is this evidence, given the class" into "how likely is the class, given this evidence". The **naive** part assumes attributes are independent given the class, so the likelihood is just a product.

**Why Bayesian classification** (the slides' five reasons):

- **Statistical:** it predicts class membership probabilities, not just a label.
- **Foundation:** it rests on Bayes' theorem.
- **Performance:** even simple Naive Bayes is comparable to decision trees and some neural networks.
- **Incremental:** each new training example nudges the probabilities up or down, so prior knowledge combines with new data.
- **Standard:** even when exact Bayesian methods are too expensive, they set the optimal benchmark that other methods are measured against.

**The four words in Bayes' theorem.** X is the data sample (the "evidence"), and H is the hypothesis "X belongs to class C".

| Term | Symbol | Meaning, with the buys\_computer example |
| --- | --- | --- |
| **Prior** | P(H) | What you believed before seeing X: the chance anyone buys a computer, whatever their age or income |
| **Likelihood** | P(X \| H) | How likely this evidence is if H is true: given that someone buys, the chance they're 31…40 with medium income |
| **Evidence** | P(X) | How likely X is overall |
| **Posterior** | P(H \| X) | What you believe after seeing X. This is what classification wants |

In words: posterior = likelihood × prior ÷ evidence. The slides also give the **total probability theorem**, which builds P(X) by summing over every class:

```latex
P(B) = \sum_{i=1}^{M} P(B \mid A_i)\,P(A_i)
```

Predict the class Cᵢ with the highest posterior P(Cᵢ \| X). That's called the **maximum posteriori** rule. The practical difficulty of full Bayes is that it needs many probabilities, which costs a lot to compute, and that's exactly why the naive independence assumption is made.

```latex
\begin{aligned}
P(C \mid X) &= \frac{P(X \mid C)\,P(C)}{P(X)} \\
P(X \mid C) &= P(x_1 \mid C) \times P(x_2 \mid C) \times \dots \times P(x_n \mid C)
\end{aligned}
```

P(X) is the same for every class, so compare only P(X \| C) × P(C) and pick the biggest.

**The recipe:** priors from the class counts, then one conditional per attribute value in X, per class, then multiply.

**Zero-probability problem:** if one conditional is 0, the whole product becomes 0. The **Laplace correction** adds 1 to every count, and adds the number of values to the denominator.

The slides' Laplace example: 1000 tuples have income = low 0 times, medium 990 times and high 10 times. Without correction P(low) = 0, which would zero out any product it appears in. Add 1 to each of the 3 counts (so 3 to the total):

```latex
P(\text{low}) = \tfrac{0+1}{1000+3} = \tfrac{1}{1003}, \quad P(\text{medium}) = \tfrac{991}{1003}, \quad P(\text{high}) = \tfrac{11}{1003}
```

The corrected values are almost the same as the originals, but none is zero.

**Continuous attributes.** For a categorical attribute, P(xₖ \| Cᵢ) is just a count ratio. For a continuous one (an exact age, say), assume a **Gaussian** (normal, bell-shaped) distribution. Find the mean μ and standard deviation σ of that attribute within class Cᵢ, then plug xₖ into the bell curve:

```latex
P(x_k \mid C_i) = g(x_k, \mu_{C_i}, \sigma_{C_i}) = \frac{1}{\sqrt{2\pi}\,\sigma}\, e^{-\frac{(x_k - \mu)^2}{2\sigma^2}}
```

Example: if buyers' ages have μ = 38 and σ = 12, then for a 35-year-old:

```latex
g(35, 38, 12) = \frac{1}{\sqrt{2\pi} \times 12}\, e^{-\frac{9}{288}} = 0.0332 \times 0.969 = 0.0322
```

**Naive Bayes, pros and cons:**

| Advantages | Disadvantages |
| --- | --- |
| Easy to implement | Assumes class-conditional independence, which costs accuracy |
| Good results in most cases | Real attributes are often dependent. In a hospital, age and family history affect symptoms (fever, cough), which relate to diseases (lung cancer, diabetes). Naive Bayes can't model this |

The fix for dependencies is a **Bayesian belief network**, at the end of this stop.

> **PYQ, Sessional-2 2025 Q2, 4 marks.** Build a Naive Bayes model from the data below, and determine the species of X = (Color = Green, Legs = 2, Height = Tall, Smell = No).

| No. | Color | Legs | Height | Smell | Species |
| --- | --- | --- | --- | --- | --- |
| 1 | White | 3 | Short | Yes | M |
| 2 | Green | 2 | Tall | No | M |
| 3 | Green | 3 | Short | Yes | M |
| 4 | White | 3 | Short | Yes | M |
| 5 | Green | 2 | Short | No | H |
| 6 | White | 2 | Tall | No | H |
| 7 | White | 2 | Tall | No | H |
| 8 | White | 2 | Short | Yes | H |

**Answer:** Priors: P(M) = 4/8 and P(H) = 4/8.

| Conditional | M | H |
| --- | --- | --- |
| Color = Green | 2/4 | 1/4 |
| Legs = 2 | 1/4 | 4/4 |
| Height = Tall | 1/4 | 2/4 |
| Smell = No | 1/4 | 3/4 |

```latex
\begin{aligned}
P(X \mid M)\,P(M) &= \tfrac{2}{4} \cdot \tfrac{1}{4} \cdot \tfrac{1}{4} \cdot \tfrac{1}{4} \cdot \tfrac{4}{8} = \tfrac{1}{256} = 0.0039 \\
P(X \mid H)\,P(H) &= \tfrac{1}{4} \cdot \tfrac{4}{4} \cdot \tfrac{2}{4} \cdot \tfrac{3}{4} \cdot \tfrac{4}{8} = \tfrac{3}{64} = 0.0469
\end{aligned}
```

**0.0469 > 0.0039, so X is classified as species H.**

> **PYQ, Endsem 2025 Q4(a), 4.5 marks.** Using the student data below, use a Naive Bayes classifier to decide whether someone with Excellent attendance, Poor GPA and Lots of effort should be hired.

| Name | Attendance | Effort | GPA | Hirable |
| --- | --- | --- | --- | --- |
| Sarah | Excellent | Lots | Average | Yes |
| Dana | Poor | Some | Average | No |
| Alex | Excellent | Some | Average | No |
| Annie | Poor | Lots | Poor | Yes |
| Emily | Excellent | Lots | Excellent | Yes |
| Pete | Poor | Lots | Excellent | No |
| John | Poor | Lots | Excellent | No |
| Kathy | Excellent | Some | Poor | No |

**Answer:** Priors: P(Yes) = 3/8 and P(No) = 5/8.

| Conditional | Yes | No |
| --- | --- | --- |
| Attendance = Excellent | 2/3 | 2/5 |
| GPA = Poor | 1/3 | 1/5 |
| Effort = Lots | 3/3 | 2/5 |

```latex
\begin{aligned}
P(X \mid \text{Yes})\,P(\text{Yes}) &= \tfrac{2}{3} \cdot \tfrac{1}{3} \cdot 1 \cdot \tfrac{3}{8} = \tfrac{1}{12} = 0.0833 \\
P(X \mid \text{No})\,P(\text{No}) &= \tfrac{2}{5} \cdot \tfrac{1}{5} \cdot \tfrac{2}{5} \cdot \tfrac{5}{8} = \tfrac{1}{50} = 0.02
\end{aligned}
```

Normalising, P(Yes \| X) = 0.0833 / (0.0833 + 0.02) = 0.81.

**Hire: Yes, with a posterior of about 81%.** For the "discuss" part, note that every hired student put in Lots of effort, so that one attribute does most of the work.

> **PYQ, CSDS Sessional-2 2026 Q2, 6 marks (this year).** Ten students with Study Hours (H) and Attendance (A), class Pass or Fail. (i) Compute the priors. (ii) Compute all the conditional probabilities. (iii) Predict S11 (H = Medium, A = Good) and S12 (H = High, A = Poor).

| Student | H | A | Class |
| --- | --- | --- | --- |
| S1 | High | Good | Pass |
| S2 | Medium | Average | Pass |
| S3 | Low | Good | Fail |
| S4 | Medium | Poor | Pass |
| S5 | Low | Average | Fail |
| S6 | Medium | Poor | Fail |
| S7 | High | Average | Pass |
| S8 | Low | Poor | Fail |
| S9 | High | Good | Pass |
| S10 | Medium | Average | Pass |

**Answer:**

**(i)** P(Pass) = 6/10 and P(Fail) = 4/10.

**(ii)**

| Conditional | Pass (6) | Fail (4) |
| --- | --- | --- |
| H = High | 3/6 | 0/4 |
| H = Medium | 3/6 | 1/4 |
| H = Low | 0/6 | 3/4 |
| A = Good | 2/6 | 1/4 |
| A = Average | 3/6 | 1/4 |
| A = Poor | 1/6 | 2/4 |

**(iii)**

```latex
\begin{aligned}
\text{S11: } P(\text{Pass}) &\propto \tfrac{3}{6} \cdot \tfrac{2}{6} \cdot \tfrac{6}{10} = 0.100, \qquad P(\text{Fail}) \propto \tfrac{1}{4} \cdot \tfrac{1}{4} \cdot \tfrac{4}{10} = 0.025 \\
\text{S12: } P(\text{Pass}) &\propto \tfrac{3}{6} \cdot \tfrac{1}{6} \cdot \tfrac{6}{10} = 0.050, \qquad P(\text{Fail}) \propto \tfrac{0}{4} \cdot \tfrac{2}{4} \cdot \tfrac{4}{10} = 0
\end{aligned}
```

**S11 = Pass, and S12 = Pass.** S12's Fail score is 0 only because no Fail student had High hours. Mention that the Laplace correction would avoid the hard zero; the answer stays Pass either way.

> **The slides' worked example.** Using the 14-row buys\_computer table from Stop 2, classify X = (age ≤ 30, income = medium, student = yes, credit\_rating = fair).

**Answer:**

```latex
P(\text{yes}) = \tfrac{9}{14} = 0.643, \qquad P(\text{no}) = \tfrac{5}{14} = 0.357
```

| Conditional | buys = yes | buys = no |
| --- | --- | --- |
| age ≤ 30 | 2/9 = 0.222 | 3/5 = 0.6 |
| income = medium | 4/9 = 0.444 | 2/5 = 0.4 |
| student = yes | 6/9 = 0.667 | 1/5 = 0.2 |
| credit\_rating = fair | 6/9 = 0.667 | 2/5 = 0.4 |

```latex
\begin{aligned}
P(X \mid \text{yes}) &= 0.222 \times 0.444 \times 0.667 \times 0.667 = 0.044, & P(X \mid \text{yes})\,P(\text{yes}) &= 0.044 \times 0.643 = 0.028 \\
P(X \mid \text{no}) &= 0.6 \times 0.4 \times 0.2 \times 0.4 = 0.019, & P(X \mid \text{no})\,P(\text{no}) &= 0.019 \times 0.357 = 0.007
\end{aligned}
```

**0.028 > 0.007, so X buys a computer (buys\_computer = yes).**

> **Practice from the slides (slide 17).** Same data. Classify (1) X = (age ≤ 40, income = medium, student = yes, credit\_rating = fair), and (2) X = (age 31…40, income = medium, student = yes, credit\_rating = fair).

**Answer (1):** "age ≤ 40" covers both the ≤30 and 31…40 groups. Among the 9 buyers that's 2 + 4 = 6, and among the 5 non-buyers 3 + 0 = 3. The other three conditionals are as above.

```latex
\begin{aligned}
\text{yes: } & \tfrac{6}{9} \times \tfrac{4}{9} \times \tfrac{6}{9} \times \tfrac{6}{9} \times \tfrac{9}{14} = 0.1317 \times 0.643 = 0.0847 \\
\text{no: } & \tfrac{3}{5} \times \tfrac{2}{5} \times \tfrac{1}{5} \times \tfrac{2}{5} \times \tfrac{5}{14} = 0.0192 \times 0.357 = 0.0069
\end{aligned}
```

**(1) buys\_computer = yes (0.0847 vs 0.0069).**

**Answer (2):** No non-buyer is aged 31…40, so P(age = 31…40 \| no) = 0/5 = 0, and the whole "no" product collapses to 0. That's the zero-probability problem the slides warn about.

```latex
\begin{aligned}
\text{yes: } & \tfrac{4}{9} \times \tfrac{4}{9} \times \tfrac{6}{9} \times \tfrac{6}{9} \times \tfrac{9}{14} = 0.0878 \times 0.643 = 0.0564 \\
\text{no: } & \tfrac{0}{5} \times \dots = 0
\end{aligned}
```

With the Laplace correction (add 1 to each count; add 3 to the denominator for age and income, which have 3 values, and 2 for student and credit\_rating):

```latex
\begin{aligned}
\text{yes: } & \tfrac{5}{12} \times \tfrac{5}{12} \times \tfrac{7}{11} \times \tfrac{7}{11} \times \tfrac{9}{14} = 0.0452 \\
\text{no: } & \tfrac{1}{8} \times \tfrac{3}{8} \times \tfrac{2}{7} \times \tfrac{3}{7} \times \tfrac{5}{14} = 0.0021
\end{aligned}
```

**(2) buys\_computer = yes, with or without the Laplace correction. Mention the zero to show you spotted it.**

**Bayesian belief networks** (Unit 4) drop the naive assumption. Real attributes are often dependent: smoking affects both lung cancer and bronchitis. A BBN models this with two parts:

1. A **directed acyclic graph**: nodes are variables, and an arrow from X to Y means Y depends directly on X. Each node is conditionally independent of its non-descendants, given its parents.
2. A **conditional probability table (CPT)** at each node, giving P(node \| parents).

```
 FamilyHistory    Smoker
        \         /    \
         v       v      v
        LungCancer   Emphysema
          /      \
         v        v
   PositiveXRay  Dyspnea
```

The joint probability factorises along the graph:

```latex
P(x_1, \dots, x_n) = \prod_{i=1}^{n} P\left(x_i \mid \text{Parents}(x_i)\right)
```

**Naive Bayes is the special case where the class is the only parent of every attribute. A BBN allows any dependency, shown as a DAG with a CPT at each node.**

**More on belief networks, from the Unit 4 slides.** Other names: Bayesian network, Bayes net, probabilistic network, probabilistic directed acyclic graphical model.

- **Nodes** are random variables, and **links** (arrows) are dependencies: each arrow is a direction of influence. In A → C ← B, A and B are the **parents** of C, and C is their **descendant**.
- The graph must be **acyclic**: following the arrows must never bring you back where you started. A graph with a cycle is **not** a Bayesian network.
- Variables with no path between them are independent, given their parents. In the slides' X, Y → Z and Y → P example, Z and P don't depend on each other once Y is known.

For a small graph where B → A, and both A and B point into C, the joint probability is:

```latex
P(A, B, C) = P(B) \cdot P(A \mid B) \cdot P(C \mid A, B)
```

**The CPT for LungCancer** (its parents are FamilyHistory FH and Smoker S). One column per combination of parent values:

|  | FH, S | FH, ¬S | ¬FH, S | ¬FH, ¬S |
| --- | --- | --- | --- | --- |
| LungCancer = yes | 0.8 | 0.5 | 0.7 | 0.1 |
| LungCancer = no | 0.2 | 0.5 | 0.3 | 0.9 |

Read it straight off: P(LungCancer = yes \| FH = yes, S = yes) = 0.8, and P(LungCancer = no \| FH = no, S = no) = 0.9. Each column adds up to 1.

**Steps for answering a question with a belief network** (from the slides):

1. Draw the DAG and identify each variable's parents.
2. Write the joint probability as the product of P(variable \| parents), and read the needed values from the CPTs.
3. For a joint event, multiply the relevant probabilities.
4. For a conditional probability, divide by the probability of the evidence.
5. If the evidence can arise through several states, sum over all of them.

> **The slides' example 2: Fire, Smoke, Tampering, Alarm.** Fire causes Smoke; Fire and Tampering both cause Alarm. P(Smoke \| Fire) = 0.90 and P(Smoke \| ¬Fire) = 0.01. P(Alarm \| Fire, Tampering) = 0.5, P(Alarm \| Fire, ¬Tampering) = 0.99, P(Alarm \| ¬Fire, Tampering) = 0.85, P(Alarm \| ¬Fire, ¬Tampering) = 0.0001. Write the joint distribution and compute an example.

**Answer:** Fire and Tampering have no parents, Smoke's parent is Fire, and Alarm's parents are Fire and Tampering:

```latex
P(F, S, A, T) = P(F) \cdot P(T) \cdot P(S \mid F) \cdot P(A \mid F, T)
```

The slides don't list the root probabilities P(F) and P(T), so assume P(Fire) = 0.01 and P(Tampering) = 0.02 and say so. Then the chance of a fire, no tampering, smoke and an alarm:

```latex
P(F, \neg T, S, A) = 0.01 \times 0.98 \times 0.90 \times 0.99 = 0.0087
```

An example of step 5 (summing over states): if there's a fire, how likely is the alarm? Tampering is unknown, so sum over both cases:

```latex
P(A \mid F) = P(T)\,P(A \mid F, T) + P(\neg T)\,P(A \mid F, \neg T) = 0.02 \times 0.5 + 0.98 \times 0.99 = 0.980
```

**Joint = product of each node's CPT entry given its parents; here P(F, ¬T, S, A) = 0.0087 and P(Alarm \| Fire) = 0.980 under the assumed priors.**

**Training a belief network: four scenarios.** Experts usually know the direct dependencies well, which helps design the network; they give the conditional probabilities for those nodes, and the rest are computed from them.

| Scenario | Structure | Variables | What to do |
| --- | --- | --- | --- |
| 1 | Known | All observable | Just compute the CPT entries from counts |
| 2 | Known | Some hidden | **Gradient descent** (greedy hill-climbing): start the CPT weights at random values, move each step in the direction that improves the fit most, never backtrack; converges to a local optimum |
| 3 | Unknown | All observable | Search through the space of possible graphs to reconstruct the topology |
| 4 | Unknown | All hidden | No good algorithms known |

The slides end the topic with a textbook network for diagnosing **heart disease and heartburn** from exercise, diet, blood pressure and chest pain: the same idea with more nodes.

## Stop 4: Support Vector Machines

An SVM draws the boundary that keeps the **widest possible gap** between the two classes. Many lines separate the data, and the SVM picks the one with the biggest safety margin, so it generalises best.

```
   +   +            .  margin  .
     +    +        .           .         -
   +    +   ======.=====H=====.========    -   -
       +          .           .        -     -
                  .           .     -
          support vectors sit on the dashed edges
```

```latex
\begin{aligned}
\text{Hyperplane: } & \mathbf{w} \cdot \mathbf{x} + b = 0 \\
\text{Margin: } & \frac{2}{\lVert \mathbf{w} \rVert} \\
\text{Goal: } & \min \tfrac{1}{2}\lVert \mathbf{w} \rVert^2 \ \text{ subject to } \ y_i(\mathbf{w} \cdot \mathbf{x}_i + b) \ge 1
\end{aligned}
```

- **Support vectors** are the training points closest to the boundary. Only they decide the hyperplane; delete any other point and nothing changes.
- **Soft margin** allows a few points on the wrong side, with a penalty C, for noisy data.
- **Kernel trick:** when the data isn't linearly separable, map it to a higher dimension where it is, using a kernel such as polynomial, RBF (Gaussian) or sigmoid, without computing the mapping explicitly.

> **PYQ, Endsem 2025 Q4(c), 4.5 marks.** Explain linear SVM. Discuss the advantages and disadvantages of SVM.

**Answer:** A linear SVM separates two classes with the hyperplane w · x + b = 0 that maximises the margin 2 / ‖w‖ between the nearest points of each class, the support vectors. A new point is classified by the sign of w · x + b.

| Advantages | Disadvantages |
| --- | --- |
| High accuracy, and resists overfitting thanks to the maximum margin | Slow to train on large datasets |
| Works in high dimensions, even when features outnumber samples | Choosing the kernel and parameters (C, gamma) is tricky |
| Memory-efficient: only the support vectors are kept | No direct probability output |
| Handles non-linear data through kernels | Hard to interpret compared with a decision tree |

**Linear SVM = the maximum-margin hyperplane, set by the support vectors. Great accuracy, slow on big data.**

> **PYQ, Sessional-2 2025 Q3(i), 3 marks.** SVMs are highly accurate, but slow to train on a large set of data tuples. Discuss how to overcome this difficulty, and develop a scalable SVM algorithm for efficient classification of large datasets.

**Answer:** Training cost grows roughly with the square of the number of tuples, but only the tuples near the boundary matter. So shrink the data first, keeping the detail only where the boundary is. This is **CB-SVM** (clustering-based SVM), from Han and Kamber.

1. Build a **micro-cluster tree** (a CF-tree, as in BIRCH) separately for the positive and the negative tuples, in one scan of the data. Each node stores just a cluster summary: count, linear sum and squared sum.
2. Train an SVM on the **centroids** of the top-level clusters only. That's a tiny training set.
3. Find the clusters that lie **near the boundary**, within the margin or close to it. **Decluster** them, replacing each with its child clusters.
4. Retrain on the new set of centroids, and repeat until reaching the leaves.

Far-away clusters never get expanded, because they can't be support vectors.

Other options worth a line each: sampling the data, chunking (train on subsets, keep their support vectors), and SMO, which breaks the optimisation into the smallest possible pieces.

**Summarise the data with hierarchical micro-clusters, train on centroids, and expand only the clusters near the boundary.**

## Stop 5: Linear regression and MSE

This appeared in this year's CSDS paper, so it's cheap insurance. Regression predicts a **number**, not a class. Simple linear regression fits a straight line through the points that minimises the squared vertical errors.

```latex
\begin{aligned}
\hat{y} &= w x + b \\
\text{MSE} &= \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 \\
w &= \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}, \qquad b = \bar{y} - w\bar{x}
\end{aligned}
```

The formulas for w and b come from setting the derivatives of the MSE with respect to w and b to zero. Squaring makes every error positive and punishes big misses more than small ones.

> **PYQ, CSDS Sessional-2 2026 Q1(iii) (this year).** Find the Mean Squared Error for this data.

| X | 2 | 3 | 5 | 6 | 8 |
| --- | --- | --- | --- | --- | --- |
| Y-true | 6 | 4 | 5 | 8 | 10 |
| Y-pred | 7 | 5 | 6 | 7 | 9 |

**Answer:** The errors y − ŷ are −1, −1, −1, +1, +1.

```latex
\text{MSE} = \frac{(-1)^2 + (-1)^2 + (-1)^2 + 1^2 + 1^2}{5} = \frac{5}{5} = 1
```

**MSE = 1.**

**Non-linear regression.** When the points curve, transform the problem back into a linear one. A polynomial such as y = w₀ + w₁x + w₂x² + w₃x³ becomes linear by setting x₁ = x, x₂ = x² and x₃ = x³, then solving by least squares as usual. Exponential models become linear after taking logs. Regression trees and model trees handle the rest.

**Predictor error measures**, for numeric predictions, where d is the number of test tuples:

```latex
\begin{aligned}
\text{MAE} &= \frac{1}{d}\sum |y_i - \hat{y}_i|, \qquad \text{MSE} = \frac{1}{d}\sum (y_i - \hat{y}_i)^2, \qquad \text{RMSE} = \sqrt{\text{MSE}} \\
\text{Relative absolute error} &= \frac{\sum |y_i - \hat{y}_i|}{\sum |y_i - \bar{y}|}, \qquad \text{Relative squared error} = \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}
\end{aligned}
```

For the CSDS data above, MAE = 5/5 = 1 and RMSE = 1 too, because every error is exactly ±1.

## Stop 5B: Evaluating classifiers

**The confusion matrix**, for a two-class problem with positive as the class of interest:

|  | Predicted yes | Predicted no |
| --- | --- | --- |
| Actual yes | TP | FN |
| Actual no | FP | TN |

```latex
\begin{aligned}
\text{Accuracy} &= \frac{TP + TN}{P + N}, \qquad \text{Error rate} = 1 - \text{Accuracy} \\
\text{Sensitivity (recall)} &= \frac{TP}{P} = \frac{TP}{TP + FN}, \qquad \text{Specificity} = \frac{TN}{N} = \frac{TN}{TN + FP} \\
\text{Precision} &= \frac{TP}{TP + FP}, \qquad F_1 = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
\end{aligned}
```

Accuracy lies on imbalanced data. If 97% of patients are healthy, a model that always says "healthy" scores 97% accuracy and 0% sensitivity. That's why sensitivity and specificity exist.

> **Practice.** A cancer test is run on 1000 people, 100 of whom have cancer. It flags 120 people, 90 of whom really have cancer. Find the accuracy, sensitivity, specificity and precision.

**Answer:** TP = 90 and FN = 100 − 90 = 10. FP = 120 − 90 = 30, and TN = 900 − 30 = 870.

```latex
\begin{aligned}
\text{Accuracy} &= \frac{90 + 870}{1000} = 0.96 \\
\text{Sensitivity} &= \frac{90}{100} = 0.90 \\
\text{Specificity} &= \frac{870}{900} = 0.967 \\
\text{Precision} &= \frac{90}{120} = 0.75
\end{aligned}
```

**Accuracy 96%, sensitivity 90%, specificity 96.7%, precision 75%.** One in four positive results is a false alarm.

**Two more names the slides use:** accuracy is also called the **recognition rate**, and sensitivity is the **true positive recognition rate** (specificity is the true negative one). Precision measures **exactness** (of everything flagged positive, how much really is), and recall measures **completeness** (of all real positives, how many were caught). The two pull against each other, so the **F-measure** combines them into one number:

```latex
F_\beta = \frac{(1 + \beta^2)\,P \times R}{\beta^2 P + R}, \qquad F_1 = \frac{2PR}{P + R}
```

F₁ is the harmonic mean, with precision and recall weighted equally. A β of 2 counts recall twice as much as precision, and a β of 0.5 does the reverse.

> **The slides' worked example.** Cancer screening on 10,000 people. Actual cancer = yes: 90 predicted yes and 210 predicted no (300 in total). Actual cancer = no: 140 predicted yes and 9560 predicted no (9700 in total). Compute sensitivity, specificity, accuracy, error rate, precision, recall and F₁.

**Answer:** TP = 90, FN = 210, FP = 140, TN = 9560, P = 300, N = 9700.

```latex
\begin{aligned}
\text{Sensitivity} &= \tfrac{TP}{P} = \tfrac{90}{300} = 30.00\% \\
\text{Specificity} &= \tfrac{TN}{N} = \tfrac{9560}{9700} = 98.56\% \\
\text{Accuracy} &= \tfrac{90 + 9560}{10000} = 96.50\% \\
\text{Error rate} &= \tfrac{140 + 210}{10000} = 3.50\% \\
\text{Precision} &= \tfrac{90}{90 + 140} = 39.13\% \\
\text{Recall} &= \tfrac{90}{90 + 210} = 30.00\% \\
F_1 &= \tfrac{2 \times 39.13 \times 30.00}{39.13 + 30.00} = 33.96\%
\end{aligned}
```

**96.5% accuracy, yet only 30% of the cancers are caught. This is the class imbalance problem in one picture: the rare class (cancer, fraud, HIV-positive) is what matters, and accuracy hides how badly it's handled.**

The slides' other confusion matrix (play\_golf, 10,000 days: 6954 yes-yes, 46 yes-no, 412 no-yes, 2588 no-no) works the same way: accuracy 95.42%, sensitivity 99.34%, specificity 86.27%, precision 94.41%.

**Training error vs testing error.** As a model gets more complex (a deeper tree, say), its error on the **training** data keeps falling. Its error on **test** data falls at first, then rises again.

- **Underfitting** is when both errors are high: the model is too simple to capture the pattern.
- **Overfitting** is when the training error is low but the test error is high: the model has memorised noise.

The sweet spot is where the test error is lowest. That's why accuracy is always measured on data the model never trained on.

**Accuracy evaluation methods**, which decide how the data gets split for testing:

| Method | How | Note |
| --- | --- | --- |
| Holdout | Randomly split, usually 2/3 for training and 1/3 for testing | Simple, but the estimate depends on one lucky or unlucky split |
| Random subsampling | Repeat holdout k times, and average the accuracies | Smooths out the luck |
| k-fold cross-validation | Split into k equal folds. Each fold is the test set once while the other k − 1 train. Average the k results | Every tuple is tested exactly once. k = 10 is standard. Leave-one-out uses k = n |
| Bootstrap | Sample n tuples **with replacement** for training, and test on the tuples never picked | About 63.2% of the tuples get picked, since 1 − (1 − 1/n)ⁿ → 1 − e⁻¹ |

The .632 bootstrap combines both sets:

```latex
\text{Acc}(M) = \frac{1}{k}\sum_{i=1}^{k}\left(0.632 \times \text{Acc}_{\text{test}_i} + 0.368 \times \text{Acc}_{\text{train}_i}\right)
```

**Stratified cross-validation:** the folds are formed so each one has roughly the **same class proportions** as the whole dataset. If 30% of the data is positive, every fold is about 30% positive. That stops a fold from accidentally getting no positives at all. **Leave-one-out** (k = number of tuples) is for small datasets.

Why is the bootstrap's test set 36.8%? Each of the d draws misses a given tuple with probability 1 − 1/d, so the chance it's never picked is (1 − 1/d)ᵈ ≈ e⁻¹ = 0.368. That leaves about 63.2% in training. The bootstrap works well for **small** datasets.

**ROC curves** (Receiver Operating Characteristic, from signal detection theory) compare classifiers visually. Plot the **true positive rate** (TP/P) on the vertical axis against the **false positive rate** (FP/N) on the horizontal axis.

1. Rank the test tuples by the classifier's predicted probability of being positive, most likely first.
2. Walk down the list. Each actual positive moves the curve **up** by 1/P, and each actual negative moves it **right** by 1/N.
3. The **area under the curve (AUC)** measures accuracy: 1.0 is a perfect model, and 0.5 (the diagonal line) is random guessing. The closer a curve hugs the diagonal, the worse the model.

Example: five test tuples ranked by probability, with actual classes P, P, N, P, N (so P = 3 and N = 2):

| Step | Tuple | Point (FPR, TPR) |
| --- | --- | --- |
| Start |  | (0, 0) |
| 1 | P | (0, 1/3) |
| 2 | P | (0, 2/3) |
| 3 | N | (1/2, 2/3) |
| 4 | P | (1/2, 1) |
| 5 | N | (1, 1) |

```latex
\text{AUC} = \tfrac{1}{2} \times \tfrac{2}{3} + \tfrac{1}{2} \times 1 = 0.833
```

That equals the fraction of (positive, negative) pairs the model ranks the right way round: 5 of 6.

**Is model M1 really better than M2?** Run 10-fold cross-validation on both to get mean error rates. A small difference might be pure chance, so use a **test of statistical significance**, usually a t-test on the per-fold differences, with k − 1 = 9 degrees of freedom, and quote **confidence limits** on the error estimates. Only if the t value exceeds the critical value at the chosen level (say 5%) is the difference real.

## Stop 5C: Ensembles and k-nearest neighbour

An **ensemble** combines many classifiers, so one model's mistakes get outvoted by the others.

|  | Bagging | Boosting (AdaBoost) |
| --- | --- | --- |
| Training sets | k bootstrap samples, drawn independently | Sequential: each round reweights the tuples |
| Focus | Every tuple equally | Tuples the previous models got wrong get higher weights |
| Combining | Equal majority vote | Weighted vote: more accurate models count more |
| Effect | Reduces variance, robust to noise | Reduces bias, usually more accurate, but can overfit noise |
| Example | Random forest is bagging plus random feature choice | AdaBoost |

In AdaBoost, a model's vote weight is log((1 − error) / error), so a model with 10% error gets a much bigger say than one with 40%.

**k-nearest neighbour** is the classic lazy learner. Store all the training tuples. For a new tuple, find the k closest by distance, and take the majority class (or the mean, for prediction). Normalise the attributes first, so a salary in lakhs doesn't drown out an age in years. Choose an odd k to avoid ties.

> **Practice.** Training data: (7, 7) Bad, (7, 4) Bad, (3, 4) Good, (1, 4) Good. Classify (3, 7) with k = 3, using Euclidean distance.

**Answer:** Squared distances from (3, 7):

| Point | Class | Squared distance |
| --- | --- | --- |
| (7, 7) | Bad | 16 + 0 = 16 |
| (7, 4) | Bad | 16 + 9 = 25 |
| (3, 4) | Good | 0 + 9 = 9 |
| (1, 4) | Good | 4 + 9 = 13 |

The 3 nearest are (3, 4) Good, (1, 4) Good and (7, 7) Bad.

**Majority 2 to 1, so (3, 7) is classified Good.**

## Stop 5D: Weakly supervised learning

This is from the Unit 4 slides and wasn't in last year's papers, so expect it as theory ("explain self-training", "what is zero-shot learning"). The common problem: **labels are expensive**. A human has to read every review, look at every X-ray. Weakly supervised learning gets a good classifier from **few, cheap or noisy labels**. The slides list five approaches.

**1. Semi-supervised learning (SSL):** build a classifier from a small **labelled** set plus a large **unlabelled** set.

**Self-training:**

1. Pick a learning method, say Naive Bayes.
2. Train it on the labelled data.
3. Use it to label the unlabelled data.
4. Take the unlabelled tuple it's **most confident** about.
5. Add that tuple, with its predicted label, to the labelled set.
6. Repeat.

**Co-training** uses two classifiers that teach each other:

1. Split the attributes into two **separate, non-overlapping** feature sets.
2. Train classifier f1 on one feature set and f2 on the other, using the labelled data.
3. Let each classify the unlabelled tuples.
4. The tuple f1 is most confident about goes into **f2's** labelled set, and f2's most confident tuple goes into **f1's**.
5. Repeat.

It works because each view catches what the other misses.

**When does SSL work?** It needs one of two assumptions to hold:

- **Cluster assumption:** tuples in the same cluster tend to share a label. Example: **S3VM** (semi-supervised SVM) looks for a maximum-margin hyperplane, like an SVM, that also passes through **low-density** regions of the unlabelled data, so it doesn't cut through a cluster.
- **Manifold assumption:** two tuples that are close together tend to share a label. Example: **graph-based SSL**, which connects nearby tuples and spreads labels along the edges.

**2. Active learning:** the model **asks** an oracle (a human expert) to label only the tuples that would help it most, so every paid label counts. In **pool-based** active learning the model picks from a pool of unlabelled tuples. The key question is which tuples to query:

| Strategy | Query the tuple… |
| --- | --- |
| Uncertainty sampling | the model is least sure about |
| Query-by-committee | on which several models disagree most |
| Version space | that shrinks the set of hypotheses still consistent with the data fastest |
| Decision-theoretic | expected to reduce future error the most |

|  | Semi-supervised | Active learning | Transductive learning |
| --- | --- | --- | --- |
| Uses unlabelled data by | Labelling it automatically | Asking a human to label the best tuples | Labelling exactly the given test tuples |
| Human in the loop | No | Yes | No |
| Goal | A general model | A general model with the fewest labels | Labels for that specific set only |

**3. Transfer learning:** reuse knowledge from one or more **source** tasks on a different **target** task. Example: a sentiment classifier trained on **electronics** reviews is adapted to **movie** reviews.

- **TrAdaBoost** is instance-based transfer: reweight the source data and use it to learn the target task. Like boosting (Stop 5C), each round focuses on the hard examples. The twist is that a **source** tuple the model gets wrong has its weight **reduced**, because it's probably not relevant to the target task.
- **The key challenge is negative transfer**, when using the source makes the target worse. Measuring how different the tasks are (transfer margin, divergence metrics) guards against it.
- **Related ideas:** multi-task learning, and pre-training plus fine-tuning.

**4. Distant supervision:** automatically generate a **large** number of labelled tuples from some outside signal. The labels are **noisy**, but there are lots of them.

- Twitter sentiment: a tweet containing ":-)" counts as positive, and one with ":-(" as negative.
- Twitter topics: a tweet with a URL gets the website's category from the Open Directory Project (ODP); a tweet with a YouTube link gets that video's category.

It's used for social media post classification and for relation extraction in NLP (natural language processing). The main challenge is noisy labels: a ":)" can be sarcastic.

**5. Zero-shot learning:** predict a class that **never appeared in training**. Say a classifier was trained on owl, dog and fish images, and a cat image arrives. The strategy is to use outside knowledge, typically a **semantic attribute classifier**:

1. Train classifiers for descriptive attributes (has fur, has whiskers, four legs) on the training data.
2. Use them to infer the attributes of the new image.
3. Match those attributes to the description of an unseen class, such as "cat: fur, whiskers, four legs".

Applications: image recognition, neural activity recognition, graph anomaly detection. In **generalized** zero-shot learning, a test tuple may come from a known class or a new one.

**Summary: SSL = few labels plus many unlabelled tuples (self-training, co-training). Active learning = ask a human for the most useful labels. Transfer = reuse a source task (TrAdaBoost, beware negative transfer). Distant supervision = many noisy automatic labels. Zero-shot = classes never seen in training, reached through semantic attributes.**

## Stop 6: k-means

Clustering groups similar objects with **no labels given**. Good clusters have high similarity inside and low similarity between them.

**Cluster analysis** (also called clustering or data segmentation) finds similarities in the data and groups similar objects into clusters. It's **unsupervised**: "learning by observation", not "learning by examples" as in classification. Similarity is judged from the attribute values, usually through a **distance** measure.

**Where it's used** (the slides' list): biology (the taxonomy of kingdom, phylum, class … species), information retrieval (grouping documents), land use (finding similar areas in satellite data), marketing (finding customer groups for targeted campaigns), city planning (grouping houses by type, value and location), earthquake studies (epicentres cluster along fault lines), climate (atmospheric and ocean patterns), and economic market research.

**Two roles for clustering:**

- **A stand-alone tool**, to get insight into how the data is distributed.
- **A preprocessing step** for other algorithms:
    - **summarisation** before regression, PCA, classification or association analysis;
    - **compression**, such as vector quantisation in image processing;
    - **speeding up k-nearest neighbour**, by searching only within one or a few clusters;
    - **outlier detection**, since outliers are the points far from every cluster.

**What makes a clustering good:**

- **High intra-class similarity**, meaning the objects inside a cluster are cohesive.
- **Low inter-class similarity**, meaning the clusters are distinct from each other.

The quality depends on the similarity measure, how the method is implemented, and its ability to find the hidden patterns. Judging "similar enough" is often **subjective**, which is why a separate quality function (Stop 9B) is used.

**Considerations when choosing a method** (the slides' four axes):

| Consideration | One option | The other |
| --- | --- | --- |
| Partitioning criteria | Single level | Hierarchical, multi-level (often preferred) |
| Separation of clusters | **Exclusive**: a customer belongs to one region only | **Non-exclusive**: a document can belong to several topics |
| Similarity measure | **Distance-based**: Euclidean, road network, vector | **Connectivity-based**: density or contiguity |
| Clustering space | **Full space**, often for low dimensions | **Subspaces**, for high-dimensional data |

**Features required of a clustering algorithm:** scalability to large data, the ability to handle different attribute types, clusters of arbitrary shape, minimal domain knowledge needed for parameters, robustness to noise and outliers, insensitivity to the order of input, handling high dimensions, constraints, and interpretable results.

**Categories of clustering methods:**

| Category | Idea | Typical methods |
| --- | --- | --- |
| Partitioning | Build k partitions, then improve them against a criterion such as minimum sum of squared errors | k-means, k-medoids (PAM, CLARA), CLARANS |
| Hierarchical | Build a tree of clusters by merging or splitting | AGNES, DIANA, BIRCH, CHAMELEON |
| Density-based | Grow clusters through connected dense regions | DBSCAN, OPTICS, DENCLUE |
| Grid-based | Quantise the space into a multi-level grid of cells | STING, WaveCluster, CLIQUE |
| Model-based | Assume a model for each cluster and find the best fit | EM, SOM (self-organising map), COBWEB |
| Frequent-pattern-based | Cluster from frequent patterns in the data | p-Cluster |
| User-guided or constraint-based | Respect user or application constraints | COD (clustering with obstacles), constrained clustering |
| Link-based | Use the links between objects (web pages, people) | SimRank, LinkClus |

**Data types and dissimilarity measures**, where d(i, j) is the dissimilarity between objects i and j:

| Data type | Dissimilarity |
| --- | --- |
| Interval-scaled (height, weight) | Standardise first, then Euclidean, Manhattan or Minkowski |
| Symmetric binary (gender) | (r + s) / (q + r + s + t) |
| Asymmetric binary (test positive) | (r + s) / (q + r + s), ignoring the 0-0 matches t (the Jaccard distance) |
| Nominal (colour) | (p − m) / p, with m matches out of p attributes |
| Ordinal (bronze, silver, gold) | Replace by rank, map to \[0, 1\] with (r − 1) / (M − 1), then treat as interval |
| Ratio-scaled (growth) | Take logs, then treat as interval |
| Mixed | Weighted average of the per-attribute dissimilarities |

For binary data, q counts the attributes that are 1 for both objects, r those that are 1 for i only, s those that are 1 for j only, and t those that are 0 for both.

```latex
d_{\text{Minkowski}}(i, j) = \left(\sum_f |x_{if} - x_{jf}|^p\right)^{1/p} \qquad (p = 1 \text{ Manhattan},\ p = 2 \text{ Euclidean})
```

> **Practice (the Han and Kamber patient example).** Six asymmetric binary attributes (fever, cough, test1 to test4), with yes and positive as 1. Jack = 1 0 1 0 0 0, Mary = 1 0 1 0 1 0, Jim = 1 1 0 0 0 0. Which pair is most alike?

**Answer:**

```latex
\begin{aligned}
d(\text{Jack}, \text{Mary}) &= \frac{0 + 1}{2 + 0 + 1} = 0.33 \\
d(\text{Jack}, \text{Jim}) &= \frac{1 + 1}{1 + 1 + 1} = 0.67 \\
d(\text{Jim}, \text{Mary}) &= \frac{1 + 2}{1 + 1 + 2} = 0.75
\end{aligned}
```

**Jack and Mary are the most alike (0.33). Jim and Mary are the least alike (0.75).**

**k-means**, the partitioning workhorse:

1. Pick k initial centroids (the question usually gives them).
2. Assign every point to its nearest centroid.
3. Recompute each centroid as the mean of its points.
4. Repeat steps 2 and 3 until no point changes cluster.

```latex
\begin{aligned}
\text{Euclidean: } d(p, q) &= \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2} \\
\text{Manhattan: } d(p, q) &= |x_1 - x_2| + |y_1 - y_2|
\end{aligned}
```

Its weak spots: you must choose k, it's sensitive to the starting centroids and to outliers (the mean gets dragged), and it only finds round, convex clusters.

**What k-means is minimising.** Partitioning methods split n objects into k clusters (k ≤ n) so as to minimise the **sum of squared errors (SSE)**, the total squared distance from each point to its cluster's centre cᵢ:

```latex
E = \sum_{i=1}^{k} \sum_{p \in C_i} \text{dist}(p, c_i)^2
```

Trying every possible partition would find the global optimum but takes forever, so k-means and k-medoids are **heuristics**. k-means (MacQueen 1967, Lloyd 1957/1982) represents each cluster by its **mean**, and k-medoids (PAM, Kaufman and Rousseeuw 1987) by **one of its actual objects**.

**k-means, the slides' verdict:**

- **Strength: efficient.** It runs in O(tkn) time, where n is the number of objects, k the number of clusters and t the number of iterations, and normally k, t ≪ n. Compare PAM at O(k(n − k)²) per iteration and CLARA at O(ks² + k(n − k)), where s is the sample size.
- **It often stops at a local optimum**, so different starting centroids can give different answers.
- **Weaknesses:** it works only where a mean makes sense (continuous data), needs k in advance, is sensitive to noise and outliers, and can't find non-convex shapes.

**Variations:** k-means variants differ in how the initial k means are chosen, how dissimilarity is computed, and how means are calculated.

- **k-modes** handles **categorical** data. It replaces means with **modes** (the most frequent value), uses a dissimilarity suited to categories, and updates modes by frequency.
- **k-prototype** handles a **mix** of categorical and numerical data.

> **The slides' worked example.** Cluster A1(2, 10), A2(2, 5), A3(8, 4), A4(5, 8), A5(7, 5), A6(6, 4), A7(1, 2), A8(4, 9) into three clusters. The initial centres are A1(2, 10), A4(5, 8) and A7(1, 2). Use **Manhattan** distance, ρ(a, b) = \|x₂ − x₁\| + \|y₂ − y₁\|. Find the three cluster centres after the second iteration.

**Answer:** These are the same points as the Endsem 2025 question below, but with Manhattan distance instead of Euclidean.

**Iteration 1**, centres C1(2, 10), C2(5, 8), C3(1, 2). For example, A1 to C2 is \|5 − 2\| + \|8 − 10\| = 3 + 2 = 5.

| Point | to C1 | to C2 | to C3 | Cluster |
| --- | --- | --- | --- | --- |
| A1(2, 10) | 0 | 5 | 9 | C1 |
| A2(2, 5) | 5 | 6 | 4 | C3 |
| A3(8, 4) | 12 | 7 | 9 | C2 |
| A4(5, 8) | 5 | 0 | 10 | C2 |
| A5(7, 5) | 10 | 5 | 9 | C2 |
| A6(6, 4) | 10 | 5 | 7 | C2 |
| A7(1, 2) | 9 | 10 | 0 | C3 |
| A8(4, 9) | 3 | 2 | 10 | C2 |

```latex
\begin{aligned}
C_1 &= (2, 10) \text{ (only A1)} \\
C_2 &= \left(\tfrac{8 + 5 + 7 + 6 + 4}{5}, \tfrac{4 + 8 + 5 + 4 + 9}{5}\right) = (6, 6) \\
C_3 &= \left(\tfrac{2 + 1}{2}, \tfrac{5 + 2}{2}\right) = (1.5, 3.5)
\end{aligned}
```

**Iteration 2**, centres C1(2, 10), C2(6, 6), C3(1.5, 3.5):

| Point | to C1 | to C2 | to C3 | Cluster |
| --- | --- | --- | --- | --- |
| A1 | 0 | 8 | 7 | C1 |
| A2 | 5 | 5 | 2 | C3 |
| A3 | 12 | 4 | 7 | C2 |
| A4 | 5 | 3 | 8 | C2 |
| A5 | 10 | 2 | 7 | C2 |
| A6 | 10 | 2 | 5 | C2 |
| A7 | 9 | 9 | 2 | C3 |
| A8 | 3 | 5 | 8 | **C1** (moved) |

```latex
\begin{aligned}
C_1 &= \left(\tfrac{2 + 4}{2}, \tfrac{10 + 9}{2}\right) = (3, 9.5) \\
C_2 &= \left(\tfrac{8 + 5 + 7 + 6}{4}, \tfrac{4 + 8 + 5 + 4}{4}\right) = (6.5, 5.25) \\
C_3 &= (1.5, 3.5)
\end{aligned}
```

**After the second iteration the centres are C1(3, 9.5), C2(6.5, 5.25) and C3(1.5, 3.5).** If a question asks you to run it to convergence: in iteration 3, A4 moves to C1, giving {A1, A4, A8}, {A3, A5, A6}, {A2, A7}. Iteration 4 changes nothing, so it stops with centres (3.67, 9), (7, 4.33) and (1.5, 3.5). The same final grouping as the Euclidean version below.

> **PYQ, Endsem 2025 Q5(a), 4.5 marks.** Cluster A1(2, 10), A2(2, 5), A3(8, 4), B1(5, 8), B2(7, 5), B3(6, 4), C1(1, 2), C2(4, 9) into three clusters with Euclidean distance. The initial centres are A1, B1 and C1. Use k-means, showing every round until the solution is reached.

**Answer:**

**Round 1**, with centres c1 = (2, 10), c2 = (5, 8), c3 = (1, 2):

| Point | to c1 | to c2 | to c3 | Cluster |
| --- | --- | --- | --- | --- |
| A1 | 0 | 3.61 | 8.06 | 1 |
| A2 | 5.00 | 4.24 | 3.16 | 3 |
| A3 | 8.49 | 5.00 | 7.28 | 2 |
| B1 | 3.61 | 0 | 7.21 | 2 |
| B2 | 7.07 | 3.61 | 6.71 | 2 |
| B3 | 7.21 | 4.12 | 5.39 | 2 |
| C1 | 8.06 | 7.21 | 0 | 3 |
| C2 | 2.24 | 1.41 | 7.62 | 2 |

The clusters are {A1}, {A3, B1, B2, B3, C2} and {A2, C1}. The new centres are the means:

```latex
c_1 = (2, 10), \quad c_2 = \left(\tfrac{8+5+7+6+4}{5}, \tfrac{4+8+5+4+9}{5}\right) = (6, 6), \quad c_3 = (1.5, 3.5)
```

**Round 2**, with centres (2, 10), (6, 6), (1.5, 3.5): C2 is now 2.24 from c1 against 3.61 from c2, so it moves to cluster 1. Everything else stays.

The clusters are {A1, C2}, {A3, B1, B2, B3} and {A2, C1}, with new centres (3, 9.5), (6.5, 5.25) and (1.5, 3.5).

**Round 3:** B1 is now 2.50 from c1 against 3.13 from c2, so it moves to cluster 1.

The clusters are {A1, B1, C2}, {A3, B2, B3} and {A2, C1}, with new centres (3.67, 9), (7, 4.33) and (1.5, 3.5).

**Round 4:** every point keeps its cluster, so the algorithm stops.

**Final clusters: {A1, B1, C2}, {A3, B2, B3}, {A2, C1}, with centroids (3.67, 9), (7, 4.33) and (1.5, 3.5). It converges in 4 rounds.**

> **PYQ, Data Analytics Sessional-2 2025 Q4, 5 marks.** Points P1 to P12: (185, 72), (170, 56), (168, 60), (179, 68), (182, 72), (188, 77), (180, 71), (180, 70), (183, 84), (180, 88), (180, 67), (177, 76). Starting centroids (185, 72) and (170, 56). Use k-means with Manhattan distance and show the clusters after 2 rounds.

**Answer:**

**Round 1**, with c1 = (185, 72) and c2 = (170, 56):

| Point | to c1 | to c2 | Cluster |
| --- | --- | --- | --- |
| P1 (185, 72) | 0 | 31 | 1 |
| P2 (170, 56) | 31 | 0 | 2 |
| P3 (168, 60) | 29 | 6 | 2 |
| P4 (179, 68) | 10 | 21 | 1 |
| P5 (182, 72) | 3 | 28 | 1 |
| P6 (188, 77) | 8 | 39 | 1 |
| P7 (180, 71) | 6 | 25 | 1 |
| P8 (180, 70) | 7 | 24 | 1 |
| P9 (183, 84) | 14 | 41 | 1 |
| P10 (180, 88) | 21 | 42 | 1 |
| P11 (180, 67) | 10 | 21 | 1 |
| P12 (177, 76) | 12 | 27 | 1 |

```latex
\begin{aligned}
c_1 &= \left(\tfrac{1814}{10}, \tfrac{745}{10}\right) = (181.4, 74.5) \\
c_2 &= \left(\tfrac{170 + 168}{2}, \tfrac{56 + 60}{2}\right) = (169, 58)
\end{aligned}
```

**Round 2:** every point is still nearer its old centroid. For example, P4 is 8.9 from c1 against 20 from c2, and P3 is 27.9 against 3. No point moves.

**After 2 rounds: Cluster 1 = {P1, P4, P5, P6, P7, P8, P9, P10, P11, P12}, centroid (181.4, 74.5). Cluster 2 = {P2, P3}, centroid (169, 58).**

## Stop 7: k-medoids (PAM)

k-medoids uses an **actual data point**, the medoid, as each cluster's centre instead of a mean. One outlier can drag a mean far away, but it can't move a medoid much, so k-medoids is **robust to outliers**. The price is speed.

**PAM** (Partitioning Around Medoids):

1. Pick k points as the initial medoids.
2. Assign every point to its nearest medoid, and add up the total cost (the sum of distances).
3. Try swapping a medoid with a non-medoid. Keep the swap only if the total cost drops.
4. Repeat until no swap helps.

> **PYQ, Data Analytics Sessional-2 2025 Q2, 3 marks.** Points P1 = (2, 6, 4), P2 = (3, 4, 7), P3 = (8, 1, 2), P4 = (7, 2, 3), P5 = (6, 5, 8), P6 = (4, 7, 6). Picking the initial medoids P1, P3 and P5, show the final clusters formed.

**Answer:** Use Manhattan distance, the usual choice for PAM, and say so.

| Point | to P1 | to P3 | to P5 | Nearest |
| --- | --- | --- | --- | --- |
| P1 | 0 | 13 | 9 | P1 |
| P2 | 6 | 13 | 5 | P5 |
| P3 | 13 | 0 | 12 | P3 |
| P4 | 10 | 3 | 9 | P3 |
| P5 | 9 | 12 | 0 | P5 |
| P6 | 5 | 14 | 6 | P1 |

```latex
\text{Total cost} = 0 + 5 + 0 + 3 + 0 + 5 = 13
```

Now test swaps. For example, swapping P5 for P2 gives exactly the same groups, at the same cost of 13, and swapping P3 for P4 also costs 13. No swap brings the cost below 13 (a brute-force check of every medoid triple confirms 13 is the minimum), so PAM stops.

**Final clusters: {P1, P6}, {P3, P4}, {P2, P5}, with total cost 13.** Euclidean distance gives the same three clusters, so either assumption gets full marks.

**From the slides: why medoids, and what PAM's swap looks like.** An object with an extremely large value drags a cluster's **mean** far away, distorting everything. A **medoid** is the most centrally located actual object in a cluster, so one extreme value barely moves it.

The slides draw PAM with k = 2. With the current medoids, the total cost (the sum of each point's distance to its medoid) is **20**. Swapping one medoid with a randomly chosen non-medoid (the slides call it O\_random) gives a cost of **26**. That's worse, so the swap is rejected. A swap is kept only if it lowers the cost, and PAM loops until no swap helps.

**PAM's problem is scale.** Each iteration tries k(n − k) swaps, each needing a pass over the n − k other points, so it costs O(k(n − k)²) per iteration. That's fine for small datasets and hopeless for large ones. Two fixes:

| Method | Idea | Cost |
| --- | --- | --- |
| **CLARA** (Clustering LARge Applications, Kaufman and Rousseeuw 1990) | Run PAM on several **random samples** and keep the best medoids found | O(ks² + k(n − k)), with s the sample size |
| **CLARANS** (Clustering Large Applications based on RANdomized Search, Ng and Han 1994) | Don't try every swap. Try **random** swaps, move whenever one improves the cost, restart a few times | Better quality than CLARA without sampling the data away |

**k-medoids = robust to outliers, but slow; CLARA samples, CLARANS randomises the search.**

## Stop 8: Hierarchical clustering

**Agglomerative** (bottom-up, AGNES): start with every point as its own cluster, and repeatedly merge the two closest clusters until one is left. **Divisive** (top-down, DIANA) does the reverse. The result is a **dendrogram**, a tree whose merge heights are the merge distances. You don't need to choose k in advance: cut the tree at any height.

| Linkage | Distance between clusters | Tends to give |
| --- | --- | --- |
| Single | The closest pair of points (min) | Long, chained clusters |
| Complete | The farthest pair (max) | Compact clusters |
| Average | The mean of all pairs | Somewhere in between |

**The single-link recipe:** merge the smallest entry in the matrix, then update the new cluster's distance to each other cluster as the **minimum** of the old two. Repeat.

**Divisive (DIANA)** runs the other way. Start with every object in one cluster. Split the cluster with the largest diameter: the object with the highest average dissimilarity to the others starts a splinter group, and objects closer to the splinter group than to the rest move across. Repeat until every object is alone. It's rarer in practice, because there are 2ⁿ⁻¹ − 1 ways to split n objects in two, so it relies on heuristics.

**Merges and splits can't be undone**, in both directions. That's the main weakness of hierarchical clustering. A bad early merge stays forever.

**Strengths of hierarchical clustering** (from the slides):

- You don't have to assume a number of clusters. Any number can be had by **cutting** the dendrogram at the right level.
- The tree may correspond to a meaningful **taxonomy**, like the animal kingdom or a phylogeny (an evolutionary tree).

**The basic agglomerative algorithm:**

1. Compute the **proximity matrix**, the distance between every pair of points.
2. Let each data point be its own cluster.
3. Repeat:
4. merge the two closest clusters, and
5. update the proximity matrix,
6. until only one cluster remains.

The key operation is step 5: how to measure the distance between two **clusters**. The different answers are what distinguish the algorithms:

| Inter-cluster distance | Definition | Strength | Limitation |
| --- | --- | --- | --- |
| **MIN** (single link) | The two **closest** points in different clusters | Handles non-elliptical (odd-shaped) clusters | Sensitive to noise and outliers: one bridging point chains clusters together |
| **MAX** (complete link) | The two **farthest** points | Less susceptible to noise | Tends to break up large clusters; biased towards round (globular) ones |
| **Group average** | The average of all cross-cluster pairs | A compromise; less susceptible to noise | Biased towards globular clusters |
| **Centroid distance** | The distance between the two cluster centres | Simple | Can behave oddly: a merge can end up closer than the previous one |
| **Ward's method** | The increase in total squared error (SSE) caused by the merge | Same objective as k-means, so good for initialising k-means | Biased towards globular clusters |

```latex
\text{proximity}(C_i, C_j) = \frac{\sum_{p_i \in C_i} \sum_{p_j \in C_j} \text{proximity}(p_i, p_j)}{|C_i| \times |C_j|} \qquad (\text{group average})
```

> **The slides' worked example (from Tan, Steinbach and Kumar).** Six points with this distance matrix. Cluster them with MIN, MAX and group average.

|  | p1 | p2 | p3 | p4 | p5 | p6 |
| --- | --- | --- | --- | --- | --- | --- |
| p1 | 0 | 0.24 | 0.22 | 0.37 | 0.34 | 0.23 |
| p2 | 0.24 | 0 | 0.15 | 0.20 | 0.14 | 0.25 |
| p3 | 0.22 | 0.15 | 0 | 0.15 | 0.28 | 0.11 |
| p4 | 0.37 | 0.20 | 0.15 | 0 | 0.29 | 0.22 |
| p5 | 0.34 | 0.14 | 0.28 | 0.29 | 0 | 0.39 |
| p6 | 0.23 | 0.25 | 0.11 | 0.22 | 0.39 | 0 |

**Answer:** The first two merges are the same for all three, because between single points every linkage is just the matrix entry: {3, 6} at 0.11, then {2, 5} at 0.14. After that they differ:

| Step | MIN (single) | MAX (complete) | Group average |
| --- | --- | --- | --- |
| 3 | {3, 6} + 4 at 0.15 | {3, 6} + 4 at 0.22 | {3, 6} + 4 at 0.185 |
| 4 | {2, 5} + {3, 4, 6} at 0.15 | {2, 5} + 1 at 0.34 | {2, 5} + {3, 4, 6} at 0.26 |
| 5 | + 1 at 0.22 | {1, 2, 5} + {3, 4, 6} at 0.39 | + 1 at 0.28 |

How some of those numbers come about:

- **MIN, step 3:** min(d(3, 4), d(6, 4)) = min(0.15, 0.22) = 0.15. Step 4 ties at 0.15 too, since d(2, 3) = 0.15.
- **MAX, step 4:** the candidates are {3, 4, 6} to 1 = max(0.22, 0.37, 0.23) = 0.37, {3, 4, 6} to {2, 5} = 0.39, and {2, 5} to 1 = max(0.24, 0.34) = 0.34. The smallest is 0.34.
- **Average, step 4:** {3, 4, 6} to {2, 5} = (0.15 + 0.28 + 0.25 + 0.39 + 0.20 + 0.29) / 6 = 0.26, beating {3, 4, 6} to 1 = (0.22 + 0.37 + 0.23) / 3 = 0.273 and {2, 5} to 1 = (0.24 + 0.34) / 2 = 0.29.

**MIN joins p1 last at 0.22; MAX pairs p1 with {2, 5} and only joins the two big groups at 0.39; group average sits in between (final merge at 0.28).** The slides' dendrograms show exactly these merge orders.

> **PYQ, Endsem 2025 Q5(c), 4.5 marks.** Explain any one algorithm of hierarchical clustering. For objects A to E with the distance matrix below, what dendrogram does single-link hierarchical clustering return?

|  | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| A | 0 | 9 | 2 | 3 | 1 |
| B |  | 0 | 8 | 6 | 5 |
| C |  |  | 0 | 7 | 10 |
| D |  |  |  | 0 | 4 |
| E |  |  |  |  | 0 |

**Answer:** Explain agglomerative single-link using the recipe above, then run it.

| Step | Smallest distance | Merge | Updated distances |
| --- | --- | --- | --- |
| 1 | A–E = 1 | {A, E} | to B: min(9, 5) = 5; to C: min(2, 10) = 2; to D: min(3, 4) = 3 |
| 2 | AE–C = 2 | {A, E, C} | to B: min(5, 8) = 5; to D: min(3, 7) = 3 |
| 3 | AEC–D = 3 | {A, E, C, D} | to B: min(5, 6) = 5 |
| 4 | AECD–B = 5 | {A, B, C, D, E} | done |

```
height
  5  |   ________________________
     |  |                        |
  3  |  |___________             |
     |  |           |            |
  2  |  |_______    |            |
     |  |       |   |            |
  1  |  |___    |   |            |
     |  |   |   |   |            |
     |  A   E   C   D            B
```

**The dendrogram merges A and E at 1, adds C at 2, D at 3, and B at 5.** B joins last, so it's the natural outlier.

> **PYQ, Data Analytics Sessional-2 2025 Q3, 3 marks.** Use single-link agglomerative clustering on the matrix below and show the dendrogram. Can a dendrogram tell you the best number of clusters?

|  | A | B | C | D |
| --- | --- | --- | --- | --- |
| A | 0 | 1 | 4 | 5 |
| B |  | 0 | 2 | 6 |
| C |  |  | 0 | 3 |
| D |  |  |  | 0 |

**Answer:**

| Step | Merge | At distance | Updated |
| --- | --- | --- | --- |
| 1 | {A, B} | 1 | to C: min(4, 2) = 2; to D: min(5, 6) = 5 |
| 2 | {A, B, C} | 2 | to D: min(5, 3) = 3 |
| 3 | {A, B, C, D} | 3 | done |

```
  3  |   ______________
  2  |   _________     |
  1  |   ____     |    |
     |   A  B     C    D
```

**Merges: A + B at 1, then C at 2, then D at 3.** Yes, a dendrogram suggests the number of clusters: cut across the **longest vertical gap**, where no merges happen for the biggest stretch of distance, and count the branches you cross. Here the gaps are all equal (1 each), so this data shows no strong natural grouping, which is itself a fair answer.

## Stop 9: DBSCAN, outliers and high dimensions

**DBSCAN** (density-based clustering) grows clusters through dense regions. It needs two parameters: **ε** (the neighbourhood radius) and **MinPts**.

| Point type | Rule |
| --- | --- |
| Core | Has at least MinPts points within ε, itself included |
| Border | Within ε of a core point, but not core itself |
| Noise | Neither: no core point reaches it |

A cluster is a maximal set of **density-connected** points: start from any core point, add everything within ε, and keep expanding through the core points you reach. It finds the number of clusters by itself.

**The DBSCAN algorithm, as the slides write it:**

1. Label every point as core, border or noise. (Density means the number of points within Eps, and a point **counts itself**.)
2. Throw away the noise points.
3. Put an edge between every pair of core points within Eps of each other.
4. Each group of connected core points becomes a separate cluster.
5. Assign each border point to the cluster of one of its core points.

**When DBSCAN works well:** it handles clusters of **different shapes and sizes**, and it's **resistant to noise**. The slides show letter-shaped clusters with Eps = 10 and MinPts = 4.

**When it doesn't:**

- **Varying densities.** A single Eps can't suit a dense cluster and a sparse one at the same time. The slides show Eps = 9.92 and Eps = 9.75 (MinPts = 4) giving very different results on the same data.
- **High-dimensional data**, where density loses meaning (see the curse of dimensionality below).

**Choosing Eps and MinPts: the k-distance plot.**

1. For every point, find the distance to its **k-th nearest neighbour**, with k = MinPts (often 4).
2. Sort these distances and plot them.
3. Points inside clusters have close k-th neighbours, so the curve stays low and flat. Noise points have far k-th neighbours, so the curve shoots up at the end.
4. Set **Eps at the knee**, where the sharp rise starts. Everything beyond it is noise.

> **PYQ, Endsem 2025 Q5(b)(i); Data Analytics Sessional-2 2025 Q1, 4 marks.** Why can DBSCAN (and OPTICS) find clusters of arbitrary shape, when partition-based algorithms fail to?

**Answer:** k-means assigns every point to its nearest centroid, so the boundary between two clusters is always the straight line halfway between their centres. That makes every cluster a convex, roughly spherical blob around its centre. A ring or a crescent gets chopped into pieces.

DBSCAN has no centre at all. It follows **density**, chaining from core point to core point, so a cluster can snake along any path the dense region takes, however curved. OPTICS orders points by reachability distance, so it handles clusters of varying density too.

**Partitioning measures distance to a centre, which forces convex shapes. Density-based methods follow connected dense regions, whatever their shape.**

> **PYQ, Data Analytics Sessional-2 2025 Q4(a).** How can DBSCAN be used to detect outliers?

**Answer:** DBSCAN labels every point that isn't core and isn't reachable from a core point as **noise**. Those noise points are exactly the outliers: they sit in sparse regions that no dense cluster reaches. Unlike k-means, outliers can't distort the clusters, because they never join one.

**DBSCAN's noise points are the outliers, found for free as a by-product of clustering.**

> **PYQ, Endsem 2025 Q5(b)(ii).** How does the curse of dimensionality affect distance-based clustering algorithms?

**Answer:** As the number of dimensions grows:

- **Distances concentrate.** The nearest and the farthest neighbour end up almost equally far away, so "closest" loses its meaning.
- **Data becomes sparse.** The volume grows exponentially, so any fixed number of points thins out, and density-based notions like ε-neighbourhoods stop working.
- **Irrelevant features add noise** to every distance, hiding the real structure.

The fixes are dimensionality reduction (PCA, feature selection) or subspace clustering such as CLIQUE.

**In high dimensions all points look roughly equally far apart, so distance-based clustering loses its ability to tell similar from dissimilar.**

## Stop 9B: Cluster validity

The last big topic in the Unit 5 slides. For classification we have accuracy, precision and recall. **How do we judge whether clusters are any good?** "Clusters are in the eye of the beholder", yet we still need to check, for four reasons:

- to avoid finding patterns in **noise**: the slides show k-means, DBSCAN and complete link all happily "finding" clusters in uniformly random points;
- to compare clustering algorithms;
- to compare two sets of clusters;
- to compare two clusters.

**Two kinds of measures:**

|  | Supervised (**external** index) | Unsupervised (**internal** index) |
| --- | --- | --- |
| Measures | How well the cluster labels match externally supplied class labels | How good the structure is, using only the data itself |
| Example | Entropy of the true classes inside each cluster | Sum of squared errors (SSE) |

**Cohesion and separation**, the two internal ideas:

- **Cohesion:** how closely related the objects in a cluster are. It's measured by the within-cluster sum of squares, the **SSE**. Smaller is better.
- **Separation:** how distinct a cluster is from the others. It's measured by the between-cluster sum of squares, the **SSB**, where \|Cᵢ\| is the size of cluster i, mᵢ its mean and m the overall mean. Bigger is better.

```latex
SSE = \sum_i \sum_{x \in C_i} (x - m_i)^2, \qquad SSB = \sum_i |C_i|\,(m - m_i)^2
```

> **The slides' example.** Points 1, 2, 4 and 5 on a line, so the overall mean is m = 3. Compute SSE and SSB for K = 1 cluster, and for K = 2 clusters, {1, 2} and {4, 5}.

**Answer:**

```latex
\begin{aligned}
K = 1: \quad SSE &= (1-3)^2 + (2-3)^2 + (4-3)^2 + (5-3)^2 = 10, \quad SSB = 4 \times (3-3)^2 = 0, \quad \text{Total} = 10 \\
K = 2: \quad SSE &= (1-1.5)^2 + (2-1.5)^2 + (4-4.5)^2 + (5-4.5)^2 = 1 \\
SSB &= 2 \times (3-1.5)^2 + 2 \times (4.5-3)^2 = 9, \quad \text{Total} = 1 + 9 = 10
\end{aligned}
```

**SSE + SSB stays constant (10): a better clustering moves error out of SSE (cohesion) into SSB (separation).**

The slides also give a **graph** version: cohesion is the sum of the edge weights **within** a cluster, and separation is the sum of the edge weights from the cluster to nodes **outside** it.

**The silhouette coefficient** combines cohesion and separation for each **point**. For a point i:

1. a = the average distance from i to the other points in its own cluster (cohesion).
2. b = the smallest, over all the other clusters, of the average distance from i to that cluster's points (separation).
3. s = (b − a) / max(a, b).

s ranges from −1 to 1, and is typically between 0 and 1. **Closer to 1 is better.** Averaging s over a cluster or a whole clustering scores those too.

Example with the same four points and clusters {1, 2} and {4, 5}:

| Point | a | b | s |
| --- | --- | --- | --- |
| 1 | 1 | (3 + 4) / 2 = 3.5 | 2.5 / 3.5 = 0.714 |
| 2 | 1 | (2 + 3) / 2 = 2.5 | 1.5 / 2.5 = 0.600 |
| 4 | 1 | 2.5 | 0.600 |
| 5 | 1 | 3.5 | 0.714 |

```latex
\bar{s} = \frac{0.714 + 0.600 + 0.600 + 0.714}{4} = 0.657
```

**Average silhouette 0.66: a reasonably good clustering.**

**Validity through correlation.** Build two n × n matrices:

- the **proximity matrix** of the points;
- an **ideal similarity matrix**, where the entry is 1 if the two points are in the same cluster and 0 if not.

Then compute the correlation between them. Both are symmetric, so only n(n − 1)/2 entries are needed. A high-magnitude correlation means points in the same cluster really are close. The sign is negative if the proximity matrix holds distances rather than similarities. It's not a good measure for density- or contiguity-based clusters.

**Is a validity value significant?** A number like SSE = 10 means nothing alone. Statistics gives the framework: compute the same index on **random data**, and if your value is very unlikely under randomness (the more "atypical" it is), the clusters reflect real structure. The slides end with Jain and Dubes' warning that validating clusters is "the most difficult and frustrating part of cluster analysis".

**Validity = external (match known labels, e.g. entropy) or internal (SSE for cohesion, SSB for separation, silhouette s = (b − a)/max(a, b) per point, correlation with the ideal similarity matrix), judged against random data.**

## Stop 10: Web mining and text mining

The last line of Unit 5, and usually worth a short theory answer.

**Web mining** discovers patterns from the web, and splits three ways:

| Type | Mines | Example |
| --- | --- | --- |
| Web content mining | The text, images and data on pages | Classifying pages by topic, extracting product prices |
| Web structure mining | The hyperlink graph | PageRank, finding hubs and authorities (HITS) |
| Web usage mining | Server logs and clickstreams | Recommending pages, improving site layout |

**Text mining** finds patterns in unstructured text. The pipeline: tokenise, remove stop words, stem ("mining" and "mined" become "mine"), then represent each document as a term vector, usually weighted by **TF-IDF**, so that words frequent in one document but rare overall score highest.

```latex
\text{TF-IDF}(t, d) = \text{tf}(t, d) \times \log\frac{N}{\text{df}(t)}
```

Then apply the usual tools: classification (spam filtering), clustering (grouping news stories), and association (words that co-occur). Documents are compared with cosine similarity.

**Web mining is content, structure or usage. Text mining turns documents into TF-IDF vectors, then classifies, clusters or associates them.**

That's the run. Refill the tea, and give the cat a pat for being a perfectly clustered point of one.
