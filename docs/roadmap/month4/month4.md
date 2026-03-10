# Month 4 — Statistical Foundations for ML

## Primary Goal

Build the statistical intuition required to work with ML responsibly.
This month bridges data engineering and machine learning — you learn
to understand your data before modeling it.

---

# Technical Focus

## Probability Basics

- What is a probability distribution
- Uniform, normal, and skewed distributions
- How the log generator's distributions look (and why)
- Expected value and variance

## Descriptive Statistics

- Mean, median, mode — when each is appropriate
- Standard deviation and variance
- Percentiles and quartiles
- Outlier detection

## Correlation vs Causation

- Pearson correlation coefficient
- Correlation matrix with seaborn heatmap
- Verify the CPU → response_time correlation designed into the generator
- Why correlation does not imply causation

## Train / Test Split

- Why you split data before modeling
- `sklearn.model_selection.train_test_split`
- Stratified splits for imbalanced data
- Data leakage — what it is and how to avoid it

## Bias vs Variance

- Underfitting vs overfitting
- The bias-variance tradeoff
- How to detect each with evaluation metrics

## Evaluation Metrics

- Accuracy — when it is misleading
- Precision, recall, F1 score
- Confusion matrix
- When to use each metric

---

# Analysis Objectives

Using the log feature dataset built in Month 3:

### Distribution Analysis
- Plot distribution of response_time, cpu, mem
- Identify skew and outliers
- Compare distributions across services

### Correlation Analysis
- Correlation matrix of all numeric features
- Verify CPU → response_time correlation
- Identify any unexpected correlations

### Dataset Splitting
- Split the feature dataset into train/test sets
- Verify the split preserves class balance (INFO/WARNING/ERROR)
- Save splits to `output/datasets/`

### Statistical Report
- Write a documented analysis in `docs/statistical_analysis.md`
- Include plots, findings, and interpretation

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── src/
│   └── analysis/
│       └── statistical_analysis.py    ← new this month
│
├── output/
│   └── datasets/
│       ├── train.csv                  ← new this month
│       └── test.csv                   ← new this month
│
├── docs/
│   └── statistical_analysis.md        ← new this month
```

---

# Deliverables

By the end of Month 4 you must have:

- Statistical analysis module
- Distribution plots for all numeric features
- Correlation matrix visualization
- Train/test split of the feature dataset
- Documented EDA in `docs/statistical_analysis.md`
- Frequent commits

---

# Definition of Done

A task is complete when:

- Code runs
- Analysis is documented with interpretation
- Train/test splits are saved and reproducible
- Commit pushed
