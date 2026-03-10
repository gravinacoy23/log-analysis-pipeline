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
