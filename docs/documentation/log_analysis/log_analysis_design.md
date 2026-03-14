# Log Analysis Module — Design (v2)

## Objective

Provide the analytical layer of the pipeline.
Receives structured log data and converts it into a pandas DataFrame
ready for analysis and visualization. Validates that required columns
are present before creating the DataFrame.

---

## Function: _verify_columns()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — list of strings with the required column names

### Returns

- None — raises an error if validation fails

### Implementation Details

- Checks that `log_dicts` is not empty — an empty list cannot produce
  a valid DataFrame
- Extracts column names from the first dict in the list using `.keys()`
- Iterates over `expected_columns` and raises a `ValueError` if any
  required column is missing

### Design Decisions

- **Private function.** Validation is an internal step of DataFrame
  creation, not part of the public interface. Callers use
  `convert_to_dataframe()` which handles validation internally.
- **Expected columns come from the caller, not from config.**
  `_verify_columns()` does not know about `config.yaml` — it receives
  the list of expected columns as a parameter. This keeps the analysis
  layer decoupled from the config system. The pipeline orchestrator is
  responsible for loading config and passing the columns.
- **Fail fast.** If a required column is missing, the function raises
  immediately with a descriptive message rather than letting pandas
  produce a confusing error downstream.

---

## Function: convert_to_dataframe()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line
- `expected_columns` — list of strings with the required column names

### Returns

- `pd.DataFrame` with one row per log entry and correct dtypes

### Implementation Details

- Calls `_verify_columns()` before creating the DataFrame
- DataFrame is created using `pd.DataFrame(log_dicts)`
- `timestamp` dtype is already `datetime` when it arrives — conversion
  is handled upstream in `log_parser.py`

### Design Decisions

- Validation happens before DataFrame creation — if columns are missing
  or the input is empty, no DataFrame is created
- `expected_columns` is passed by the pipeline orchestrator, which loads
  it from `config.yaml` via `config_loader.py`

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

### Design Decisions

- `.loc[]` was chosen over other filtering methods because it is explicit
  and idiomatic in pandas
- Index preservation is intentional — pandas default behavior that will
  be relevant in future analysis

---

## Function: select_col()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `column_name` — string with the name of the column to select

### Returns

- `pd.Series` containing the values of the selected column

### Implementation Details

- Uses standard pandas column selection with `df[column_name]`

### Design Decisions

- Returns a Series, not a DataFrame — a single column in pandas is
  always a Series, which is the 1D building block of a DataFrame
- Named `select_col()` instead of `filter_col()` because the operation
  selects structure, not filters rows by condition

---

## Function: count_by_level()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data
- `level` — string representing the log level to count (e.g. "INFO", "WARNING", "ERROR")

### Returns
- `int` — number of rows matching the given log level

### Implementation Details
- Uses a boolean condition `(df["level"] == level).sum()`
- `.sum()` counts `True` values in the boolean Series

### Design Decisions
- Preferred over `len(filter_loglevel())` because it avoids creating
  an intermediate filtered DataFrame — the count is computed directly
  on the boolean Series, which is more efficient and idiomatic in pandas

---

## Function: count_by_level_all()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.Series` — count of log entries per level, sorted by frequency

### Implementation Details
- Uses `df.value_counts("level")`
- Returns all levels in a single call

### Design Decisions
- Preferred over calling `count_by_level()` multiple times — one call
  returns the full distribution, which is more useful for analysis

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
- `.groupby()` returns a GroupBy object — the column is then selected
  and the aggregation applied in a single chain

### Design Decisions
- response_time by service is the most operationally relevant metric —
  it identifies which service is slowest under normal conditions

---

## Function: mean_cpu_by_level()

### Parameters
- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns
- `pd.Series` — mean CPU usage per log level

### Implementation Details
- Uses `.groupby("level")["cpu"].mean()`

### Design Decisions
- CPU by log level connects directly to the correlation designed in
  the log generator — ERROR and WARNING logs are expected to show
  higher CPU usage, which this function allows us to verify

---

## Changes from v1

- Added `_verify_columns()` — validates required columns before
  DataFrame creation
- `convert_to_dataframe()` now receives `expected_columns` as a
  second parameter, passed by the pipeline orchestrator
- Validation covers two cases: empty input list and missing columns
- Column names are config-driven — loaded from `config.yaml` by
  the pipeline, not hardcoded in the analysis layer

---

## Future Improvements (Planned)

- Expand analytical functions to support a full dashboard with more
  metric combinations (e.g. mean memory by service, error rate over time)
