# Run Pipeline — Design (v8)

## Objective

Implement the pipeline orchestrator for the log analysis pipeline.

The goal of this file is to:

- Coordinate the ingestion, processing, and analysis layers
- Receive pipeline configuration from the caller
- Pass data and config between pipeline stages
- Return a validated DataFrame to the caller

---

# System Context

`run_pipeline.py` is the orchestration layer. It knows about the
pipeline stages and connects them together. It receives configuration
from `main.py` and passes relevant values to the modules that
require them.

```
main.py → load_config() → config dict
       → run_pipeline.py → log_reader.py (raw logs)
                         → log_parser.py (parsed + validated logs)
                         → log_analysis.py (fully validated DataFrame)
```

---

# File Location

```
pipelines/run_pipeline.py
```

---

# Interface

## `run_pipeline(raw_data)`

Orchestrates the full log ingestion, parsing, and analysis pipeline.

**Parameters:**
- `raw_data` (dict[str, Any]) — full config dict loaded by main.py

**Returns:**
- `pd.DataFrame` — validated DataFrame with parsed log data

---

# Implementation Details

## Pipeline Flow

```
1. extract log path from raw_data["paths"]["raw_log"]    → str
2. extract expected_columns from raw_data["columns"]     → dict[str, str]
3. extract column names via list(.keys())                → list[str]
4. extract expected_values from raw_data["expected_values"] → dict[str, list]
5. load_all_logs(log_path)                               → iterator of raw strings
6. parse_logs(raw_logs, column_names)                    → (list of parsed dicts, stats dict)
7. convert_to_dataframe(parsed_logs, expected_columns,
   expected_values)                                      → fully validated DataFrame
```

The config is received from `main.py` as a parameter. The pipeline
extracts and adapts config values for each stage:

- **Reader** receives the log directory path as a string from
  `raw_data["paths"]["raw_log"]`
- **Parser** receives `list[str]` of column names — for field
  mapping and presence validation per line. Returns a tuple: the
  parsed logs and a stats dict with lines_processed, skipped_lines,
  and skip_rate.
- **Analysis layer** receives two config-derived structures:
  - `expected_columns` (`dict[str, str]`) — column names mapped to
    types, used for column presence and dtype validation
  - `expected_values` (`dict[str, list]`) — column names mapped to
    valid values (lists for categorical, range for numeric)

## Return Value

A validated pandas DataFrame is returned. The raw strings and
parsed dicts are intermediate steps not exposed to the caller.

---

# Design Decisions

## Service parameter removed
The previous interface accepted a `service` string to select which
service directory to read. With the migration to real logs, the
per-service directory structure no longer exists. The reader now
receives a single directory path from config. The `service`
parameter was removed from the function signature.

## Config received from caller, not loaded internally
The config dict is received from `main.py`. This eliminates
redundant config loading when multiple pipelines need the same
config, and makes the dependency explicit in the function signature.

## Orchestrator adapts config format per stage
The pipeline extracts the log path for the reader, column names
as a `list[str]` for the parser, and passes the full columns dict
and expected values for the analysis layer. Each stage receives
only what it needs in the format it needs.

## Expected values from dedicated config key
Previously `expected_values` was built manually in the pipeline
from `raw_data["service"]` and `raw_data["level"]`. Now it comes
directly from `raw_data["expected_values"]` — a dedicated config
key that supports both list-based validation (method, protocol)
and range-based validation (http_response).

## Metric thresholds removed
The previous pipeline called `get_metric_thresholds()` for cpu
and mem columns. These columns do not exist in CLF logs. The
function is retained in `log_analysis.py` (generic) but is not
called by the pipeline until new thresholds are defined for
CLF-relevant metrics.

## Single responsibility
`run_pipeline` orchestrates. It does not validate inputs, configure
logging, load configuration, or handle CLI arguments.

---

# Deprecated (removed in v8)

| Element | Reason |
|---|---|
| `service` parameter | Per-service directory structure no longer exists |
| `get_metric_thresholds()` calls for cpu and mem | Columns do not exist in CLF |
| Manual `expected_values` construction from `service` and `level` keys | Replaced by dedicated `expected_values` config key |

---

# Changes from v7

- Removed `service` parameter from function signature — reader
  now receives log path from config
- Reader call changed from `load_service_logs(service)` to
  `load_all_logs(raw_data["paths"]["raw_log"])`
- `expected_values` now read directly from
  `raw_data["expected_values"]` instead of manually constructed
  from `service` and `level` keys
- Removed `get_metric_thresholds()` calls — cpu and mem columns
  do not exist in real logs
- Pipeline flow updated to reflect new reader interface and
  config structure

---

# Future Improvements (Planned)

- Surface parse_stats to the caller or to logs — the stats are
  available but not yet used by the pipeline beyond logging in
  the parser
