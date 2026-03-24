# Sprint 4 — Code Refinements

Identified during Sprint 4 code review. Follows the same structure
as the original code_refinements.md.

---

## How to read this document

| Priority | Meaning |
|----------|---------|
| P1 | Fix first — affects correctness or determinism |
| P2 | Fix second — affects clarity and maintainability |
| P3 | Fix third — good improvement, lower urgency |

---

## P1 — Correctness and Determinism

---

### #15 — `log_analysis.py`: `__main__` block has incorrect test data

**File:** `src/analysis/log_analysis.py`

**Current behavior:**
The `expected_columns` dict in the `__main__` block maps `"level"` to
`"int"`. Level is a string column, not an integer.

```python
"level": "int",
```

**Why it matters:**
If someone runs the module directly to test, `_verify_col_dtype` will
reject every line because `level` values are strings like `"INFO"`, not
integers. The test data would produce zero results with no obvious
explanation. Incorrect test data in a portfolio project is misleading.

**What to do:**
Change `"level": "int"` to `"level": "str"` in the `__main__` block.

**Status** [Completed]

Updated the typo in the data type of the `"level"` key.

---

## P2 — Clarity and Maintainability

---

### #16 — `log_analysis.py`: Duplicate `typing` imports

**File:** `src/analysis/log_analysis.py`

**Current behavior:**
```python
from typing import Any
import pandas as pd
import logging
from typing import KeysView
```

Two separate `from typing import` lines.

**Why it matters:**
Python convention is to group imports from the same module. Separate
lines suggest they were added at different times without consolidating.
Additionally, `KeysView` has been available in `collections.abc` since
Python 3.9 — importing from `typing` still works but is the older
pattern.

**What to do:**
Consolidate into a single import. Consider whether `collections.abc`
is more appropriate for `KeysView`.

**Status** [Completed]

Switched to `collections.abc.KeysView` for the typing.

---

### #17 — `log_analysis.py`: Docstring parameter names don't match code

**File:** `src/analysis/log_analysis.py`

**Current behavior:**
In `_verify_col_dtype`, the docstring says `expected_Dtypes` (capital D)
but the parameter is `expected_dtypes`. In `get_metric_thresholds`, the
docstring says `Thresholds` (capitalized) but the parameter is
`thresholds`.

**Why it matters:**
Docstrings are documentation — they should match the code exactly. An
IDE that renders docstring parameter names will show the wrong name.
For a portfolio project, this signals inattention to detail.

**What to do:**
Update the docstring parameter names to match the actual function
signatures.

**Status** [Completed]

Corrected the name of the variables in both Docstrings

---

### #18 — `run_reporting_pipeline.py`: `_dist_report` has hardcoded filename

**File:** `pipelines/run_reporting_pipeline.py`

**Current behavior:**
`_count_report` generates a dynamic filename from the metric name:
`f"{metric_name}_count_plot.png"`. But `_dist_report` hardcodes
`"distribution_report.png"` even though it receives `metric_name`.

**Why it matters:**
If `_dist_report` is called for two different metrics (e.g.
`response_time` and `cpu`), the second call would overwrite the first.
The inconsistency between the two functions is also confusing — they
follow different naming conventions for no clear reason.

**What to do:**
Use a dynamic filename in `_dist_report` following the same pattern
as `_count_report`: `f"{metric_name}_distribution_plot.png"`.

**Status** [Completed]

Added the file name for the distribution report as a dynamic name
taking into account `metric_name`

---

### #19 — `log_visualizer.py`: `__main__` block has broken code

**File:** `src/analysis/log_visualizer.py`

**Current behavior:**
The `__main__` block still calls `sns.countplot(level_dict)` which
passes a dict directly to seaborn — this was the test code from when
you were learning seaborn. It does not work correctly.

**Why it matters:**
Running the module directly produces unexpected behavior. The
`__main__` block should either work correctly or be cleaned up.

**What to do:**
Either update the `__main__` block to use a proper DataFrame for
testing, or clean it up to reflect the current function signatures.

---

## P3 — Good Improvements, Lower Urgency

---

### #20 — `log_analysis.py`: `__main__` block is outdated

**File:** `src/analysis/log_analysis.py`

**Current behavior:**
The `__main__` block still uses the old function signatures and test
data from before the validation orchestrator refactor. It calls
`convert_to_dataframe(log_dicts, expected_columns, expected_values)`
with test data that has incorrect types (see #15).

**Why it matters:**
This is the same item as #12 from the original refinements — the
`__main__` block will be replaced when proper tests are written.
But now it is also incorrectly reflecting the current API.

**What to do:**
If keeping the block, update test data to be correct. When tests
arrive, remove the block entirely.

---

### #21 — `main.py`: `print(main())` still dumps full DataFrame

**File:** `main.py`

**Current behavior:**
Same as original #13 — the full DataFrame is printed to stdout.

**Why it matters:**
The reporting pipeline now saves visualizations to disk, making the
print statement less necessary. With 2000+ rows, the output is
unreadable.

**What to do:**
This is a development convenience. Consider removing the print or
replacing with a summary message (e.g. row count, service analyzed).

---

## Summary

| ID | Module | Issue | Priority |
|----|--------|-------|----------|
| #15 | log_analysis | Incorrect test data in __main__ | P1 |
| #16 | log_analysis | Duplicate typing imports | P2 |
| #17 | log_analysis | Docstring param names wrong | P2 |
| #18 | run_reporting_pipeline | Hardcoded filename in _dist_report | P2 |
| #19 | log_visualizer | Broken __main__ block | P2 |
| #20 | log_analysis | Outdated __main__ block | P3 |
| #21 | main | print(main()) dumps DataFrame | P3 |
