# Sprint 7 — Code Refinements

Identified during Sprint 7 code review. Follows the same structure
as the previous code_refinements documents.

---

## How to read this document

| Priority | Meaning |
|----------|---------|
| P1 | Fix first — affects correctness or determinism |
| P2 | Fix second — affects clarity and maintainability |

---

## P1 — Correctness and Determinism

---

### #27 — `log_statistical_analysis.py`: Missing `random_state` in train/test split

**File:** `src/analysis/log_statistical_analysis.py`

**Current behavior:**
```python
return train_test_split(dataset, test_size=0.2, stratify=dataset["is_error"])
```

`train_test_split` is called without `random_state`, which means
every execution produces a different split.

**Why it matters:**
The project's Definition of Done requires reproducible results.
Without a fixed seed, running the pipeline twice produces different
training and test sets. This makes it impossible to verify results
or compare experiments — a fundamental requirement for ML work in
Phase 3.

**What to do:**
Add `random_state=42` (or any fixed integer) to the
`train_test_split` call. Consider whether this value should come
from the config file for flexibility.

**Status** [Completed]

---

## P2 — Clarity and Maintainability

---

### #28 — `run_statistical_pipeline.py`: Imprecise docstring for `_get_directory()`

**File:** `pipelines/run_statistical_pipeline.py`

**Current behavior:**
```python
def _get_directory() -> Path:
    """Resolves the directory where the file is located."""
```

"The file" is ambiguous — it could refer to the pipeline module
itself, the features CSV, or the output files.

**Why it matters:**
A reader of the docstring should understand what directory is
being resolved without reading the implementation. The function
resolves the `output/datasets/` directory used for both loading
the feature dataset and saving the train/test splits.

**What to do:**
Update the docstring to specify that it resolves the
`output/datasets/` directory.

**Status** [Completed]

---

## Summary

| ID | Module | Issue | Priority |
|----|--------|-------|----------|
| #27 | log_statistical_analysis | Missing random_state | P1 |
| #28 | run_statistical_pipeline | Imprecise docstring | P2 |
