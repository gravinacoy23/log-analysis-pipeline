# Month 8 — Classical Machine Learning

## Primary Goal

Train the first ML model on the log dataset built across Phases 1 and 2.
Start with classical algorithms — understand them deeply before moving
to neural networks.

---

# Technical Focus

## Linear Regression

- What linear regression is and when to use it
- Implementing from scratch (gradient descent)
- Implementing with scikit-learn
- Predicting `response_time` from `cpu` and `mem`
- Interpreting coefficients

## Logistic Regression

- Binary and multiclass classification
- Predicting log level (INFO / WARNING / ERROR) from metrics
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

Using the feature dataset from Month 3:

**Task 1 — Regression:**
Predict `response_time` from `cpu`, `mem`, and service.

**Task 2 — Classification:**
Predict `level` (INFO / WARNING / ERROR) from `cpu`, `mem`, and `response_time`.

Task 2 is interesting because the generator designed this relationship
explicitly — the model should be able to learn it.

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
This is manual for now. Experiment tracking tools come in Month 9.

---

# Deliverables

By the end of Month 8 you must have:

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
