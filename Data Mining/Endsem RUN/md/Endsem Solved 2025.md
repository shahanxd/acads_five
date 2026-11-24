# Data Mining Endsem 2025, Solved

**Paper:** B.Tech (CE) Sem V, Introduction to Data Mining (CSE-501), 3 hours, 45 marks. Attempt any two parts from each question; every part is 4.5 marks. All 15 parts are solved here; every numerical was checked by computer.

Every question of the 2025 endsem paper, solved. The same answers sit inside the unit docs at the topic they belong to; the unit is named under each question so you can jump there for the explanation.

---

## Question 1

> **Endsem 2025 · Q1(a) · 4.5 marks**
> Describe in detail the architecture of data mining. Also discuss the different types of data on which data mining can be applied.

**Answer.**

A typical data mining system has these layered components:

```
              +------------------------------+
              |   Graphical User Interface   |   <- user queries, results
              +------------------------------+
              |   Pattern Evaluation Module  |   <- keeps interesting patterns
              +------------------------------+
              |     Data Mining Engine       |<-->  Knowledge Base
              +------------------------------+     (concept hierarchies,
              | Database / Data Warehouse    |      beliefs, thresholds)
              |          Server              |
              +------------------------------+
                 ^ cleaning, integration, selection
   [Database] [Data warehouse] [World Wide Web] [Other repositories]
```

1. **Data sources (repositories):** databases, data warehouses, the web, spreadsheets, other information repositories. Data cleaning, integration and selection happen on the way in.
2. **Database or data warehouse server:** fetches the relevant data in response to the user's mining request.
3. **Knowledge base:** domain knowledge that guides the search and judges patterns: concept hierarchies (city → state → country), user beliefs, interestingness thresholds such as minimum support and confidence, metadata.
4. **Data mining engine:** the core: modules for characterisation, association, classification, prediction, clustering, outlier analysis and evolution analysis.
5. **Pattern evaluation module:** uses interestingness measures (support, confidence, accuracy, novelty) to filter the patterns, often working with the engine to focus the search.
6. **Graphical user interface:** lets the user specify the task and constraints, browse the data, and see results in visual form.

**Types of data that can be mined:**

| Data type | What it is | Example of mining |
| --- | --- | --- |
| **Relational databases** | Tables of tuples | Find customers likely to churn |
| **Data warehouses** | Integrated, historical, multidimensional data (data cubes) | Sales trends by region and quarter |
| **Transactional data** | Each record is a transaction with a set of items | Market basket analysis |
| **Time-series and sequence data** | Values over time, ordered events | Stock prices, click sequences |
| **Spatial data** | Maps, locations | Hotspots of crime, store placement |
| **Text and multimedia** | Documents, images, audio, video | Spam detection, image search |
| **Web data** | Pages, links, usage logs | PageRank, recommendation |
| **Graphs and networks** | Nodes and edges | Social network communities |
| **Data streams** | Continuous fast-arriving data | Sensor alerts, fraud in card swipes |

**Architecture: data sources → DB/warehouse server → mining engine (with knowledge base) → pattern evaluation → GUI. Data can be relational, warehouse, transactional, time-series, spatial, text/multimedia, web, graph or stream.**

*Taught in Unit 1.*

> **Endsem 2025 · Q1(b) · 4.5 marks**
> As a software engineer at a big university, design a data mining system to examine the university course database, containing each student's name, address and status (undergraduate or graduate), courses taken, and cumulative GPA. Describe the architecture you choose and the purpose of each component.

**Answer.**

Choose a **tightly coupled architecture**: the mining system is integrated with the university's database/data warehouse, so it can use the DBMS's indexing and query processing and store results back. (Coupling options, worst to best: *no coupling* (works on flat files), *loose* (only fetches data from the DB), *semi-tight* (some mining primitives like sorting and aggregation run inside the DB), *tight* (mining is a component of the DB/warehouse system). Tight is most efficient for a large, continuously updated student database.)

Components and their purpose for this university:

1. **Data sources:** the student database (name, address, status), course registration records, and grade records. Cleaning fixes missing GPAs and inconsistent course codes; integration joins students with their courses.
2. **Data warehouse server:** stores integrated history in a **star schema**: a fact table *Enrollment* (student_id, course_id, semester_id, grade) with dimension tables *Student* (name, address, status), *Course*, *Semester*. Lets queries roll up from course → department, or address → city → state.
3. **Knowledge base:** concept hierarchies (course → department → faculty; address → city → state; GPA → grade bands like "excellent ≥ 9"), and thresholds (minimum support and confidence).
4. **Data mining engine** with the modules this task needs:
   - **Characterisation/discrimination:** "graduate students with GPA ≥ 3.5 vs undergraduates: what distinguishes them?"
   - **Association:** "students who took Data Structures and Algorithms also take Data Mining (70% confidence)".
   - **Classification/prediction:** predict GPA band or "at risk of failing" from courses and status.
   - **Clustering:** group students by course choices and performance.
   - **Outlier analysis:** unusual GPA jumps (possible errors or misconduct).
5. **Pattern evaluation:** keeps rules above support/confidence thresholds and drops obvious ones (e.g. "graduate students took graduate courses").
6. **GUI:** lets the academic office ask questions (e.g. "characterise students with GPA > 3.5 from Delhi") and shows charts, rules and reports.

**A tightly coupled system over a university data warehouse (star schema), with a knowledge base of concept hierarchies, an engine for characterisation, association, classification and clustering, pattern evaluation, and a GUI for the academic office.**

*Taught in Unit 1.*

> **Endsem 2025 · Q1(c) · 4.5 marks**
> Why is data preprocessing an essential step in the data mining and machine learning process? Describe the major steps of data preprocessing, with the purpose and common techniques of each.

**Answer.**

**Why:** real-world data is **dirty**:

- **Incomplete:** missing values (a customer skipped the age field).
- **Noisy:** errors and outliers (age = 250).
- **Inconsistent:** different codes or formats (DOB as 03/04/05; "M" vs "Male").
- **Redundant / huge:** duplicates and irrelevant attributes, too big to mine quickly.

"Garbage in, garbage out": mining dirty data gives misleading patterns, and models learn the noise. Preprocessing improves **accuracy, completeness, consistency, timeliness and interpretability**, and makes mining faster.

**The four major steps:**

**1. Data cleaning:** fill missing values, smooth noise, remove outliers, fix inconsistencies.

- *Missing values:* ignore the tuple; fill manually; use a global constant ("Unknown"); fill with the attribute **mean/median**; mean of the **same class**; or the **most probable value** (regression, decision tree, Bayesian inference).
- *Noise:* **binning** (sort, split into bins, smooth by bin means, medians or boundaries), **regression** (fit a function), **clustering** (values outside clusters are outliers).

**2. Data integration:** merge data from several sources into one store.

- Problems: **schema integration / entity identification** (`cust_id` vs `customer_no`), **redundancy** (an attribute derivable from others, like annual income from monthly), **value conflicts** (₹ vs $, kg vs pounds).
- Techniques: metadata, **correlation analysis** to detect redundancy (χ² test for nominal data, correlation coefficient and covariance for numeric data).

**3. Data transformation:** convert data into forms suitable for mining.

- **Smoothing** (remove noise), **aggregation** (daily → monthly sales), **generalisation** (street → city; age → young/middle/senior via concept hierarchies), **attribute construction** (area = length × width), **discretisation**, and **normalisation** (scale to a small range so no attribute dominates):
  - **Min-max:** $v' = \frac{v - \min}{\max - \min}(\text{new\_max} - \text{new\_min}) + \text{new\_min}$
  - **Z-score:** $v' = \frac{v - \bar{x}}{\sigma}$
  - **Decimal scaling:** $v' = v / 10^j$, the smallest j that makes all $|v'| < 1$

**4. Data reduction:** get a much smaller dataset that gives (almost) the same mining results.

- **Dimensionality reduction:** remove attributes: **PCA**, wavelet transforms, **attribute subset (feature) selection** (forward selection, backward elimination, decision-tree induction).
- **Numerosity reduction:** replace data with smaller representations: regression models, histograms, clustering, **sampling**.
- **Data compression** (lossless or lossy); **data cube aggregation**.

**Preprocessing = cleaning (missing values, noise) + integration (schema, redundancy, conflicts) + transformation (smoothing, aggregation, generalisation, normalisation) + reduction (PCA, feature selection, sampling).**

### Worked examples (quick)

**Binning** the sorted prices 4, 8, 15, 21, 21, 24, 25, 28, 34 into 3 equal-frequency bins:

| Bin | Values | By means | By boundaries |
| --- | --- | --- | --- |
| 1 | 4, 8, 15 | 9, 9, 9 | 4, 4, 15 |
| 2 | 21, 21, 24 | 22, 22, 22 | 21, 21, 24 |
| 3 | 25, 28, 34 | 29, 29, 29 | 25, 25, 34 |

(By boundaries: each value is replaced by the nearer of its bin's min and max.)

**Normalising income = 73,600** where min = 12,000, max = 98,000, mean = 54,000, σ = 16,000:

```latex
\begin{aligned}
\text{Min-max to } [0, 1]&: \frac{73600 - 12000}{98000 - 12000} = \frac{61600}{86000} = 0.716 \\
\text{Z-score}&: \frac{73600 - 54000}{16000} = 1.225
\end{aligned}
```

**Correlation coefficient** (Pearson) between numeric A and B:

```latex
r_{A,B} = \frac{\sum (a_i - \bar{A})(b_i - \bar{B})}{n\,\sigma_A \sigma_B}
```

r > 0: positively correlated (one may be redundant); r = 0: no linear correlation; r < 0: negatively correlated. Correlation does not mean causation.

*Taught in Unit 1.*

---

## Question 2

> **Endsem 2025 · Q2(a)(i) · 2 marks**
> Given two objects (22, 1, 42, 10) and (20, 0, 36, 8), compute the Euclidean distance and the Manhattan distance between them.

**Answer.**

Differences: (22 − 20, 1 − 0, 42 − 36, 10 − 8) = (2, 1, 6, 2).

```latex
\begin{aligned}
d_{\text{Euclidean}} &= \sqrt{2^2 + 1^2 + 6^2 + 2^2} = \sqrt{4 + 1 + 36 + 4} = \sqrt{45} = 6.708 \\
d_{\text{Manhattan}} &= |2| + |1| + |6| + |2| = 11
\end{aligned}
```

**Euclidean = 6.71, Manhattan = 11.**

*Taught in Unit 1.*

> **Endsem 2025 · Q2(a)(ii) · 2.5 marks**
> Define (a) Curse of Dimensionality, (b) Underfitting and Overfitting.

**Answer.**

**(a) Curse of dimensionality:** the set of problems that appear as the number of attributes (dimensions) grows. The volume of the space grows exponentially, so a fixed amount of data becomes extremely **sparse**; the **distances between points become almost equal** (nearest and farthest neighbours look alike), so distance-based methods (k-NN, clustering) lose meaning; and the data needed to cover the space, and the computation, grow exponentially. Example: 10 points fill a 1-D line of 10 cells; covering a 10-D grid with 10 cells per side needs $10^{10}$ cells. Remedies: feature selection, PCA.

**(b) Underfitting:** the model is **too simple** to capture the real pattern, so it performs badly on **both** training and test data (high bias). Like a student who only learnt the chapter titles. Example: fitting a straight line to clearly curved data.

**Overfitting:** the model is **too complex** and learns the **noise** of the training data along with the pattern, so it does very well on training data but **badly on new data** (high variance). Like a student who memorised last year's answers word for word and fails on a twisted question. Example: a decision tree grown until every leaf has one record. Remedies: pruning, cross-validation, more data, regularisation.

**Curse of dimensionality: high dimensions make data sparse and distances meaningless. Underfitting: too simple, bad everywhere. Overfitting: memorises the training noise, bad on new data.**

*Taught in Unit 1.*

> **Endsem 2025 · Q2(b) · 4.5 marks**
> Let the data matrix X be students' scores. Find two principal components from: Student 1 (Math 90, DSA 60, DM 90), 2 (90, 90, 30), 3 (60, 60, 60), 4 (60, 60, 90), 5 (30, 30, 30).

**Answer.**

**Step 1: means.** Math = 330/5 = 66, DSA = 300/5 = 60, DM = 300/5 = 60. Centred data:

| Student | Math − 66 | DSA − 60 | DM − 60 |
| --- | --- | --- | --- |
| 1 | 24 | 0 | 30 |
| 2 | 24 | 30 | −30 |
| 3 | −6 | 0 | 0 |
| 4 | −6 | 0 | 30 |
| 5 | −36 | −30 | −30 |

**Step 2: covariance matrix** (sample, divide by n − 1 = 4):

```latex
\begin{aligned}
\text{Var(Math)} &= \tfrac{24^2 + 24^2 + 6^2 + 6^2 + 36^2}{4} = \tfrac{2520}{4} = 630 \\
\text{Cov(Math, DSA)} &= \tfrac{0 + 720 + 0 + 0 + 1080}{4} = 450, \quad \text{Cov(Math, DM)} = \tfrac{720 - 720 + 0 - 180 + 1080}{4} = 225 \\
\text{Var(DSA)} &= \tfrac{900 + 900}{4} = 450, \quad \text{Cov(DSA, DM)} = \tfrac{-900 + 900}{4} = 0, \quad \text{Var(DM)} = \tfrac{3600}{4} = 900 \\
C &= \begin{bmatrix} 630 & 450 & 225 \\ 450 & 450 & 0 \\ 225 & 0 & 900 \end{bmatrix}
\end{aligned}
```

**Step 3: eigenvalues** from $\det(C - \lambda I) = 0$:

```latex
\lambda^3 - 1980\,\lambda^2 + 1{,}002{,}375\,\lambda - 50{,}118{,}750 = 0
\;\Rightarrow\; \lambda_1 = 1137.6,\quad \lambda_2 = 786.4,\quad \lambda_3 = 56.0
```

(Coefficients: trace = 630 + 450 + 900 = 1980; sum of 2×2 principal minors = 81,000 + 516,375 + 405,000 = 1,002,375; det C = 50,118,750. Solve the cubic with a calculator.)

**Step 4: eigenvectors** (solve $(C - \lambda I)v = 0$ and normalise):

```latex
\text{PC1} = \begin{bmatrix} 0.656 \\ 0.429 \\ 0.621 \end{bmatrix} (\lambda_1 = 1137.6), \qquad
\text{PC2} = \begin{bmatrix} -0.386 \\ -0.516 \\ 0.764 \end{bmatrix} (\lambda_2 = 786.4)
```

**Variance explained:** PC1 = 1137.6 / 1980 = **57.5%**, PC2 = 786.4 / 1980 = **39.7%**, together **97.2%**. So two components keep almost all the information; the third (2.8%) can be dropped.

**Interpretation:** PC1 has all positive weights: overall performance (high in everything). PC2 contrasts DM (+) against Math and DSA (−): "strong in DM relative to the core subjects".

**Projected scores** (centred data · [PC1, PC2]): S1 (34.4, 13.7), S2 (10.0, −47.7), S3 (−3.9, 2.3), S4 (14.7, 25.3), S5 (−55.1, 6.5).

**PC1 = (0.656, 0.429, 0.621) and PC2 = (−0.386, −0.516, 0.764), capturing 57.5% and 39.7% of the variance (97.2% together).**

(If you use the population covariance, dividing by n = 5, every eigenvalue is scaled by 4/5 but the eigenvectors and percentages are identical.)

*Taught in Unit 1.*

> **Endsem 2025 · Q2(c) · 4.5 marks**
> A data warehouse can be modelled by a star schema or a snowflake schema. Describe the similarities and differences between the two, and analyse their advantages and disadvantages relative to each other.

**Answer.**

**Star schema:** one central fact table directly connected to **denormalised** dimension tables; the diagram looks like a star.

```
            Time
              |
 Product --- SALES FACT --- Store (store, city, state, country)
              |
           Customer
```

**Snowflake schema:** the same, but dimension tables are **normalised** into further sub-tables (Store → City → State), so the diagram branches like a snowflake.

```
            Time
              |
 Product --- SALES FACT --- Store --- City --- State
    |         |
 Category  Customer
```

**Similarities:** both have a central **fact table** with measures and foreign keys; both use dimension tables; both support OLAP (roll-up, drill-down, slice, dice); both are dimensional models for data warehouses.

| Aspect | Star | Snowflake |
| --- | --- | --- |
| Dimension tables | Denormalised (one table per dimension) | Normalised (split into sub-tables) |
| Redundancy | More (e.g. "Delhi" repeated in every store row) | Less |
| Number of joins in queries | Few (fact + dimension) | More (fact + dimension + sub-tables) |
| Query speed | **Faster** | Slower |
| Storage | More | **Less** |
| Design and understanding | **Simpler** | More complex |
| Maintenance / updates | Updating a repeated value touches many rows | **Easier**: change it in one place |

**Star: simpler and faster to query, at the cost of redundancy and storage. Snowflake: saves space and keeps data consistent, at the cost of more joins and slower queries.** Since dimension tables are small compared to the fact table, the space saving is usually minor, so the **star schema is more popular**. (A **fact constellation** has several fact tables sharing dimensions.)

*Taught in Unit 1.*

---

## Question 3

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

*Taught in Unit 2.*

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

*Taught in Unit 2.*

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

*Taught in Unit 2.*

---

## Question 4

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

*Taught in Unit 3.*

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

*Taught in Unit 3.*

> **Endsem 2025 · Q4(c) · 4.5 marks**
> Explain linear SVM. Discuss the advantages and disadvantages of SVM.

**Answer.**

A **Support Vector Machine** is a supervised classifier that finds the **hyperplane** separating two classes with the **maximum margin**. The **margin** is the distance between the hyperplane and the nearest training points of each class; those nearest points are the **support vectors**, and they alone decide where the hyperplane goes.

**Linear SVM (linearly separable case).** A hyperplane in n dimensions is

```latex
\mathbf{w} \cdot \mathbf{x} + b = 0
```

where **w** is the weight vector (perpendicular to the hyperplane) and b the bias. Points are classified by the sign of $\mathbf{w}\cdot\mathbf{x} + b$. The two margin boundaries are $\mathbf{w}\cdot\mathbf{x} + b = +1$ and $-1$, and the margin width is

```latex
\text{margin} = \frac{2}{\lVert \mathbf{w} \rVert}
```

So maximising the margin means **minimising** $\lVert \mathbf{w} \rVert$:

```latex
\min_{\mathbf{w}, b}\ \tfrac12 \lVert \mathbf{w} \rVert^2 \quad \text{subject to} \quad y_i(\mathbf{w}\cdot\mathbf{x}_i + b) \ge 1 \ \ \text{for all } i, \ \ y_i \in \{+1, -1\}
```

This is a convex quadratic optimisation problem, solved with **Lagrange multipliers** $\alpha_i$; only the support vectors get $\alpha_i > 0$, and $\mathbf{w} = \sum \alpha_i y_i \mathbf{x}_i$.

```
   class -1                     class +1
    o   o      |  :  |        x    x
      o    o   |  :  |   x       x
    o      (o) |  :  | (x)    x
               |  :  |
   w.x+b = -1  w.x+b=0  w.x+b = +1
          <-- margin 2/||w|| -->
   (o) and (x) on the dashed lines are the support vectors
```

**Soft margin:** real data overlaps, so slack variables $\xi_i$ allow some points inside the margin or misclassified, with a penalty C: small C = wider margin, more errors tolerated; large C = narrow margin, fewer training errors.

**Non-linear data:** the **kernel trick** maps the data to a higher-dimensional space where a linear separator exists, without computing that mapping explicitly. Common kernels: polynomial, RBF (Gaussian), sigmoid.

| Advantages | Disadvantages |
| --- | --- |
| Maximum margin gives good **generalisation**, less overfitting | **Slow to train** on very large datasets (quadratic optimisation) |
| Works well in **high-dimensional** spaces (text, genes), even when features outnumber samples | Choosing the **kernel** and parameters (C, γ) is tricky and needs tuning |
| Only support vectors matter: memory-efficient, robust to far-away points | Output isn't a probability; results are **hard to interpret** |
| Kernels handle non-linear boundaries | Basic SVM is **binary**: multiclass needs one-vs-one or one-vs-rest |
| Convex problem: a global optimum, no local minima | Sensitive to noise and overlapping classes; needs feature scaling |

**A linear SVM picks the separating hyperplane w·x + b = 0 with the widest margin 2/‖w‖, defined by the support vectors; it generalises well in high dimensions but is slow on big data and needs careful kernel/parameter choice.**

*Taught in Unit 4.*

---

## Question 5

> **Endsem 2025 · Q5(a) · 4.5 marks**
> Cluster the points A1(2, 10), A2(2, 5), A3(8, 4), B1(5, 8), B2(7, 5), B3(6, 4), C1(1, 2), C2(4, 9) into three clusters with Euclidean distance. Initially A1, B1 and C1 are the cluster centres. Use k-means and show all rounds until the solution.

**Answer.**

**Round 1.** Centres: c1 = (2, 10), c2 = (5, 8), c3 = (1, 2). Distance of each point to each centre:

| Point | to c1 (2, 10) | to c2 (5, 8) | to c3 (1, 2) | Cluster |
| --- | --- | --- | --- | --- |
| A1 (2, 10) | 0 | 3.61 | 8.06 | 1 |
| A2 (2, 5) | 5.00 | 4.24 | **3.16** | 3 |
| A3 (8, 4) | 8.49 | **5.00** | 7.28 | 2 |
| B1 (5, 8) | 3.61 | **0** | 7.21 | 2 |
| B2 (7, 5) | 7.07 | **3.61** | 6.71 | 2 |
| B3 (6, 4) | 7.21 | **4.12** | 5.39 | 2 |
| C1 (1, 2) | 8.06 | 7.21 | **0** | 3 |
| C2 (4, 9) | 2.24 | **1.41** | 7.62 | 2 |

Clusters: C1 = {A1}, C2 = {A3, B1, B2, B3, C2}, C3 = {A2, C1}.

```latex
\begin{aligned}
c_1 &= (2, 10) \\
c_2 &= \left(\tfrac{8+5+7+6+4}{5}, \tfrac{4+8+5+4+9}{5}\right) = (6, 6) \\
c_3 &= \left(\tfrac{2+1}{2}, \tfrac{5+2}{2}\right) = (1.5, 3.5)
\end{aligned}
```

**Round 2.** Centres (2, 10), (6, 6), (1.5, 3.5):

| Point | to c1 | to c2 | to c3 | Cluster |
| --- | --- | --- | --- | --- |
| A1 | **0** | 5.66 | 6.52 | 1 |
| A2 | 5.00 | 4.12 | **1.58** | 3 |
| A3 | 8.49 | **2.83** | 6.52 | 2 |
| B1 | 3.61 | **2.24** | 5.70 | 2 |
| B2 | 7.07 | **1.41** | 5.70 | 2 |
| B3 | 7.21 | **2.00** | 4.53 | 2 |
| C1 | 8.06 | 6.40 | **1.58** | 3 |
| C2 | **2.24** | 3.61 | 6.04 | 1 |

C2 moves to cluster 1. Clusters: {A1, C2}, {A3, B1, B2, B3}, {A2, C1}.

```latex
c_1 = (3, 9.5), \quad c_2 = \left(\tfrac{26}{4}, \tfrac{21}{4}\right) = (6.5, 5.25), \quad c_3 = (1.5, 3.5)
```

**Round 3.** Centres (3, 9.5), (6.5, 5.25), (1.5, 3.5):

| Point | to c1 | to c2 | to c3 | Cluster |
| --- | --- | --- | --- | --- |
| A1 | **1.12** | 6.54 | 6.52 | 1 |
| A2 | 4.61 | 4.51 | **1.58** | 3 |
| A3 | 7.43 | **1.95** | 6.52 | 2 |
| B1 | **2.50** | 3.13 | 5.70 | 1 |
| B2 | 6.02 | **0.56** | 5.70 | 2 |
| B3 | 6.26 | **1.35** | 4.53 | 2 |
| C1 | 7.76 | 6.39 | **1.58** | 3 |
| C2 | **1.12** | 4.51 | 6.04 | 1 |

B1 moves to cluster 1. Clusters: {A1, B1, C2}, {A3, B2, B3}, {A2, C1}.

```latex
c_1 = \left(\tfrac{11}{3}, \tfrac{27}{3}\right) = (3.67, 9), \quad c_2 = \left(\tfrac{21}{3}, \tfrac{13}{3}\right) = (7, 4.33), \quad c_3 = (1.5, 3.5)
```

**Round 4.** Recomputing distances with these centres, every point stays in the same cluster (e.g. B1: 1.67 to c1 vs 4.18 to c2; C2: 0.33 to c1). No change, so the algorithm **converges**.

**Final clusters: {A1, B1, C2} centred at (3.67, 9); {A3, B2, B3} at (7, 4.33); {A2, C1} at (1.5, 3.5). Converged after 3 rounds of changes (checked in round 4).**

**k-means: pros and cons.** Simple, fast ($O(nkt)$), scales well. But k must be given in advance; results depend on the initial centres; sensitive to **outliers** (one far point drags the mean); finds only **spherical, similar-size** clusters; needs numeric data for means.

*Taught in Unit 5.*

> **Endsem 2025 · Q5(b) · 4.5 marks**
> (i) Why can DBSCAN produce clusters of arbitrary shape whereas partition-based algorithms fail to? (ii) How does the curse of dimensionality affect distance-based clustering algorithms?

**Answer.**

**(i)** Partition-based methods like k-means assign each point to the **nearest centre** and represent a cluster by its mean. That implicitly makes every cluster a **convex, roughly spherical** region (the boundary between two clusters is a straight line, the perpendicular bisector of the centres). A crescent, a ring or a long snake-shaped cluster gets chopped into pieces or merged wrongly, and outliers drag the means.

DBSCAN has **no centres**. A cluster grows by **chaining** from core point to core point through **local density** (each step only needs a neighbour within ε). So it follows the data wherever the density continues, around curves, rings and irregular shapes, and stops where density drops. It also labels sparse points as **noise** instead of forcing them into a cluster, and doesn't need k in advance.

```
k-means on two moons:        DBSCAN on two moons:
  1 1 1 1 2 2                  1 1 1 1
 1         2 2                1       1
1    2 2 2   2               1    2 2 2   1 ...
      (cut by a straight         (each moon is one
       line: wrong)               dense chain: right)
```

**(ii)** Distance-based clustering assumes "close" means "similar". In high dimensions:

- **Distances concentrate:** the difference between the nearest and the farthest neighbour shrinks relative to the distances themselves, so **all points look roughly equally far apart**, and the notion of a nearest neighbour or a compact cluster loses meaning.
- **Data becomes sparse:** the volume grows exponentially, so a fixed number of points is spread thin; dense regions (needed by DBSCAN) almost vanish, and choosing ε and MinPts becomes very hard.
- **Irrelevant attributes add noise:** with many attributes, the few that matter are drowned out by the many that don't; clusters may exist only in **subspaces** (a few attributes).
- **Cost rises:** distance computations and index structures (k-d trees) degrade towards brute force.

Remedies: dimensionality reduction (PCA), feature selection, **subspace clustering** (e.g. CLIQUE), and other similarity measures (cosine for text).

**DBSCAN grows clusters through local density chains, so shape doesn't matter, while k-means' nearest-centre rule forces convex blobs. In high dimensions distances become almost equal and data sparse, so distance-based clustering stops being meaningful.**

*Taught in Unit 5.*

> **Endsem 2025 · Q5(c) · 4.5 marks**
> Explain any one algorithm of hierarchical clustering. For objects A, B, C, D, E with the distance matrix below, what dendrogram does single-link hierarchical clustering return?

| | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| A | 0 | 9 | 2 | 3 | 1 |
| B | | 0 | 8 | 6 | 5 |
| C | | | 0 | 7 | 10 |
| D | | | | 0 | 4 |
| E | | | | | 0 |

**Answer.**

**Agglomerative (AGNES) with single link:** start with each object as a cluster; at each step merge the two clusters with the **smallest single-link distance** (the minimum distance between their members), and update the distance matrix: $d(X \cup Y, Z) = \min(d(X, Z), d(Y, Z))$. Repeat until one cluster remains, recording the merge heights.

**Step 1:** the smallest entry is d(A, E) = **1** → merge {A, E} at height 1.

| | AE | B | C | D |
| --- | --- | --- | --- | --- |
| AE | 0 | min(9, 5) = 5 | min(2, 10) = 2 | min(3, 4) = 3 |
| B | | 0 | 8 | 6 |
| C | | | 0 | 7 |
| D | | | | 0 |

**Step 2:** smallest is d(AE, C) = **2** → merge {A, E, C} at height 2.

| | AEC | B | D |
| --- | --- | --- | --- |
| AEC | 0 | min(5, 8) = 5 | min(3, 7) = 3 |
| B | | 0 | 6 |
| D | | | 0 |

**Step 3:** smallest is d(AEC, D) = **3** → merge {A, E, C, D} at height 3.

| | AECD | B |
| --- | --- | --- |
| AECD | 0 | min(5, 6) = 5 |

**Step 4:** merge B at height **5** → one cluster {A, B, C, D, E}.

**Dendrogram:**

```
height
  5 |   ┌───────────────┐
    |   │               │
  3 |   ┌──────────┐    │
    |   │          │    │
  2 |   ┌─────┐    │    │
    |   │     │    │    │
  1 | ┌─┴─┐   │    │    │
    | │   │   │    │    │
  0 | A   E   C    D    B
```

**Merge order: (A, E) at 1 → C at 2 → D at 3 → B at 5.** Cutting below height 5 gives 2 clusters {A, C, D, E} and {B}; below 3 gives {A, C, E}, {D}, {B}. Note the chaining typical of single link: each new object joins the growing group one by one.

*Taught in Unit 5.*

