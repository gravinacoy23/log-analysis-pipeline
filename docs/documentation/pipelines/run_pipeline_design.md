# Run Pipeline — Implementation (v2)

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
                           → log_parser.py (parsed logs)
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
1. load_config()                              → config dict
2. load_service_logs(service)                  → list of raw strings
3. parse_logs(raw_logs)                        → list of parsed dicts
4. convert_to_dataframe(parsed_logs, columns)  → validated DataFrame
```

The config is loaded once at the start and its values are passed to
the stages that need them. Currently, `convert_to_dataframe()` receives
the expected column names from the config for validation.

## Return Value

A validated pandas DataFrame is returned. The raw strings and parsed
dicts are intermediate steps not exposed to the caller.

---

# Design Decisions

## Config loaded once in the orchestrator
The pipeline loads `config.yaml` once via `config_loader.py` and passes
relevant values to each stage. This avoids modules reading config
independently and ensures the config file is only accessed once per
pipeline run.

## Orchestrator adapts between modules
The pipeline extracts `raw_data["columns"]` and passes it to
`convert_to_dataframe()`. The analysis layer does not know about
`config.yaml` — it only receives a list of expected column names.
This keeps the analysis layer decoupled from the config system.

## Single responsibility
`run_pipeline` orchestrates. It does not validate inputs, configure
logging, or handle CLI arguments. Each layer has one job.

## pipelines/ directory
The `pipelines/` directory is plural by design. As the project grows,
additional pipelines can be added here — for example a training pipeline
or a reporting pipeline — each with its own file and clear responsibility.

---

# Changes from v1

- Config loading added via `config_loader.py` — loaded once at the
  start of the pipeline
- `convert_to_dataframe()` now receives expected columns from config
- Variable names updated: `raw_logs` for reader output, `parsed_logs`
  for parser output
- Return type is now a validated `pd.DataFrame`, not a list of dicts

---

# Future Improvements (Planned)

- Accept a list of services and run the pipeline for each
- Support reading all log files for a service, not just the first
- Return pipeline metadata alongside results (lines processed, lines skipped)
