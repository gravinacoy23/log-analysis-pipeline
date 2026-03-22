# Run Pipeline — Implementation (v3)

## Objective

Implement the pipeline orchestrator for the log analysis pipeline.

The goal of this file is to:

- Coordinate the ingestion, processing, and analysis layers
- Load pipeline configuration
- Pass data and config between pipeline stages
- Return a validated DataFrame to the caller

---

# System Context

`run_pipeline.py` is the orchestration layer. It knows about the
pipeline stages and connects them together. It loads configuration
that the pipeline needs and passes it to the modules that require it.

```
main.py → run_pipeline.py → config_loader.py (config)
                           → log_reader.py (raw logs)
                           → log_parser.py (parsed + validated logs)
                           → log_analysis.py (validated DataFrame)
```

---

# File Location

```
pipelines/run_pipeline.py
```

---

# Interface

## `run_pipeline(service)`

Orchestrates the full log ingestion, parsing, and analysis pipeline
for a given service.

**Parameters:**
- `service` (str) — name of the service to process (e.g. `"booking"`)

**Returns:**
- `pd.DataFrame` — validated DataFrame with parsed log data

---

# Implementation Details

## Pipeline Flow

```
1. load_config()                                    → config dict
2. load_service_logs(service)                       → iterator of raw strings
3. parse_logs(raw_logs, config["columns"])           → list of parsed dicts
4. convert_to_dataframe(parsed_logs, config["columns"]) → validated DataFrame
5. get_metric_thresholds(df, "cpu", thresholds)     → mutates DataFrame
6. get_metric_thresholds(df, "mem", thresholds)     → mutates DataFrame
```

The config is loaded once at the start and its values are passed to
the stages that need them. Both `parse_logs()` and
`convert_to_dataframe()` receive the expected column names from the
config for validation — the parser validates per line, the analysis
layer validates the complete list.

## Return Value

A validated pandas DataFrame is returned with computed columns
(`cpu_bucket`, `mem_bucket`). The raw strings and parsed dicts are
intermediate steps not exposed to the caller.

---

# Design Decisions

## Config loaded once in the orchestrator
The pipeline loads `config.yaml` once via `config_loader.py` and passes
relevant values to each stage. This avoids modules reading config
independently and ensures the config file is only accessed once per
pipeline run.

## Orchestrator adapts between modules
The pipeline extracts `raw_data["columns"]` and passes it to both
`parse_logs()` and `convert_to_dataframe()`. Neither the parser nor
the analysis layer knows about `config.yaml` — they only receive
the list of expected column names. This keeps both layers decoupled
from the config system.

## Config passed to two stages is not redundant
The parser uses the column list to validate each line individually —
rejecting lines with missing fields before they enter the result list.
The analysis layer uses the same list to validate the complete result —
catching the case where all lines are rejected and the list is empty.
Each stage validates at its own level.

## Single responsibility
`run_pipeline` orchestrates. It does not validate inputs, configure
logging, or handle CLI arguments. Each layer has one job.

## pipelines/ directory
The `pipelines/` directory is plural by design. As the project grows,
additional pipelines can be added here — for example a training pipeline
or a reporting pipeline — each with its own file and clear responsibility.

---

# Changes from v2

- `parse_logs()` now receives `raw_data["columns"]` as a second
  parameter — the parser uses this to validate that each parsed line
  contains all expected fields before accepting it
- Pipeline flow updated to reflect both parser and analysis layer
  receiving the expected columns list
- `get_metric_thresholds()` calls documented in the pipeline flow —
  computed columns for cpu and mem added after DataFrame creation

---

# Future Improvements (Planned)

- Accept a list of services and run the pipeline for each
- Return pipeline metadata alongside results (lines processed, lines skipped)
