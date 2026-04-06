# Month 10 — Classical Machine Learning

## Primary Goal

Train the first ML model on the log dataset built across Phases 1,
1.5, and 2. Start with classical algorithms — understand them deeply
before moving to neural networks.

---

# Technical Focus

## Linear Regression

- What linear regression is and when to use it
- Implementing from scratch (gradient descent)
- Implementing with scikit-learn
- Predicting a numeric target from the feature dataset
- Interpreting coefficients

## Logistic Regression

- Binary and multiclass classification
- Predicting the target variable from derived features
- Decision boundary interpretation
- Probability outputs

## Feature Scaling

- Why scaling matters for gradient-based models
- StandardScaler and MinMaxScaler
- When to scale and when not to
- Scaling the log feature dataset

## Model Evaluation

- Train/test split (already done in Month 4)
- Accuracy, precision, recall, F1
- Confusion matrix
- When accuracy is misleading

## Overfitting vs Underfitting

- Learning curves
- Regularization basics (L1, L2)
- Cross-validation

---

# ML Objective

Using the feature dataset produced by the pipeline:

**Task 1 — Regression:**
Identify a numeric column in the feature dataset suitable for
regression. Predict it from other features. The specific target
depends on the dataset available at this point — if working with
real web server logs, response size or request rate could be
candidates.

**Task 2 — Classification:**
Predict the error/non-error classification (or equivalent target)
from the available features. This is the primary ML task — the
feature dataset was designed with this in mind since Month 4.

The specific features and targets will be defined when Month 10
begins, based on whatever dataset the pipeline produces at that
point (synthetic or real web server logs).

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── src/
│   └── models/
│       └── train.py              ← new this month
│       └── evaluate.py           ← new this month
│
├── output/
│   └── models/                   ← new this month
│       └── logistic_v1.pkl
│
├── docs/
│   └── ml_experiment_01.md       ← new this month
```

---

# Model Versioning

Models are saved with a version suffix — `logistic_v1.pkl`, `linear_v1.pkl`.
This is manual for now. Experiment tracking tools come in Month 11.

---

# Deliverables

By the end of Month 10 you must have:

- Linear regression model trained and evaluated
- Logistic regression model trained and evaluated
- Evaluation metrics documented
- Confusion matrix visualization
- Models saved to `output/models/`
- Experiment documented in `docs/ml_experiment_01.md`
- Frequent commits

---

# Definition of Done

A task is complete when:

- Model trains without errors
- Evaluation metrics are computed and documented
- Model artifact is saved
- Commit pushed
