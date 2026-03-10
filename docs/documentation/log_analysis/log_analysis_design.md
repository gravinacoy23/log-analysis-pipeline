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
