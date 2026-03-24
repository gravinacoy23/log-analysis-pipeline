# Month 3 — Week 1 (Sprint 5)

## Sprint Goal

Begin the transition from data analysis to data engineering. By the
end of this week the pipeline should produce a clean feature dataset
from the log data, persisted to disk, with transformations documented
and config-driven.

---

## Context

Sprint 4 closed Month 2 deliverables. The pipeline now has:

- 4 visualizations saved to `output/plots/` via generalized reporting
  pipeline
- Seaborn integrated (countplot, histplot, heatmap)
- Data quality checks at two layers: parser (structure, field presence,
  empty values) and analysis (column presence, int dtype, categorical
  values)
- Validation orchestrator with single-loop architecture
- Docker volume mounts for output persistence
- Config evolved to dict mapping columns to types

The project is shifting from "can I analyze this data?" to "can I
transform this data into something an ML model can consume?"

---

## Sprint Focus

### Feature Engineering Module

Create `src/features/feature_engineering.py`. This module receives a
DataFrame and produces derived features suitable for ML.

Features to implement:

1. `is_error` — binary flag (1 if level == ERROR, 0 otherwise)
2. `is_slow` — binary flag (1 if response_time > threshold from config)
3. `hour_of_day` — extracted from timestamp column
4. `service_encoded` — numeric encoding of service name
5. `cpu_mem_ratio` — cpu / mem as a derived numeric feature

Each feature must be:
- Config-driven where thresholds are involved
- Documented — what it represents and why it matters for ML

### Config Extension

Add feature engineering thresholds to `config.yaml`:

```yaml
feature_thresholds:
  slow_response_ms: 800
  high_cpu: 70
```

The feature module reads these at runtime — no hardcoded values.

### Persist Feature Dataset

Save the feature dataset to `output/datasets/features.csv`. This is
the first time the pipeline produces a CSV output. The feature dataset
should contain:

- Original columns needed for context (timestamp, service, user)
- All derived features
- No raw metric columns that were already transformed

### Pipeline Integration

Extend `run_pipeline.py` or create a new pipeline that:

1. Runs the existing ingestion → parsing → DataFrame flow
2. Calls the feature engineering module
3. Saves the feature dataset to disk

Think about whether this belongs in `run_pipeline.py` or in a new
pipeline file.

---

## Tech Debt to Address This Sprint

### Parser: Return parsing statistics (🟡)

The parser currently skips malformed lines silently. With the
validation orchestrator also filtering lines, the pipeline has no
visibility into how much data is being lost between raw logs and
the final DataFrame. Adding parsing statistics (lines processed,
lines skipped, skip rate) improves observability.

This connects directly to the feature engineering work — you need
to know if your feature dataset represents 95% of the raw data or
50%.

---

## Day-by-Day Suggestion

### Day 1
- Create `src/features/feature_engineering.py`
- Implement `is_error` and `is_slow` features
- Add `feature_thresholds` to `config.yaml`

### Day 2
- Implement `hour_of_day` (timestamp extraction)
- Implement `service_encoded` (numeric encoding)
- Implement `cpu_mem_ratio`

### Day 3
- Save feature dataset to `output/datasets/features.csv`
- Integrate with pipeline
- Decide: extend existing pipeline or create new one

### Day 4
- Parser statistics: return lines processed, skipped, skip rate
- Surface statistics in pipeline output or logs

### Day 5–7 (Buffer)
- Refactor and clean up
- Documentation updated
- Sprint review and checkpoint

---

## Sprint Deliverable

At the end of Week 1 you must have:

- Feature engineering module with 5 derived features
- Config-driven thresholds for features
- Feature dataset saved to `output/datasets/features.csv`
- Feature module integrated into the pipeline
- Parser returns statistics alongside parsed result
- Documentation updated
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs
- Transformations are documented
- Config values externalized
- Commit pushed
- Results reproducible
