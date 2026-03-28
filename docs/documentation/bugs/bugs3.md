# Sprint 5 — Code Refinements

Identified during Sprint 5 code review. Follows the same structure
as the previous code_refinements documents.

---

## How to read this document

| Priority | Meaning |
|----------|---------|
| P1 | Fix first — affects correctness or determinism |
| P2 | Fix second — affects clarity and maintainability |
| P3 | Fix third — good improvement, lower urgency |

---

## P2 — Clarity and Maintainability

---

### #22 — `feature_engineering.py`: Context columns hardcoded in orchestrator

**File:** `src/features/feature_engineering.py`

**Current behavior:**
```python
context_cols = ["timestamp", "service", "user"]
```

The list of context columns is defined inside `orchestrate_features()`.

**Why it matters:**
The rest of the pipeline treats `config.yaml` as the source of truth
for column names. If a column name changes in the config, this list
would be out of sync with no error or warning — the feature dataset
would silently produce incorrect results.

**What to do:**
Consider whether this should come from the config or if the current
approach is acceptable given that these column names are stable.

---

### #23 — `feature_engineering.py`: Missing `__init__.py` in `src/features/`

**File:** `src/features/`

**Current behavior:**
Verify whether `__init__.py` exists in the `src/features/` directory.

**Why it matters:**
Without `__init__.py`, Python may have issues importing the module
depending on the execution context. All other directories under `src/`
(`ingestion/`, `processing/`, `analysis/`) should have one for
consistency.

**What to do:**
Verify the directory has an `__init__.py`. If not, create an empty one.
Also verify the other `src/` subdirectories have one.

---

## P3 — Good Improvements, Lower Urgency

---

### #24 — `config_loader.py`: Does not validate `feature_thresholds` key

**File:** `src/config_loader.py`

**Current behavior:**
`load_config()` validates that the `columns` key exists but does not
validate `feature_thresholds`. If that key is missing from
`config.yaml`, the error surfaces as a generic `KeyError` in
`run_features_pipeline` when it tries to access
`raw_data["feature_thresholds"]`.

**Why it matters:**
The project follows a fail-fast principle — missing config should
produce a descriptive error immediately, not a confusing `KeyError`
downstream. This is the same pattern already applied for `columns`.

**What to do:**
Add validation for `feature_thresholds` in `load_config()`. Consider
whether other keys (`service`, `level`, `metric_thresholds`) should
also be validated here for consistency.

---

### #25 — `log_parser.py`: Docstring return description is imprecise

**File:** `src/processing/log_parser.py`

**Current behavior:**
The docstring for `parse_logs` says:
```
"three stats of lines skipped and processed"
```

**Why it matters:**
The description does not specify which three stats are returned. A
reader of the docstring should know without reading the implementation
that the stats dict contains `lines_processed`, `skipped_lines`, and
`skip_rate`.

**What to do:**
Update the return description to explicitly name the three stats.

---

### #26 — `run_pipeline.py`: Extra blank line in docstring

**File:** `pipelines/run_pipeline.py`

**Current behavior:**
There is an extra blank line between the `Args` section and the
`Returns` section in the `run_pipeline` docstring.

**Why it matters:**
Inconsistent with the Google-style docstring format used across the
rest of the project. Minor, but visible in a portfolio project.

**What to do:**
Remove the extra blank line.

---

## Summary

| ID | Module | Issue | Priority |
|----|--------|-------|----------|
| #22 | feature_engineering | Context columns hardcoded | P2 |
| #23 | feature_engineering | Missing __init__.py | P2 |
| #24 | config_loader | No validation for feature_thresholds | P3 |
| #25 | log_parser | Imprecise docstring return | P3 |
| #26 | run_pipeline | Extra blank line in docstring | P3 |
