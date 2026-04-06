# Month 11 — Structured ML Pipeline

## Primary Goal

Make the ML workflow reproducible and structured. Move from ad-hoc
training scripts to a proper ML pipeline with experiment tracking,
hyperparameter testing, and model management.

---

# Technical Focus

## Reproducible Training

- Seeds for reproducibility (`random.seed`, `numpy.random.seed`)
- Config-driven training — hyperparameters in `config.yaml`
- Same config always produces same model
- Training logs saved to disk

## Experiment Tracking (Manual First)

Before using MLflow or similar tools, track experiments manually:

```
output/experiments/
    experiment_001/
        config.yaml         ← exact config used
        metrics.json        ← train/test metrics
        model.pkl           ← saved model
        notes.md            ← observations
```

This builds the intuition for why tools like MLflow exist.

## Hyperparameter Testing

- What hyperparameters are
- Grid search with `sklearn.model_selection.GridSearchCV`
- Recording results across runs
- Choosing the best model based on metrics

## Saving and Loading Models

- `joblib` for saving sklearn models
- Loading a model and running inference
- Model versioning strategy

---

# ML Pipeline Evolution

By end of Month 11 the ML workflow looks like this:

```
config.yaml (hyperparameters)
    → train.py
    → model artifact + metrics
    → output/experiments/<run_id>/
```

Each training run is isolated and reproducible.

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── output/
│   └── experiments/
│       └── run_001/
│           ├── config.yaml
│           ├── metrics.json
│           ├── model.pkl
│           └── notes.md
│
├── docs/
│   └── experiment_tracking.md    ← new this month
```

---

# Deliverables

By the end of Month 11 you must have:

- Reproducible training pipeline
- At least 3 documented experiments with different hyperparameters
- Grid search results compared and documented
- Best model identified and saved
- Manual experiment tracking structure in `output/experiments/`
- Frequent commits

---

# Definition of Done

A task is complete when:

- Training is reproducible from config alone
- Experiment results are documented
- Best model is saved with its config
- Commit pushed
