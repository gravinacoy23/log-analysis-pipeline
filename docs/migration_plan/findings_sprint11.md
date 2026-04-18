# Month 6 — Analysis Findings (Sprint 11, Day 3)

## Dataset Summary

- **Source:** NASA HTTP access logs, August 1995
- **Final DataFrame:** 1,569,888 rows × 9 columns
- **Numeric columns:** http_response, response_size

---

## Descriptive Statistics (response_size)

| Metric | Value |
|--------|-------|
| Mean | ~17,089 bytes |
| Std | ~67,955 bytes |
| Min | 0 bytes |
| 25th percentile | ~669 bytes |
| 50th percentile (median) | ~3,164 bytes |
| 75th percentile | ~9,202 bytes |
| Max | ~3,421,948 bytes (~3.4 MB) |

### Interpretation

The response_size distribution is heavily right-skewed. The
median (3.1K) is far below the mean (17K), indicating that
most responses are small (HTML pages, small images) while a
small number of very large responses (up to 3.4 MB) pull the
mean upward. This is typical of real web server traffic where
the majority of requests serve lightweight assets and a few
serve large files.

---

## Descriptive Statistics (http_response)

| Metric | Value |
|--------|-------|
| Mean | ~212 |
| Std | ~35 |
| 25th percentile | 200 |
| 50th percentile | 200 |
| 75th percentile | 200 |

### Interpretation

The mean and standard deviation of http_response are
mathematically valid but semantically meaningless. Status codes
are categorical values represented as integers — a "mean of
212" has no real-world interpretation. The percentile values
confirm what the format analysis already documented: ~89% of
responses are status 200, so even the 75th percentile remains
at 200. The `describe()` output for this column is useful only
to confirm the dominance of 200, not for statistical analysis.

---

## Correlation Analysis

### Finding

The Pearson correlation between http_response and response_size
is effectively zero — the heatmap shows no linear relationship.

### Why This Happens

Although a real relationship exists (status 302/304 responses
tend to have response_size of 0, while 200 responses have
varied sizes), Pearson correlation cannot capture it because:

- **Class imbalance:** 89% of rows are status 200 with highly
  varied response sizes. These cases dominate the correlation
  calculation.
- **Non-linear relationship:** The relationship between status
  code and response size is categorical, not linear. A 302
  always has size 0, but a 200 can have any size — this is not
  a pattern that Pearson measures.
- **Low variance in one variable:** With 89% of status codes
  being the same value (200), there is almost no variance for
  Pearson to work with.

### Comparison with Synthetic Data

In the synthetic dataset, correlations were designed and
controlled (CPU→response_time, MEM→response_time). Both
variables had continuous distributions with enough variance
for Pearson to detect the relationship clearly.

In real data, correlations are not designed — they must be
discovered. The signals are hidden behind class imbalance,
outliers, and noise. Pearson correlation alone is insufficient
for this dataset. Future feature engineering (Month 6 Week 2)
will need to create derived features that expose these
relationships — for example, status code categories (2xx, 3xx,
4xx, 5xx) or binary flags (is_error) that make the patterns
explicit.

---

## Metric Thresholds Defined (response_size)

Based on percentile analysis, three buckets were defined:

| Bucket | Range | Rationale |
|--------|-------|-----------|
| low | 0 – 669 bytes | Below 25th percentile |
| normal | 669 – 9,200 bytes | 25th to 75th percentile (IQR) |
| high | 9,200 – max | Above 75th percentile |

Configuration added to `config.yaml`:

```yaml
metric_thresholds:
  response_size:
    low: 669
    normal: 9200
    high: max
```

The `get_metric_thresholds()` function was updated to handle
`"max"` as a dynamic value, resolving to `DataFrame[metric].max()`
at runtime. This mirrors the existing behavior of the lower
bound (`DataFrame[metric].min()`) and makes the function
resistant to datasets with different ranges.

---

## Key Takeaways

1. **Real data distributions are skewed.** Unlike synthetic data
   where distributions were controlled, real web traffic produces
   heavily right-skewed response sizes. Mean is not representative
   — median and percentiles are more informative.

2. **Not all numeric columns are meaningful for statistics.**
   http_response is stored as int for validation purposes, but
   `describe()` and `corr()` outputs for this column are
   misleading. Semantic data type matters, not just storage type.

3. **Correlation discovery is harder in real data.** Designed
   correlations in synthetic data were visible with basic Pearson.
   Real correlations require feature engineering to surface —
   raw columns alone are insufficient.

4. **Class imbalance affects everything.** The 89% dominance of
   status 200 suppresses signals in both descriptive statistics
   and correlation analysis. This will be a recurring challenge
   in feature engineering and ML modeling.
