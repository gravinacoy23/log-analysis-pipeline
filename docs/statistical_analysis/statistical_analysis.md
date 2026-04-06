# Statistical Analysis Report — Month 4

## Overview

This report documents the exploratory data analysis (EDA) performed
on the log analysis pipeline dataset during Month 4. The goal is to
understand the data before modeling it in Phase 3 — distributions,
correlations, class balance, and evaluation metrics.

All analysis uses two data sources:

- **Raw DataFrame** from `run_pipeline` — contains original metrics
  (cpu, mem, response_time, level, service)
- **Feature dataset** from `output/datasets/features.csv` — contains
  derived features (is_error, is_slow, hour_of_day, service_encoded,
  cpu_mem_ratio)

---

## Distribution Analysis

### Response Time

The response time distribution is skewed toward higher values. This
is expected and directly traceable to the generator's design.

Response time is determined by an OR condition: if **either** CPU
or memory exceeds the configured "normal" threshold, response time
is generated in the high range (801–1200ms). Since CPU and memory
are independent random variables, the probability that **at least
one** exceeds the threshold is higher than the probability that any
single metric exceeds it alone. This produces more high-RT logs
than the original design where only CPU influenced response time.

### CPU

With a small dataset (~600 logs), the CPU distribution appeared
irregular with unexpected peaks at the edges and center. After
generating a larger dataset (~16,000 logs), the distribution
converged to a **uniform distribution** — consistent with the
generator using `random.randint(30, 70)`.

This illustrates the **law of large numbers**: with small samples,
randomness produces noise; with large samples, the underlying
distribution becomes visible.

**Range:** 30–70 (config-driven)

### Memory

Findings are identical to CPU. Memory is generated with the same
mechanism (`random.randint(40, 75)`) and produces a uniform
distribution at scale.

**Range:** 40–75 (config-driven)

---

## Cross-Service Comparison

Descriptive statistics (mean, median, std, percentiles) were
computed for each service independently by running the pipeline
for booking, shopping, and pricing separately.

**Finding:** The statistics are practically identical across all
three services. This is expected — the generator uses the same
ranges and logic for all services. Service-specific instability
is not yet implemented (tracked in tech debt).

---

## Correlation Analysis

### Raw DataFrame

The correlation heatmap confirms the correlations designed into
the generator:

- **CPU ↔ response_time:** moderate positive correlation — when
  CPU increases, response time tends to increase
- **Memory ↔ response_time:** moderate positive correlation —
  same relationship as CPU
- **User ↔ everything:** no correlation — user ID is randomly
  generated and does not influence any other metric

### Feature Dataset

Correlations between derived features are consistent with how
they were constructed from the raw metrics. No unexpected
correlations were found.

### Correlation vs Causation

The CPU → response_time correlation exists in the data, and in a
real system this would represent genuine causation — CPU saturation
impedes request processing and increases response time.

However, in this project the correlation exists because the
generator explicitly programs it: `if cpu > threshold: return
random.randint(801, 1200)`. There is no real server, no real
processing, no physical mechanism. The correlation is real in the
data, but the causation is the generator's design — not system
physics. This distinction matters because in real-world data
analysis, finding a correlation does not prove that one variable
causes the other.

---

## Train / Test Split

The feature dataset was split using `sklearn.model_selection.train_test_split`:

- **Split ratio:** 80% train, 20% test
- **Stratification:** on `is_error` to preserve class distribution
- **Reproducibility:** `random_state=42` for deterministic splits

### Class Distribution

`is_error = True` represents approximately 20% of the dataset.
This imbalance is expected — the generator only produces ERROR
level for response times >= 900ms, which requires either CPU or
memory to exceed the "normal" threshold.

Stratification ensures both train and test sets maintain this
same ~20% proportion.

**Output files:** `training_data.csv` and `test_data.csv` in
`output/datasets/`

---

## Bias vs Variance

- **Underfitting (high bias):** a model too simple to capture
  patterns. Performs poorly on both training and test data.
  Example: a model that always predicts `is_error = False`
  regardless of input.

- **Overfitting (high variance):** a model that memorizes
  training data including noise. Performs well on training data
  but poorly on unseen data. The model learns specifics instead
  of generalizable patterns.

- **The tradeoff:** increasing complexity reduces bias but
  increases variance. The goal is a model that generalizes —
  performing well on data it has never seen.

---

## Evaluation Metrics

### Why Accuracy Is Misleading

A model that always predicts `is_error = False` achieves ~80%
accuracy on this dataset — because ~80% of rows are indeed not
errors. This is the **accuracy trap**: a high accuracy number
that reflects class distribution, not model quality.

**Baseline accuracy:** ~80% (always predict False). Any useful
model must exceed this baseline on meaningful metrics.

### Precision, Recall, and F1

- **Precision** = TP / (TP + FP) — "of all rows I flagged as
  errors, how many were actually errors?"
- **Recall** = TP / (TP + FN) — "of all real errors, how many
  did I catch?"
- **F1** = 2 × (precision × recall) / (precision + recall) —
  harmonic mean that balances both metrics

For an airline backend error detection system, **recall is
prioritized** over precision. Missing a real error (false
negative) is worse than a false alarm (false positive) — the
same principle that drives alerting in incident management.

### Simulated Model Comparison

Two models were evaluated on the training set using a manually
implemented confusion matrix:

#### Model 1 — Always Predict False ("Dumb Model")

| Metric | Value |
|--------|-------|
| TP | 0 |
| TN | 445 |
| FP | 0 |
| FN | 126 |
| Accuracy | ~78% |
| Precision | 0 |
| Recall | 0 |
| F1 | 0 |

Despite ~78% accuracy, this model is completely useless for error
detection. It never identifies a single error. Precision, recall,
and F1 are all zero — the accuracy number is meaningless.

#### Model 2 — Predict Error When is_slow = True

| Metric | Value |
|--------|-------|
| TP | 126 |
| TN | 257 |
| FP | 188 |
| FN | 0 |
| Accuracy | ~67% |
| Precision | 0.40 |
| Recall | 1.00 |
| F1 | 0.57 |

This model has **lower accuracy** than the dumb model (67% vs 78%)
but is vastly more useful. It catches every single error (recall =
1.00) at the cost of many false alarms (precision = 0.40).

**Why recall = 1.00?** The generator guarantees that every ERROR
log has response_time >= 900ms, which exceeds the is_slow threshold
of 800ms. Therefore `is_slow = True` is a superset of
`is_error = True` — every error is slow, but not every slow
response is an error.

**Why precision = 0.40?** Many slow responses (response_time >=
800ms) have WARNING level, not ERROR. The model flags all of them
as errors, producing false positives.

### Conclusion

The comparison demonstrates that accuracy alone is an unreliable
metric for imbalanced classification. A model with lower accuracy
can be significantly more useful than one with higher accuracy,
depending on what matters for the use case. For error detection
in production systems, catching all errors (high recall) is more
valuable than avoiding false alarms (high precision).
