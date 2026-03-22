# Log Analysis Module — Design (v4)

## Objective

Provide the analytical layer of the pipeline.
Receives structured log data and converts it into a pandas DataFrame
ready for analysis and visualization. Validates that required columns
are present before creating the DataFrame. Supports computed columns
derived from config-driven thresholds and correlation analysis for
numeric metrics.

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

- `pd.DataFrame | pd.Series` — returns a Series when the column name
  is unique, returns a DataFrame if duplicate column names exist

### Implementation Details

- Uses standard pandas column selection with `df[column_name]`

### Design Decisions

- Return type is `pd.DataFrame | pd.Series` because pandas returns
  a DataFrame when multiple columns share the same name. In this
  pipeline, columns are validated by `_verify_columns()` so duplicates
  are not expected, but the type hint reflects what pandas actually does.

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

Each value represents the upper boundary of that bucket. The lower
boundary of the first bucket is derived from the data itself using
`.min()`.

### Design Decisions

- **Single generic function instead of one per metric.** The logic
  is identical for CPU and memory — only the thresholds differ. The
  thresholds come from config, not from the function. This avoids
  duplicating nearly identical functions and scales to any new numeric
  metric without code changes.

- **Config-driven thresholds.** Threshold values are externalized to
  `config.yaml` rather than hardcoded. This makes the classification
  adjustable without modifying code — important for when the generator
  evolves or the dataset characteristics change.

- **Mutates the DataFrame directly.** The function adds a column to
  the existing DataFrame instead of returning a new one. This is
  acceptable because the pipeline processes data in a linear chain —
  no other function depends on the DataFrame being in its pre-mutation
  state.

- **`pd.cut()` over manual `.loc[]` assignments.** An earlier
  implementation used three `.loc[]` calls with manual conditions.
  `pd.cut()` expresses the same logic in a single call, is less
  error-prone with boundary conditions, and is the idiomatic pandas
  approach for binning continuous data.

- **`.min()` as lower edge instead of hardcoded zero.** Using the
  actual minimum value from the data ensures the bins cover all
  values regardless of the metric's range. Hardcoding `0` would
  create an unnecessarily wide first bin and could misclassify values
  if a metric's range does not start at zero.

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
- Returns the resulting matrix as a DataFrame — rows and columns
  are the numeric column names, values are correlation coefficients
  ranging from -1 to 1

### Design Decisions

- **Lives in the analysis layer, not the visualizer.** Computing
  correlations is an analytical operation — it answers a question
  about the data. The visualizer only receives the result and draws
  it. This follows the same separation used throughout the pipeline:
  analysis calculates, visualizer draws, pipeline connects.

- **`select_dtypes` is called internally, not exposed as a separate
  function.** Selecting numeric columns is a utility step with no
  domain meaning — it is not an analytical question about the data.
  Functions like `count_by_level_all()` have business meaning;
  "select columns by type" does not. Keeping it internal avoids
  cluttering the public interface with generic pandas wrappers.

- **Pearson correlation.** The default and most common correlation
  method. Measures linear relationships between variables. Suitable
  for the current dataset where the CPU → response_time correlation
  was designed to be linear in the generator.

---

## Changes from v3

- Added `convert_corr_matrix()` — computes Pearson correlation matrix
  for all numeric columns using `select_dtypes` and `.corr()`
- Objective updated to reflect correlation analysis capability

---

## Future Improvements (Planned)

- Expand analytical functions to support a full dashboard with more
  metric combinations (e.g. mean memory by service, error rate over time)
