# Log Analysis Module — Design (v1)

## Objective

Provide the analytical layer of the pipeline.
Receives structured log data and converts it into a pandas DataFrame
ready for analysis and visualization.

---

## Function: convert_to_dataframe()

### Parameters

- `log_dicts` — list of dictionaries, one per parsed log line

### Returns

- `pd.DataFrame` with one row per log entry and correct dtypes

### Implementation Details

- DataFrame is created using `pd.DataFrame(log_dicts)`
- `timestamp` column is converted using `pd.to_datetime()`, which
  correctly parses the UTC timestamp and assigns dtype `datetime64[us, UTC]`

### Design Decisions

- Type conversion is handled inside this function, not in the parser.
  The parser is responsible for structure, not for analysis-ready types.
- `timestamp` is converted to datetime because time-based analysis
  (grouping by hour, filtering by range) requires a proper datetime dtype,
  not a string.

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

## Future Improvements (Planned)

- Expand analytical functions to support a full dashboard with more
  metric combinations (e.g. mean memory by service, error rate over time)
