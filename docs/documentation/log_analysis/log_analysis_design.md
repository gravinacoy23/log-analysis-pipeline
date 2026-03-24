# Log Analysis Module — Design (v6)

## Objective

Provide the analytical layer of the pipeline.
Receives structured log data and converts it into a pandas DataFrame
ready for analysis and visualization. Validates column presence, data
types of numeric columns, and expected values of categorical columns
through an orchestrated validation flow. Supports computed columns
derived from config-driven thresholds and correlation analysis.

---

# Validation Layer

Validation is orchestrated by `_validation_orchestrator()` which runs
three checks in sequence before DataFrame creation. Each check has a
single responsibility and operates at a specific level.

## Validation Flow

```
1. _verify_columns()       → hard stop if list empty or columns missing
2. For each log dict:
   a. _verify_col_dtype()  → reject if numeric columns have wrong type
   b. _verify_col_values() → reject if categorical columns have unexpected values
   c. If both pass         → append to verified list
3. Return verified list    → convert_to_dataframe() creates DataFrame
```

---

## Function: _validation_orchestrator()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — dict mapping column names to expected data type
  strings (e.g. `{"cpu": "int", "service": "str"}`)
- `expected_values` — dict mapping categorical column names to lists
  of valid values (e.g. `{"service": ["shopping", "pricing", "booking"]}`)

### Returns

- `list[dict[str, Any]]` — list of dicts containing only lines that
  passed all validation checks

### Implementation Details

- Calls `_verify_columns()` first as a hard stop — if the list is
  empty or columns are missing, raises `ValueError` immediately
- Extracts the list of int column names from `expected_columns` once
  before the loop — avoids rebuilding the same list on every iteration
- Iterates over each dict, calling `_verify_col_dtype()` and
  `_verify_col_values()` in sequence
- Uses early `continue` — if dtype validation fails, content
  validation is skipped for that line
- Only appends to the result list if both checks pass

### Design Decisions

- **Single loop for all per-line validations.** Earlier design had
  separate loops in each validation function, which would iterate
  the full list multiple times. The orchestrator runs one loop and
  calls validation functions per dict, avoiding duplication.

- **Int column extraction before the loop.** The list of columns
  that should be `int` is derived from the config and does not change
  per line. Building it once and passing it to `_verify_col_dtype()`
  avoids redundant work inside the loop.

- **Early continue on first failure.** If a line fails dtype
  validation, there is no point checking its categorical values.
  `continue` skips to the next line immediately.

---

## Function: _verify_columns()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — keys view or iterable of required column names

### Returns

- None — raises an error if validation fails

### Implementation Details

- Checks that `log_dicts` is not empty — an empty list cannot produce
  a valid DataFrame
- Extracts column names from the first dict in the list using `.keys()`
- Iterates over `expected_columns` and raises a `ValueError` if any
  required column is missing

### Design Decisions

- **Hard stop, not skip.** An empty list or missing columns are
  structural problems — there is nothing to filter or recover from.
  Raising immediately prevents downstream functions from operating
  on invalid data.
- **Called by the orchestrator, not by individual validation
  functions.** Column presence must be verified once before any
  per-line validation begins. The orchestrator owns the order.

---

## Function: _verify_col_dtype()

### Parameters

- `log_line` — single dictionary containing one parsed log line
- `expected_dtypes` — list of column names that should be `int`
- `line_number` — current line number for warning messages

### Returns

- `bool` — `True` if all int columns contain `int` values,
  `False` if any column fails

### Implementation Details

- Iterates over the expected int column names
- Uses `isinstance(log_line[col], int)` to check each value
- Returns `False` on first failure — no need to check remaining
  columns for the same line
- Logs a warning identifying the column name and line number

### Design Decisions

- **Receives a single dict, not a list.** The loop lives in the
  orchestrator. This function only validates one line, making it
  simple and reusable.

- **Returns bool instead of filtering.** The orchestrator decides
  whether to append or skip based on the return value. The function
  does not need to know about the result list.

- **Currently validates only `int` columns.** The config maps all
  column names to type strings, but only `int` is checked at this
  stage. Full type validation for `str` and `datetime` is planned
  for Month 3 — the interface supports it without signature changes.

---

## Function: _verify_col_values()

### Parameters

- `log_line` — single dictionary containing one parsed log line
- `expected_values` — dict mapping categorical column names to lists
  of valid values
- `line_number` — current line number for warning messages

### Returns

- `bool` — `True` if all categorical columns contain expected values,
  `False` if any column has an unexpected value

### Implementation Details

- Iterates over `expected_values` keys (the categorical columns to
  check), not over the full log line — more efficient since
  `expected_values` has fewer keys than the log dict
- Checks if the log line's value for each column is in the list of
  valid values
- Returns `False` on first failure
- Logs a warning identifying the column, the unexpected value, and
  the line number

### Design Decisions

- **Iterates over `expected_values`, not over `log_line`.** The
  function only cares about columns that have expected value
  constraints. Iterating over the smaller dict avoids checking
  columns that have no constraints.

- **Expected values come from the config via the pipeline.** The
  `service` and `level` lists already exist in `config.yaml`. The
  pipeline orchestrator builds the `expected_values` dict and passes
  it through — the analysis layer does not load config directly.

- **Validates content, not structure or type.** This function
  assumes the column exists (verified by `_verify_columns`) and
  contains the right type (verified by `_verify_col_dtype`). It
  only checks whether the value is one of the expected options.

---

## Function: convert_to_dataframe()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — dict mapping column names to expected data
  type strings
- `expected_values` — dict mapping categorical column names to lists
  of valid values

### Returns

- `pd.DataFrame` with one row per log entry and correct dtypes

### Implementation Details

- Calls `_validation_orchestrator()` which runs all three validation
  checks and returns a clean list
- DataFrame is created from the verified list
- `timestamp` dtype is already `datetime` when it arrives —
  conversion is handled upstream in `log_parser.py`

### Design Decisions

- `convert_to_dataframe()` does not know the details of validation —
  it delegates entirely to the orchestrator and receives a clean list
- The function signature accepts both `expected_columns` and
  `expected_values` and passes them through to the orchestrator

---

## Function: filter_loglevel()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `level` — string representing the log level to filter (e.g. "INFO", "WARNING", "ERROR")

### Returns

- `pd.DataFrame` containing only rows where `level` matches the input

### Implementation Details

- Uses boolean indexing with `.loc[]`
- Preserves original DataFrame indices in the result

---

## Function: select_col()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `column_name` — string with the name of the column to select

### Returns

- `pd.DataFrame | pd.Series` — returns a Series when the column name
  is unique, returns a DataFrame if duplicate column names exist

### Implementation Details

- Uses standard pandas column selection with `df[column_name]`

---

## Function: count_by_level()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data
- `level` — string representing the log level to count

### Returns
- `int` — number of rows matching the given log level

### Implementation Details
- Uses a boolean condition `(df["level"] == level).sum()`

---

## Function: count_by_level_all()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.Series` — count of log entries per level, sorted by frequency

### Implementation Details
- Uses `df.value_counts("level")`

---

## Function: count_by_service()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data
- `service` — string representing the service name to count

### Returns
- `int` — number of rows matching the given service

### Implementation Details
- Uses a boolean condition `(df["service"] == service).sum()`

---

## Function: count_by_service_all()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.Series` — count of log entries per service, sorted by frequency

### Implementation Details
- Uses `df.value_counts("service")`

---

## Function: mean_rt_by_service()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.Series` — mean response_time per service

### Implementation Details
- Uses `.groupby("service")["response_time"].mean()`

---

## Function: mean_cpu_by_level()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.Series` — mean CPU usage per log level

### Implementation Details
- Uses `.groupby("level")["cpu"].mean()`

---

## Function: get_metric_thresholds()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data
- `metric` — string with the name of the numeric column to classify
  (e.g. `"cpu"`, `"mem"`)
- `thresholds` — dictionary loaded from `config.yaml` containing
  the threshold values per metric

### Returns
- None — mutates the DataFrame by adding a new column
  `<metric>_bucket` with values `"low"`, `"normal"`, or `"high"`

### Implementation Details

- Reads threshold boundaries from the config dictionary for the
  given metric
- Uses the DataFrame column's `.min()` as the lower edge to ensure
  all values are covered regardless of the metric's range
- Uses `pd.cut()` with `include_lowest=True` to classify each row
  into a bucket based on the threshold boundaries
- The new column is named `f"{metric}_bucket"` (e.g. `cpu_bucket`,
  `mem_bucket`)

### Config Structure

```yaml
metric_thresholds:
  cpu:
    low: 44
    normal: 57
    high: 70
  mem:
    low: 52
    normal: 63
    high: 75
```

---

## Function: convert_corr_matrix()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.DataFrame` — correlation matrix of all numeric columns

### Implementation Details

- Uses `select_dtypes(include="number")` to extract only numeric
  columns from the DataFrame
- Applies `.corr("pearson")` to compute the Pearson correlation
  matrix across all numeric columns

---

## Changes from v5

- Added `_validation_orchestrator()` — single loop that calls all
  per-line validation functions, replaces the previous approach where
  `_verify_col_dtype()` iterated the full list internally
- `_verify_col_dtype()` refactored to receive a single dict and
  return bool — no longer manages its own loop or calls
  `_verify_columns()` internally
- `_verify_columns()` now called by the orchestrator directly —
  no longer nested inside `_verify_col_dtype()`
- Added `_verify_col_values()` — validates that categorical columns
  (service, level) contain only expected values from the config
- `convert_to_dataframe()` now receives `expected_values` as a third
  parameter — passes it through to the orchestrator
- Int column extraction moved from `_verify_col_dtype()` to the
  orchestrator — built once before the loop instead of per iteration

---

## Future Improvements (Planned)

- Full type validation for all data types (`str`, `datetime`) —
  Month 3, the interface is already in place
- Expand analytical functions to support a full dashboard with more
  metric combinations (e.g. mean memory by service, error rate over time)
