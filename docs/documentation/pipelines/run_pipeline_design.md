# Run Pipeline — Implementation (v5)

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
                           → log_analysis.py (fully validated DataFrame)
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
2. extract expected_columns from config["columns"]       → dict[str, str]
3. extract column names via list(.keys())                → list[str]
4. build expected_values from config["service"] and
   config["level"]                                       → dict[str, list[str]]
5. load_service_logs(service)                            → iterator of raw strings
6. parse_logs(raw_logs, column_names)                    → list of parsed dicts
7. convert_to_dataframe(parsed_logs, expected_columns,
   expected_values)                                      → fully validated DataFrame
8. get_metric_thresholds(df, "cpu", thresholds)          → mutates DataFrame
9. get_metric_thresholds(df, "mem", thresholds)          → mutates DataFrame
```

The config is loaded once at the start. The pipeline extracts and
adapts config values for each stage:

- **Parser** receives `list[str]` of column names — for field
  presence validation per line
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

## Config loaded once in the orchestrator
The pipeline loads `config.yaml` once via `config_loader.py` and passes
relevant values to each stage. This avoids modules reading config
independently and ensures the config file is only accessed once per
pipeline run.

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
logging, or handle CLI arguments. Each layer has one job.

## pipelines/ directory
The `pipelines/` directory is plural by design. As the project grows,
additional pipelines can be added here — for example a training pipeline
or a reporting pipeline — each with its own file and clear responsibility.

---

# Changes from v4

- `expected_values` dict constructed from `raw_data["service"]` and
  `raw_data["level"]` — maps categorical column names to valid values
- `convert_to_dataframe()` now receives three parameters:
  `parsed_logs`, `expected_columns`, and `expected_values`
- Pipeline flow updated to reflect the construction and passing of
  `expected_values` for categorical content validation

---

# Future Improvements (Planned)

- Accept a list of services and run the pipeline for each
- Return pipeline metadata alongside results (lines processed, lines skipped)
