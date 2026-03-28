# Run Pipeline — Implementation (v7)

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

## `run_pipeline(service, raw_data)`

Orchestrates the full log ingestion, parsing, and analysis pipeline
for a given service.

**Parameters:**
- `service` (str) — name of the service to process (e.g. `"booking"`)
- `raw_data` (dict[str, Any]) — full config dict loaded by main.py

**Returns:**
- `pd.DataFrame` — validated DataFrame with parsed log data

---

# Implementation Details

## Pipeline Flow

```
1. extract expected_columns from raw_data["columns"]       → dict[str, str]
2. extract column names via list(.keys())                   → list[str]
3. build expected_values from raw_data["service"] and
   raw_data["level"]                                        → dict[str, list[str]]
4. load_service_logs(service)                               → iterator of raw strings
5. parse_logs(raw_logs, column_names)                       → (list of parsed dicts, stats dict)
6. convert_to_dataframe(parsed_logs, expected_columns,
   expected_values)                                         → fully validated DataFrame
7. get_metric_thresholds(df, "cpu", thresholds)             → mutates DataFrame
8. get_metric_thresholds(df, "mem", thresholds)             → mutates DataFrame
```

The config is received from `main.py` as a parameter. The pipeline
extracts and adapts config values for each stage:

- **Parser** receives `list[str]` of column names — for field
  presence validation per line. Returns a tuple: the parsed logs
  and a stats dict with lines_processed, skipped_lines, and
  skip_rate. The pipeline unpacks both; `parse_stats` is available
  for future use.
- **Analysis layer** receives two config-derived structures:
  - `expected_columns` (`dict[str, str]`) — column names mapped to
    types, used for column presence and dtype validation
  - `expected_values` (`dict[str, list[str]]`) — categorical column
    names mapped to valid values, used for content validation

## Expected Values Construction

The pipeline builds `expected_values` from existing config keys:

```python
expected_values = {
    "service": raw_data["service"],
    "level": raw_data["level"],
}
```

The keys match the DataFrame column names (`"service"`, `"level"`),
which allows the analysis layer to validate generically without
hardcoding column names. The values are the lists of valid options
already defined in the config for the generator.

## Return Value

A validated pandas DataFrame is returned with computed columns
(`cpu_bucket`, `mem_bucket`). The raw strings and parsed dicts are
intermediate steps not exposed to the caller.

---

# Design Decisions

## Config received from caller, not loaded internally
Previously `run_pipeline` loaded config independently via
`load_config()`. Now it receives the config dict from `main.py`.
This eliminates redundant config loading when multiple pipelines
need the same config, and makes the dependency explicit in the
function signature.

## Orchestrator adapts config format per stage
The pipeline extracts column names as a `list[str]` for the parser,
passes the full columns dict for type validation, and builds a
separate `expected_values` dict for content validation. Each stage
receives only what it needs in the format it needs — no module knows
how the config is structured internally.

## Expected values reuse existing config keys
The `service` and `level` lists in the config are the same lists the
generator uses to produce logs. Reusing them for validation ensures
the pipeline validates against the same values the generator produces,
keeping the system consistent without duplicating configuration.

## Config key names match DataFrame column names
The config keys `service` and `level` (renamed from `services` and
`levels` in v4) match the DataFrame column names exactly. This allows
the analysis layer to use config keys directly as column references
without needing a mapping layer.

## Single responsibility
`run_pipeline` orchestrates. It does not validate inputs, configure
logging, load configuration, or handle CLI arguments. Each layer has
one job.

## pipelines/ directory
The `pipelines/` directory is plural by design. As the project grows,
additional pipelines can be added here — for example a training pipeline
or a feature pipeline — each with its own file and clear responsibility.

---

# Changes from v6

- `parse_logs` return value unpacked as tuple:
  `parsed_logs, parse_stats = parse_logs(...)` — stats dict
  available for future pipeline metadata reporting
- Pipeline flow updated to reflect tuple return from parser

---

# Changes from v5

- `load_config()` removed — config is now received as `raw_data`
  parameter from `main.py`
- `load_config` import removed from the module
- Function signature updated: `run_pipeline(service, raw_data)`
- Pipeline flow updated to reflect that config extraction happens
  from the received dict, not from a local load
- System context diagram updated to show config flowing from main

---

# Future Improvements (Planned)

- Accept a list of services and run the pipeline for each
- Surface parse_stats to the caller or to logs — the stats are
  available but not yet used by the pipeline beyond logging in
  the parser
