# Month 3 — Data Engineering Thinking

## Primary Goal

Transition from analysis scripts to a reproducible, automated data
engineering pipeline. This month is about discipline and infrastructure
— making the pipeline reliable, configurable, and runnable without
manual intervention.

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── src/
│   └── features/
│       └── feature_engineering.py    ← new this month
│
├── scripts/
│   └── run_daily.sh                  ← new this month
│
├── output/
│   └── datasets/                     ← new this month (clean feature datasets)
```

---

# Technical Focus

## Feature Engineering

Feature engineering is the process of transforming raw data into
inputs that are meaningful for ML models. This month you create the
first version of the feature dataset from the log pipeline.

Features to extract from logs:

- `is_error` — binary flag (1 if level == ERROR, 0 otherwise)
- `is_slow` — binary flag (1 if response_time > 800)
- `hour_of_day` — extracted from timestamp
- `cpu_bucket` — categorical: low / medium / high
- `service_id` — numeric encoding of service name

This dataset will be used for ML in Phase 3.

## Reproducible Transformations

Every transformation must be:
- Documented — what it does and why
- Deterministic — same input always produces same output
- Configurable — thresholds come from `config.yaml`, not hardcoded

## Config-Driven Pipeline

Extend `config.yaml` to include:

```yaml
thresholds:
  slow_response_ms: 800
  high_cpu: 70
  medium_cpu: 50
```

The feature engineering layer reads these at runtime.

## Linux Automation

### Bash Basics
- Writing a basic shell script
- Running Python scripts from bash
- Exit codes and error handling in bash
- Environment variables in bash

### Cron
- Cron syntax
- Scheduling the pipeline to run automatically
- Logging cron output

---

# Pipeline Evolution

By end of Month 3 the pipeline looks like this:

```
log_generator.py (scheduled via cron)
    → data/raw/<service>/
    → log_reader.py
    → log_parser.py
    → DataFrame
    → feature_engineering.py
    → output/datasets/features.csv
```

The feature dataset is persisted to disk — not just printed.

---

# Deliverables

By the end of Month 3 you must have:

- Feature engineering module with at least 5 derived features
- Clean feature dataset saved to `output/datasets/`
- Bash script that runs the full pipeline
- Cron job configured to run the pipeline on a schedule
- Config-driven thresholds
- Documented transformations
- Frequent commits

---

# Definition of Done

A task is complete when:

- Code runs
- Transformations are documented
- Config values externalized
- Cron job tested
- Commit pushed
- Results reproducible
