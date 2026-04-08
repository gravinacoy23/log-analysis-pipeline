# Sprint 10 — Code Refinements

Identified during Sprint 10 code review. Follows the same structure
as the previous code_refinements documents.

---

## How to read this document

| Priority | Meaning |
|----------|---------|
| P1 | Fix first — affects correctness or determinism |
| P2 | Fix second — affects clarity and maintainability |
| P3 | Fix when convenient — minor improvements |

---

## P1 — Correctness and Determinism

---

### #29 — `log_parser.py`: Missing `return None` in `http_response` malformed case

**File:** `src/processing/log_parser.py`

**Current behavior:**
```python
elif col_title == "http_response":
    if item.isdigit():
        log_dict[col_title] = int(item)
    else:
        logger.warning(f"Malformed line skipped at line {line_number}")
```

The `else` branch logs a warning but does not `return None`. The
line continues without `http_response` in the dict, and
`_verify_columns` catches it downstream. Works by accident.

**Why it matters:**
The intent is to skip the line immediately. Relying on a
downstream check to catch a known-bad line is fragile and
inconsistent with the `response_size` handling which correctly
returns `None`.

**What to do:**
Add `return None` after the logger warning.

**Status** [Completed]

Added missing return statement

---

### #30 — `run_pipeline.py`: Leftover `print(logs_dataframe)`

**File:** `pipelines/run_pipeline.py`

**Current behavior:**
Debug `print` statement left in the pipeline after testing.

**Why it matters:**
Prints 1.57M rows to stdout on every execution. Not appropriate
for committed code.

**What to do:**
Remove the `print(logs_dataframe)` line.

**Status** [Completed]

Deleted print.

---

### #31 — `run_pipeline.py`: Docstring references removed `service` parameter

**File:** `pipelines/run_pipeline.py`

**Current behavior:**
```python
def run_pipeline(raw_data: dict[str, Any]) -> pd.DataFrame:
    """...
    Args:
        service: name of the service to process.
        raw_data: raw data loaded from the config file.
    """
```

The `service` parameter was removed but the docstring still
documents it.

**Why it matters:**
Docstring contradicts the function signature. Misleading for
anyone reading the code.

**What to do:**
Remove the `service` line from the Args section.

**Status** [Completed]

Removed the deprecated parameter

---

### #32 — `log_analysis.py`: `filter_loglevel()` still in code

**File:** `src/analysis/log_analysis.py`

**Current behavior:**
`filter_loglevel()` references the `level` column which does not
exist in CLF logs. The function was marked for deprecation but
remains in the codebase.

**Why it matters:**
Dead code that references non-existent columns. If called, it
would raise a `KeyError`.

**What to do:**
Remove the function. It is preserved in git history on `main`.

**Status** [Completed]

Removing deprecated function

---

## P2 — Clarity and Maintainability

---

### #33 — `log_parser.py`: `_parse_fields` docstring missing `expected_columns` parameter

**File:** `src/processing/log_parser.py`

**Current behavior:**
The docstring documents `split_log_line` and `line_number` but
does not mention the third parameter `expected_columns`.

**Why it matters:**
Incomplete docstrings are misleading — a reader expects all
parameters to be documented per the project's Google-style
docstring convention.

**What to do:**
Add `expected_columns` to the Args section of the docstring.

**Status** [ ]

---

### #34 — `log_analysis.py`: `_verify_response_field` has no type hints or docstring

**File:** `src/analysis/log_analysis.py`

**Current behavior:**
```python
def _verify_response_field(value, value_range, line_number):
```

No type hints on parameters or return type. No docstring. Every
other function in the module has both.

**Why it matters:**
Inconsistent with the project's convention of type hints and
Google-style docstrings on all functions.

**What to do:**
Add type hints and a docstring following the same pattern as
the other validation functions.

**Status** [ ]

---

### #35 — `run_pipeline.py`: Unused `get_metric_thresholds` import

**File:** `pipelines/run_pipeline.py`

**Current behavior:**
```python
from src.analysis.log_analysis import convert_to_dataframe, get_metric_thresholds
```

`get_metric_thresholds` is imported but no longer called after
removing the cpu/mem threshold calls.

**Why it matters:**
Unused imports are noise. Pyright may flag it as well.

**What to do:**
Remove `get_metric_thresholds` from the import statement.

**Status** [ ]

---

## P3 — Minor

---

### #36 — `log_parser.py`: `_parse_fields` parameter missing type hint

**File:** `src/processing/log_parser.py`

**Current behavior:**
```python
def _parse_fields(
    split_log_line: tuple[str | Any, ...], line_number: int, expected_columns
) -> dict[str, Any] | None:
```

`expected_columns` has no type hint.

**Why it matters:**
Minor inconsistency with the rest of the module where all
parameters have explicit type hints.

**What to do:**
Add `list[str]` type hint to `expected_columns`.

**Status** [ ]

---

## Summary

| ID | Module | Issue | Priority |
|----|--------|-------|----------|
| #29 | log_parser | Missing return None for http_response | P1 |
| #30 | run_pipeline | Leftover print statement | P1 |
| #31 | run_pipeline | Docstring references removed parameter | P1 |
| #32 | log_analysis | Dead function filter_loglevel | P1 |
| #33 | log_parser | Incomplete docstring | P2 |
| #34 | log_analysis | Missing type hints and docstring | P2 |
| #35 | run_pipeline | Unused import | P2 |
| #36 | log_parser | Missing parameter type hint | P3 |
