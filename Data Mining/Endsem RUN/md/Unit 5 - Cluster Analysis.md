# DM Unit 5: Cluster Analysis

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** clustering groups similar objects together **without any labels**: points in a cluster should be close to each other and far from other clusters. The methods differ in how they define "cluster": around a centre (**k-means**, **k-medoids**), by merging step by step (**hierarchical**), or by dense regions (**DBSCAN**).

**What the endsem asks from here:** a k-means trace (every year), a hierarchical dendrogram from a distance matrix, and DBSCAN / high-dimension theory. 2025's whole Q5.

---

## 1. What clustering is · Quick

**Exam line:** *Cluster analysis is the process of partitioning a set of data objects into groups (clusters) so that objects within a cluster are highly similar to one another and dissimilar to objects in other clusters. It is unsupervised learning: no class labels are given.*

Uses: customer segmentation, grouping documents by topic, image segmentation, finding outliers (points that fit no cluster).

**Features required of a good clustering algorithm:** scalability; handles different attribute types; finds clusters of **arbitrary shape**; needs little domain knowledge for its parameters; deals with **noise and outliers**; insensitive to the order of input; handles **high dimensionality**; supports user constraints; interpretable results.

**Data types and dissimilarity:** numeric (Euclidean, Manhattan, Minkowski, after normalisation), binary (simple matching for symmetric, **Jaccard** for asymmetric), nominal (proportion of mismatches), ordinal (map ranks to [0, 1], then treat as numeric), mixed types (weighted combination). Usually stored as a **dissimilarity matrix** d(i, j).

**Categories of methods:**

| Category | Idea | Examples |
| --- | --- | --- |
| Partitioning | Split into k groups, improve iteratively | k-means, k-medoids (PAM) |
| Hierarchical | Build a tree of merges or splits | AGNES (agglomerative), DIANA (divisive) |
| Density-based | Clusters are dense regions | DBSCAN, OPTICS |
| Grid-based | Quantise space into cells | STING, CLIQUE |
| Model-based | Fit a statistical model | EM, Gaussian mixtures |

---

## 2. k-means · Slow down

**Algorithm:**

1. Choose k initial **centroids** (given, or random).
2. **Assign** every point to its **nearest** centroid.
3. **Update** each centroid to the **mean** of the points assigned to it.
4. Repeat 2–3 until no point changes cluster (centroids stop moving).

It minimises the **sum of squared errors** $SSE = \sum_{i}\sum_{x \in C_i} \text{dist}(x, c_i)^2$.

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

---

## 3. k-medoids (PAM) · Quick

Fixes k-means' outlier problem: instead of the mean (which can be an imaginary point dragged by outliers), each cluster is represented by a **medoid**, an actual object that is most central.

**PAM (Partitioning Around Medoids):** pick k medoids; assign each object to the nearest medoid; then for each medoid m and non-medoid o, compute the change in total cost if they're **swapped**; if any swap reduces the total cost, do it; repeat until no swap helps.

Robust to outliers and noise, but expensive: $O(k(n-k)^2)$ per iteration. **CLARA** (runs PAM on samples) and **CLARANS** (randomised search) scale it up.

---

## 4. Hierarchical clustering · Slow down

Builds a **tree of clusters** (a **dendrogram**). Cut the tree at any height to get that many clusters, so k needn't be chosen in advance.

- **Agglomerative (bottom-up, AGNES):** start with every point as its own cluster; repeatedly **merge the two closest clusters** until one remains.
- **Divisive (top-down, DIANA):** start with one big cluster; repeatedly **split** the most spread-out cluster until each point is alone.

**Distance between clusters** (the "linkage"):

| Linkage | Distance between clusters A and B |
| --- | --- |
| **Single** (nearest neighbour) | **Minimum** distance between any two points: $\min_{a,b} d(a, b)$. Tends to make long "chains" |
| **Complete** (farthest neighbour) | **Maximum** distance: $\max_{a,b} d(a, b)$. Compact clusters |
| **Average** | Average of all pairwise distances |
| **Centroid** | Distance between the means |

**Drawback:** a merge or split can never be undone; $O(n^2)$ memory for the matrix.

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

---

## 5. DBSCAN and high dimensions · Slow down

**DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) defines clusters as **dense regions** separated by sparse ones. Two parameters: **ε (Eps)**, the neighbourhood radius, and **MinPts**, the minimum points needed for density.

- **Core point:** has ≥ MinPts points within ε.
- **Border point:** fewer than MinPts neighbours, but lies within ε of a core point.
- **Noise (outlier):** neither.
- **Directly density-reachable:** q is within ε of core point p. **Density-reachable:** a chain of such steps. **Density-connected:** both reachable from a common core point.

**Algorithm:** pick an unvisited point; if it's a core point, start a cluster and **expand** it by adding everything density-reachable from it; if not, mark it noise for now (it may later turn out to be a border point). Repeat until all points are visited.

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

---

## 6. Cluster validity · Quick

How good is a clustering?

- **Internal measures** (no labels): cohesion (SSE within clusters, small is good), separation (distance between clusters, large is good), **silhouette coefficient** $s = \frac{b - a}{\max(a, b)}$ where a = mean distance to own cluster, b = mean distance to the nearest other cluster (near 1 good, near 0 on the boundary, negative wrong).
- **External measures** (compare with known labels): purity, entropy, Rand index.
- **Choosing k:** the **elbow method** (plot SSE against k and look for the bend), or silhouette.

---

## 7. Web mining and text mining · Quick

**Web mining** applies data mining to the web:

- **Web content mining:** the content of pages (text, images): topic classification, opinion mining.
- **Web structure mining:** the hyperlink graph: **PageRank**, **HITS** (hubs and authorities), community detection.
- **Web usage mining:** server logs and clickstreams: navigation patterns, recommendations, personalisation.

**Text mining** extracts patterns from unstructured text: tokenisation, stop-word removal, stemming; represent documents as vectors (**bag of words**, **TF-IDF** weights: a term's frequency in a document times the log of its inverse document frequency); then cluster or classify them using **cosine similarity**. Uses: spam filtering, sentiment analysis, document clustering, information retrieval.

---

## 8. Quick recap

- Clustering = unsupervised grouping; high intra-cluster similarity, low inter-cluster similarity.
- Methods: partitioning, hierarchical, density, grid, model-based.
- k-means: assign to nearest centroid → recompute means → repeat; sensitive to outliers and initial centres; spherical clusters.
- k-medoids (PAM): actual objects as centres, swap to reduce cost; robust, slower.
- Agglomerative: merge closest clusters; single = min, complete = max, average linkage; dendrogram.
- DBSCAN: ε, MinPts; core/border/noise; arbitrary shapes, finds noise, no k.
- High dimensions: distances concentrate, data sparse; use PCA, feature selection, subspace clustering.
- Validity: SSE, silhouette, elbow method. Web mining: content, structure, usage. Text: TF-IDF + cosine.
