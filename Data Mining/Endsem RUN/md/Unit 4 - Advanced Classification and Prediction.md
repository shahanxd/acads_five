# DM Unit 4: Advanced Classification, Evaluation and Prediction

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** better classifiers (**Bayesian belief networks**, **SVM**, **k-NN**, **ensembles** like bagging and boosting), how to **measure** how good a classifier is (confusion matrix, sensitivity, precision…), how to **test** it fairly (holdout, cross-validation, bootstrap), and **regression** for predicting numbers.

**What the endsem asks from here:** theory with a dash of numbers: accuracy measures from a confusion matrix, evaluation methods, bagging vs boosting, k-NN, regression, and SVM. 2025 asked linear SVM with its pros and cons (Q4(c)).

---

## 1. Bayesian belief networks · Quick

Naive Bayes assumes all attributes are independent given the class, which is often false (smoking and lung cancer are clearly linked). A **Bayesian belief network (BBN)** models the dependencies explicitly.

**Exam line:** *A Bayesian belief network is a directed acyclic graph (DAG) whose nodes are random variables and whose arcs show probabilistic dependence, together with a conditional probability table (CPT) for each node giving its probability given each combination of its parents' values.*

Example: FamilyHistory → LungCancer ← Smoker; LungCancer → PositiveXRay, Dyspnea. Each variable is conditionally independent of its non-descendants given its parents, so:

```latex
P(x_1, \dots, x_n) = \prod_{i=1}^{n} P(x_i \mid \text{Parents}(x_i))
```

BBNs handle dependent attributes and missing data, and can be trained from data (learning CPTs, or even the structure). Downside: building the network needs expertise and inference can be expensive.

---

## 2. Support Vector Machines · Slow down

Imagine red and blue dots on a table and you have to lay a stick between them. Many positions separate them, but the **best** one is in the middle of the widest possible empty "street" between the two colours. That's an SVM.

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

---

## 3. Measuring a classifier: the confusion matrix · Slow down

For two classes (positive = the class we care about, e.g. "has cancer"):

| | Predicted positive | Predicted negative |
| --- | --- | --- |
| **Actual positive** | TP (true positive) | FN (false negative) |
| **Actual negative** | FP (false positive) | TN (true negative) |

| Measure | Formula | Asks |
| --- | --- | --- |
| **Accuracy** (recognition rate) | $\frac{TP + TN}{\text{all}}$ | How often is it right overall? |
| **Error rate** | $1 - \text{accuracy}$ | |
| **Sensitivity** (recall, true positive rate) | $\frac{TP}{TP + FN}$ | Of the real positives, how many did we catch? |
| **Specificity** (true negative rate) | $\frac{TN}{TN + FP}$ | Of the real negatives, how many did we correctly clear? |
| **Precision** | $\frac{TP}{TP + FP}$ | Of the ones we called positive, how many really were? |
| **F1 score** | $\frac{2PR}{P + R}$ | Balance of precision and recall |

**Example (cancer screening, 10,000 patients):** TP = 90, FN = 210, FP = 140, TN = 9,560.

```latex
\begin{aligned}
\text{Accuracy} &= \frac{90 + 9560}{10000} = 96.5\% \\
\text{Sensitivity} &= \frac{90}{90 + 210} = 30\% \\
\text{Specificity} &= \frac{9560}{9560 + 140} = 98.6\% \\
\text{Precision} &= \frac{90}{90 + 140} = 39.1\%
\end{aligned}
```

96.5% accuracy sounds great, but the model catches only **30%** of cancer cases. With **imbalanced classes**, accuracy misleads; use sensitivity, specificity, precision and F1. (A model saying "no cancer" for everyone would score 97% accuracy!)

---

## 4. Predictor error measures · Quick

For numeric prediction, with actual $y_i$ and predicted $\hat{y}_i$ over n test records:

| Measure | Formula |
| --- | --- |
| Mean absolute error (MAE) | $\frac{1}{n}\sum \lvert y_i - \hat{y}_i \rvert$ |
| Mean squared error (MSE) | $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$ (punishes big errors) |
| Root mean squared error (RMSE) | $\sqrt{\text{MSE}}$ (same units as y) |
| Relative absolute error | $\frac{\sum \lvert y_i - \hat{y}_i \rvert}{\sum \lvert y_i - \bar{y} \rvert}$ |
| Relative squared error | $\frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ |

The relative versions compare the model with simply predicting the mean $\bar{y}$.

---

## 5. Accuracy evaluation methods · Slow down

You must test on data the model **hasn't seen**, or you're grading a student on the exact questions they practised.

| Method | How | Notes |
| --- | --- | --- |
| **Holdout** | Randomly split once: typically 2/3 training, 1/3 testing | Simple; result depends on the one split |
| **Random subsampling** | Repeat holdout k times; average the accuracies | Less dependent on one split |
| **k-fold cross-validation** | Split into k equal folds; each fold is the test set once while the other k − 1 train; average over k runs | k = 10 is standard; every record is tested exactly once. **Stratified** CV keeps class proportions in each fold. **Leave-one-out** = k is the number of records |
| **Bootstrap** | Sample n records **with replacement** for training; the never-picked records form the test set | Good for small datasets. **.632 bootstrap**: on average 63.2% of distinct records land in training, since a record is missed with probability $(1 - 1/n)^n \approx e^{-1} = 0.368$. Accuracy $= \frac{1}{k}\sum (0.632\,\text{Acc}_{test} + 0.368\,\text{Acc}_{train})$ |

Also: **ROC curves** plot true positive rate vs false positive rate as the threshold varies; the **area under the curve (AUC)** compares models (1 = perfect, 0.5 = random guessing).

---

## 6. Ensembles: bagging and boosting · Slow down

An **ensemble** combines many classifiers, like asking several doctors instead of one. Each may be mediocre, but their combined vote is better.

**Bagging (bootstrap aggregating):**

1. Make k training sets by **bootstrap sampling** (with replacement) from the data.
2. Train one classifier on each, **independently** (in parallel).
3. Classify a new record by **majority vote** (or average, for prediction).

Reduces **variance**, so it helps unstable models like decision trees; robust to noise. **Random forest** = bagging of decision trees, plus a random subset of attributes considered at each split.

**Boosting (e.g. AdaBoost):**

1. Give every training record an equal **weight**.
2. Train a classifier; **increase the weights of the records it misclassified** and decrease the others.
3. Train the next classifier on the reweighted data, so it **focuses on the hard cases**; repeat k times, **sequentially**.
4. Final prediction = **weighted vote**, where each classifier's vote is weighted by its accuracy ($\alpha_i = \log\frac{1 - \text{err}_i}{\text{err}_i}$).

| | Bagging | Boosting |
| --- | --- | --- |
| Training | Parallel, independent | Sequential, each fixes the previous one's mistakes |
| Sampling | Bootstrap, equal weights | Reweighted by errors |
| Voting | Equal votes | Weighted by accuracy |
| Mainly reduces | Variance | Bias (and variance) |
| Risk | Little overfitting | Can overfit noisy data / outliers |

---

## 7. Lazy learners: k-nearest neighbour · Quick

**Eager learners** (decision trees, SVM) build a model in advance. **Lazy learners** just **store** the training data and do the work at classification time.

**k-NN algorithm:** to classify a new record, compute its distance (usually Euclidean, after **normalising** the attributes) to every training record, take the **k nearest**, and assign the **majority class** among them (for prediction: average their values).

Example: k = 3; a new student's three nearest neighbours are labelled Pass, Pass, Fail → predict **Pass**.

**Choosing k:** small k is sensitive to noise; large k blurs class boundaries; choose by cross-validation, odd k for two classes to avoid ties. **Pros:** simple, no training time, handles complex boundaries. **Cons:** slow at prediction (distance to every record), needs normalisation, suffers from the curse of dimensionality and irrelevant attributes. (Another lazy learner: **case-based reasoning**.)

---

## 8. Prediction: linear and non-linear regression · Quick

**Linear regression** models $y = w_0 + w_1 x$ and fits it by **least squares** (minimising the sum of squared errors):

```latex
w_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}, \qquad w_0 = \bar{y} - w_1\bar{x}
```

**Example** (years of experience x vs salary y in ₹ thousands): x = 3, 8, 9, 13, 3, 6, 11, 21, 1, 16; y = 30, 57, 64, 72, 36, 43, 59, 90, 20, 83. Means: $\bar{x} = 9.1$, $\bar{y} = 55.4$.

```latex
w_1 = 3.54, \qquad w_0 = 55.4 - 3.54 \times 9.1 = 23.2 \qquad\Rightarrow\qquad \hat{y} = 23.2 + 3.54\,x
```

Predicted salary at 10 years: 23.2 + 35.4 ≈ **58.6 thousand**.

**Multiple linear regression:** $y = w_0 + w_1x_1 + w_2x_2 + \dots$.

**Non-linear regression:** if the relationship curves, e.g. polynomial $y = w_0 + w_1x + w_2x^2 + w_3x^3$, **transform** it into a linear one by defining new variables $x_1 = x, x_2 = x^2, x_3 = x^3$, then solve by least squares. Other models: log-linear, generalised linear models (logistic regression for probabilities of a class), regression trees.

---

## 9. Quick recap

- BBN: DAG + CPTs; joint probability = product of P(node | parents).
- SVM: maximise margin 2/‖w‖ subject to $y_i(\mathbf{w}\cdot\mathbf{x}_i + b) \ge 1$; support vectors; soft margin C; kernels.
- Accuracy (TP+TN)/all; sensitivity TP/(TP+FN); specificity TN/(TN+FP); precision TP/(TP+FP).
- Error measures: MAE, MSE, RMSE, relative errors.
- Holdout, random subsampling, k-fold CV (k = 10), bootstrap (.632).
- Bagging: bootstrap + equal vote (variance ↓). Boosting: reweight errors + weighted vote (bias ↓).
- k-NN: lazy, k nearest by distance, majority vote; normalise; choose k by CV.
- Least squares: $w_1 = \frac{\sum(x-\bar x)(y-\bar y)}{\sum(x-\bar x)^2}$, $w_0 = \bar y - w_1\bar x$.
