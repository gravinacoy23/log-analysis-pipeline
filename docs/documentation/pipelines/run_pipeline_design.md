# Run Pipeline — Implementation (v4)

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
                           → log_analysis.py (type-validated DataFrame)
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
1. load_config()                                         → config dict
2. extract expected_columns from config["columns"].keys() → list[str]
3. load_service_logs(service)                            → iterator of raw strings
4. parse_logs(raw_logs, expected_columns)                → list of parsed dicts
5. convert_to_dataframe(parsed_logs, config["columns"])  → type-validated DataFrame
6. get_metric_thresholds(df, "cpu", thresholds)          → mutates DataFrame
7. get_metric_thresholds(df, "mem", thresholds)          → mutates DataFrame
```

The config is loaded once at the start and its values are passed to
the stages that need them. The `columns` config is a dict mapping
column names to expected types. The pipeline extracts what each stage
needs:

- **Parser** receives `list[str]` of column names — extracted via
  `list(config["columns"].keys())`. The parser validates field
  presence per line but does not need type information.
- **Analysis layer** receives the full `dict[str, str]` — it uses
  the keys for column presence validation and the values for data
  type validation.

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

## Orchestrator adapts config format per stage
The pipeline extracts column names as a `list[str]` for the parser
and passes the full columns dict to the analysis layer. Each stage
receives only what it needs in the format it needs — neither module
knows how the config is structured internally.

## Config passed to two stages is not redundant
The parser uses column names to validate each line individually —
rejecting lines with missing fields before they enter the result list.
The analysis layer uses the full dict to validate column presence on
the complete result and to verify that numeric columns contain the
correct data types. Each stage validates at its own level.

## Single responsibility
`run_pipeline` orchestrates. It does not validate inputs, configure
logging, or handle CLI arguments. Each layer has one job.

## pipelines/ directory
The `pipelines/` directory is plural by design. As the project grows,
additional pipelines can be added here — for example a training pipeline
or a reporting pipeline — each with its own file and clear responsibility.

---

# Changes from v3

- `config["columns"]` is now a dict mapping names to types — the
  pipeline extracts column names via `list(.keys())` for the parser
  and passes the full dict to the analysis layer
- `convert_to_dataframe()` now receives the columns dict instead of
  a list — enables data type validation inside the analysis layer
- Pipeline flow updated to reflect the extraction step and the
  different formats passed to each stage

---

# Future Improvements (Planned)

- Accept a list of services and run the pipeline for each
- Return pipeline metadata alongside results (lines processed, lines skipped)
