# DM Unit 1: Introduction to Data Mining and Data Preprocessing

*Endsem RUN · about 70 minutes*

**The whole unit in one breath:** data mining digs useful patterns out of huge data, as one step of a bigger process (**KDD**); but real data is dirty, so most of the work is **preprocessing**: cleaning, integrating, transforming and reducing it before mining.

**What the endsem asks from here:** the 2025 paper took **6 of its 15 parts** from this unit: architecture (twice), preprocessing steps, distance measures, curse of dimensionality / overfitting, PCA, and star vs snowflake schema. This is the biggest unit for marks, so give it time.

---

## 1. What data mining is, and KDD · Quick

Imagine Flipkart's database: billions of orders. Nobody can read it. **Data mining** is the automated search for **interesting, non-obvious, useful patterns** in such data, like "people who buy phones buy covers within 3 days".

**Exam line:** *Data mining is the process of discovering interesting patterns and knowledge from large amounts of data, using methods from statistics, machine learning and database systems. It is the core step of Knowledge Discovery in Databases (KDD).*

**KDD steps** (Han & Kamber):

1. **Data cleaning:** remove noise and inconsistencies.
2. **Data integration:** combine multiple sources.
3. **Data selection:** pick the data relevant to the task.
4. **Data transformation:** convert into forms good for mining (normalise, aggregate).
5. **Data mining:** apply intelligent methods to extract patterns.
6. **Pattern evaluation:** keep only the truly interesting patterns.
7. **Knowledge presentation:** show results with visualisation and reports.

Steps 1–4 are **preprocessing**: in practice, most of a data scientist's time goes there.

---

## 2. Architecture of a data mining system · Slow down

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

---

## 3. Data mining functionalities · Quick

What kinds of patterns can be mined:

| Functionality | Question it answers | Example |
| --- | --- | --- |
| **Characterisation** | What's typical of this class? | Profile of customers spending > ₹10k/month |
| **Discrimination** | How does class A differ from class B? | Frequent vs rare buyers |
| **Association / correlation** | What occurs together? | {bread} → {butter} |
| **Classification** | Which class does a new item belong to? (labels known) | Spam / not spam |
| **Prediction (regression)** | What numeric value? | House price |
| **Clustering** | What natural groups exist? (no labels) | Customer segments |
| **Outlier analysis** | What's abnormal? | Card fraud |
| **Evolution / trend analysis** | How does it change over time? | Stock trends |

Techniques overview: statistics, machine learning (supervised and unsupervised), database systems and data warehouses, visualisation, information retrieval.

---

## 4. Describing data: central tendency and dispersion · Quick

**Central tendency** = the "middle" of the data:

- **Mean** $\bar{x} = \frac{1}{n}\sum x_i$ (sensitive to outliers); **weighted mean**; **trimmed mean** (drop extremes first).
- **Median:** the middle value of the sorted data (robust to outliers).
- **Mode:** the most frequent value. Data can be unimodal, bimodal, multimodal.
- **Midrange** = (min + max) / 2.

**Dispersion** = how spread out:

- **Range** = max − min. **Quartiles** Q1 (25th percentile), Q3 (75th); **IQR** = Q3 − Q1.
- **Five-number summary:** min, Q1, median, Q3, max, drawn as a **boxplot**. Outliers are usually values beyond $Q3 + 1.5\,\text{IQR}$ or below $Q1 - 1.5\,\text{IQR}$.
- **Variance and standard deviation:** $\sigma^2 = \frac{1}{n}\sum (x_i - \bar{x})^2$.

**Visualising summaries:** boxplots, histograms, quantile plots, Q-Q plots, scatter plots (relationships between two attributes).

---

## 5. Why preprocess, and the steps · Slow down

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

---

## 6. Distance measures · Slow down

Many methods (k-NN, clustering) need "how different are two objects?". For numeric objects $x = (x_1 \dots x_n)$, $y = (y_1 \dots y_n)$:

| Measure | Formula | Intuition |
| --- | --- | --- |
| **Euclidean** | $\sqrt{\sum (x_i - y_i)^2}$ | Straight-line ("as the crow flies") |
| **Manhattan (city block)** | $\sum \lvert x_i - y_i \rvert$ | Walking along a grid of streets |
| **Minkowski** | $\left(\sum \lvert x_i - y_i \rvert^h\right)^{1/h}$ | h = 1 Manhattan, h = 2 Euclidean |
| **Supremum (Chebyshev)** | $\max_i \lvert x_i - y_i \rvert$ | h → ∞: the single biggest difference |

For nominal attributes: dissimilarity = (attributes that don't match) / (total attributes). For binary: simple matching or Jaccard (ignores 0–0 matches).

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

---

## 7. Curse of dimensionality, overfitting, underfitting · Quick

> **Endsem 2025 · Q2(a)(ii) · 2.5 marks**
> Define (a) Curse of Dimensionality, (b) Underfitting and Overfitting.

**Answer.**

**(a) Curse of dimensionality:** the set of problems that appear as the number of attributes (dimensions) grows. The volume of the space grows exponentially, so a fixed amount of data becomes extremely **sparse**; the **distances between points become almost equal** (nearest and farthest neighbours look alike), so distance-based methods (k-NN, clustering) lose meaning; and the data needed to cover the space, and the computation, grow exponentially. Example: 10 points fill a 1-D line of 10 cells; covering a 10-D grid with 10 cells per side needs $10^{10}$ cells. Remedies: feature selection, PCA.

**(b) Underfitting:** the model is **too simple** to capture the real pattern, so it performs badly on **both** training and test data (high bias). Like a student who only learnt the chapter titles. Example: fitting a straight line to clearly curved data.

**Overfitting:** the model is **too complex** and learns the **noise** of the training data along with the pattern, so it does very well on training data but **badly on new data** (high variance). Like a student who memorised last year's answers word for word and fails on a twisted question. Example: a decision tree grown until every leaf has one record. Remedies: pruning, cross-validation, more data, regularisation.

**Curse of dimensionality: high dimensions make data sparse and distances meaningless. Underfitting: too simple, bad everywhere. Overfitting: memorises the training noise, bad on new data.**

---

## 8. PCA · Slow down

**Principal Component Analysis** finds new axes (**principal components**) along which the data varies the most, so a few components can replace many correlated attributes. Picture a cloud of points shaped like a rugby ball in 3-D: PC1 runs along the long axis, PC2 across the next widest direction, and you can often drop the thin third one.

**Steps:**

1. Centre the data: subtract each attribute's mean.
2. Compute the **covariance matrix** C.
3. Find the **eigenvalues** λ and **eigenvectors** of C (solve $\det(C - \lambda I) = 0$).
4. Sort by eigenvalue: the eigenvector with the largest λ is **PC1**, next is **PC2** … λ is the variance captured.
5. Project the centred data onto the top k eigenvectors.

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

---

## 9. Data warehouse schemas: star vs snowflake · Quick

A **data warehouse** is a subject-oriented, integrated, time-variant, non-volatile store of data for analysis. It's modelled with a central **fact table** (numeric measures like sales amount, plus foreign keys) surrounded by **dimension tables** (descriptions: time, product, store).

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

---

## 10. Quick recap

- KDD: clean → integrate → select → transform → **mine** → evaluate → present.
- Architecture: sources → DB/warehouse server → engine + knowledge base → pattern evaluation → GUI.
- Functionalities: characterisation, discrimination, association, classification, prediction, clustering, outliers, evolution.
- Preprocessing: cleaning (missing, noise via binning), integration (redundancy via correlation), transformation (min-max, z-score, decimal scaling), reduction (PCA, feature selection, sampling).
- Euclidean √Σd², Manhattan Σ|d|, Minkowski, supremum.
- Curse of dimensionality: sparse data, equal-looking distances. Overfitting memorises noise; underfitting is too simple.
- PCA: centre → covariance → eigenvalues/vectors → keep the top components.
- Star (denormalised, fast, redundant) vs snowflake (normalised, compact, more joins).
