# Log Analysis Module — Design (v7)

## Objective

Provide the analytical layer of the pipeline.
Receives structured log data and converts it into a pandas DataFrame
ready for analysis and visualization. Validates column presence, data
types of numeric columns, expected values of categorical columns, and
numeric range of status codes through an orchestrated validation flow.
Supports computed columns derived from config-driven thresholds and
correlation analysis.

---

# Validation Layer

Validation is orchestrated by `_validation_orchestrator()` which runs
checks in sequence before DataFrame creation. Each check has a single
responsibility and operates at a specific level.

## Validation Flow

```
1. _verify_columns()            → hard stop if list empty or columns missing
2. For each log dict:
   a. _verify_col_dtype()       → reject if numeric columns have wrong type
   b. _verify_col_values()      → reject if categorical columns have unexpected
                                   values or if http_response is outside valid range
   c. If both pass              → append to verified list
3. Return verified list         → convert_to_dataframe() creates DataFrame
```

---

## Function: _validation_orchestrator()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — dict mapping column names to expected data type
  strings (e.g. `{"http_response": "int", "host": "str"}`)
- `expected_values` — dict mapping categorical column names to lists
  of valid values, and `http_response` to a two-element list
  representing a valid range (e.g. `{"method": ["GET", "POST", "HEAD"],
  "http_response": [100, 599]}`)

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

- **Single loop for all per-line validations.** The orchestrator runs
  one loop and calls validation functions per dict, avoiding
  duplication.

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
- **Called by the orchestrator, not by individual validation
  functions.** Column presence must be verified once before any
  per-line validation begins.

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
- Returns `False` on first failure
- Logs a warning identifying the column name and line number

### Design Decisions

- **Receives a single dict, not a list.** The loop lives in the
  orchestrator. This function only validates one line.
- **Returns bool instead of filtering.** The orchestrator decides
  whether to append or skip based on the return value.

---

## Function: _verify_col_values()

### Parameters

- `log_line` — single dictionary containing one parsed log line
- `expected_values` — dict mapping categorical column names to lists
  of valid values, and `http_response` to a range list
- `line_number` — current line number for warning messages

### Returns

- `bool` — `True` if all columns contain expected values,
  `False` if any column has an unexpected value

### Implementation Details

- Iterates over `expected_values` keys
- For `http_response`: delegates to `_verify_response_field()`
  which validates the value falls within the configured range
- For `protocol_version` with `None` value: skips validation via
  `continue` — `None` represents a legitimately absent protocol_version
  (request lines without HTTP version), not invalid content
- For all other columns: checks if the value is in the list of
  valid values
- Uses `elif` chain to ensure only one validation path executes
  per column
- Returns `False` on first failure
- Logs a warning identifying the column, the unexpected value,
  and the line number

### Design Decisions

- **`http_response` handled via separate function.** Status codes
  are validated by numeric range, not by list membership. A
  separate function keeps the validation logic clean and avoids
  special-casing inside the list-check logic.

- **`protocol_version` with `None` skipped via `continue`.** The parser
  sets protocol_version to `None` when the request line lacks an HTTP
  version — this is a valid, intentional decision to preserve
  the method and endpoint data. `None` cannot be represented
  cleanly in YAML config as an expected value, and it is not
  an "expected value" in the same sense as `HTTP/1.0` — it is
  the absence of a value. Skipping validation for `None`
  protocol_version is the cleanest approach: the parser already decided
  the line is valid, and the analysis layer respects that
  decision. `None` becomes `NaN` in the DataFrame, which pandas
  handles natively with `.isna()`, `.fillna()`, `.dropna()`.

- **`elif` for mutual exclusivity.** When `column == "http_response"`,
  the range check runs. When `column == "protocol_version"` and value is
  `None`, validation is skipped. For all other columns, the list
  check runs. The `elif` chain prevents multiple checks from
  executing on the same column — a bug that was caught and fixed
  during implementation.

---

## Function: _verify_response_field()

### Parameters

- `value` — the `http_response` value from the log line (int)
- `value_range` — two-element list `[min, max]` from config
- `line_number` — current line number for warning messages

### Returns

- `bool` — `True` if value is within the range, `False` otherwise

### Implementation Details

- Uses `range(value_range[0], value_range[1])` to validate
- Logs a warning if the value is outside the expected range

### Design Decisions

- **Config-driven range.** The valid range `[100, 599]` is defined
  in `config.yaml` under `expected_values.http_response`. This
  keeps the validation flexible — if the pipeline needs to accept
  a different range, only the config changes.

- **Separate function instead of inline logic.** Keeps
  `_verify_col_values()` focused on its generic list-based
  validation. The range validation is a distinct type of check
  that deserves its own function.

---

## Function: convert_to_dataframe()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — dict mapping column names to expected data
  type strings
- `expected_values` — dict mapping column names to valid values
  or ranges

### Returns

- `pd.DataFrame` with one row per log entry and correct dtypes

### Implementation Details

- Calls `_validation_orchestrator()` which runs all validation
  checks and returns a clean list
- DataFrame is created from the verified list

---

## Function: convert_corr_matrix()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.DataFrame` — correlation matrix of all numeric columns

### Implementation Details
- Uses `select_dtypes(include="number")` to extract numeric columns
- Applies `.corr("pearson")` for Pearson correlation

---

## Function: select_col()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data
- `column_name` — string with the name of the column to select

### Returns
- `pd.DataFrame | pd.Series`

---

## Function: get_metric_thresholds()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data
- `metric` — string with the name of the numeric column to classify
- `thresholds` — dictionary from config with threshold boundaries

### Returns
- None — mutates the DataFrame by adding a `<metric>_bucket` column

### Implementation Details
- Uses `pd.cut()` with config-driven edges and labels
- Uses DataFrame column `.min()` as the lower edge

### Design Decisions
- **Generic function preserved.** Works with any numeric column
  and any set of thresholds from config. Not tied to specific
  columns from the synthetic or real log format.

---

## Deprecated (removed in v7)

| Function | Reason |
|---|---|
| `filter_loglevel()` | Hardcoded to `level` column — does not exist in CLF |
| `count_by_level()` | Hardcoded to `level` column |
| `count_by_level_all()` | Hardcoded to `level` column |
| `count_by_service()` | Hardcoded to `service` column — does not exist in CLF |
| `count_by_service_all()` | Hardcoded to `service` column |
| `mean_rt_by_service()` | Hardcoded to `service` and `response_time` columns |
| `mean_cpu_by_level()` | Hardcoded to `level` and `cpu` columns |

All deprecated code is preserved in git history on the `main`
branch.

---

## Changes from v6

- Added `_verify_response_field()` — validates `http_response`
  against a numeric range from config instead of a list of
  values
- `_verify_col_values()` updated with `elif` chain handling
  three validation paths: range-based for `http_response`,
  `None` skip for `protocol_version`, list-based for all other columns
- `protocol_version` with `None` value skipped in validation — `None`
  represents legitimately absent HTTP version, not invalid
  content. Parser already decided the line is valid.
- `expected_values` in config now supports both list-based
  validation (method, protocol_version) and range-based validation
  (http_response)
- Deprecated 7 functions that were hardcoded to synthetic log
  columns (level, service, cpu, response_time)
- Retained `convert_corr_matrix()`, `select_col()`, and
  `get_metric_thresholds()` — all generic and format-independent

---

## Future Improvements (Planned)

- Full type validation for all data types (`str`, `datetime`)
- New analytical functions for CLF-specific metrics (status
  code distribution, endpoint frequency, request rate)
