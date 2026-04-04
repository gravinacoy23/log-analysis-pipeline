# Main — Implementation (v6)

## Objective

Implement the entry point for the log analysis pipeline.

The goal of this file is to:

- Configure logging for the entire application
- Accept runtime arguments from the user
- Load pipeline configuration once and pass it to all pipelines
- Call the pipeline orchestrators and return results

---

# System Context

`main.py` is the entry point of the application. It does not contain
business logic or pipeline logic — it is responsible for bootstrapping
the application, loading configuration, and delegating to the
appropriate pipelines.

```
user → main.py → load_config() → config dict
              → run_pipeline.py (receives config)
              → run_report_pipeline.py
              → run_features_pipeline.py (receives config)
              → run_statistical_pipeline.py
```

---

# File Location

```
main.py  (project root)
```

---

# Interface

## `main(service_name)`

Loads configuration, calls the data pipeline, the reporting
pipeline, the features pipeline, and the statistical pipeline
in sequence.

**Parameters:**
- `service_name` (str) — name of the service to analyze

**Returns:**
- `pd.DataFrame` — parsed log data as returned by `run_pipeline`

---

# Implementation Details

## Configuration Loading

`main()` loads the config once via `load_config()` and passes the
full config dict to each pipeline that needs it. This ensures:

- The config file is read once per execution, not once per pipeline
- Each pipeline receives what it needs without loading config
  independently
- Adding a new pipeline that needs config only requires passing
  the dict — no new `load_config()` calls

## Logging Configuration

Logging is configured using `logging.basicConfig()` before any other
call in the `if __name__` block. This ensures all loggers across the
application — including those in `log_parser.py` — inherit the same
configuration.

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

The format includes timestamp, module name, level, and message — enough
context to identify when and where an issue occurred. The level is set
to `INFO` to surface parsing statistics alongside warnings.

> Important: `logging.basicConfig()` is called before `argparse` and
> before any function that could trigger a log event. Order matters.

## Argument Parsing

Uses `argparse` to accept the service name from the command line:

```bash
python main.py -s booking
python main.py --service pricing
```

If no argument is provided, the default service is `booking`.

## Pipeline Coordination

`main()` coordinates pipelines in sequence:

1. `load_config()` — loads configuration once
2. `run_pipeline(service_name, config_data)` — ingestion, parsing,
   and DataFrame creation with computed columns
3. `run_report_pipeline(logs_dataframe)` — generates all visualizations
   and saves them to `output/plots/`
4. `run_features_pipeline(logs_dataframe, config_data)` — generates
   derived features and saves the dataset to `output/datasets/`
5. `run_statistical_pipeline()` — loads the feature dataset, performs
   train/test split, and saves splits to `output/datasets/`

The config dict is passed to pipelines that need it. The DataFrame
produced by the data pipeline is passed to both the reporting and
features pipelines. The statistical pipeline is self-contained — it
loads its input from disk because the feature dataset is already
persisted by step 4. `main()` does not modify or inspect any
intermediate results.

---

# Design Decisions

## Config loaded once in main, passed to pipelines
Previously each pipeline loaded config independently. Moving
`load_config()` to `main()` eliminates redundant file reads and
makes `main()` the single source of configuration for all pipelines.
This also makes it explicit which pipelines depend on config —
visible in the function signatures.

## Logging before everything else
`logging.basicConfig()` is the first call inside `if __name__`. This
guarantees no log event is emitted before the configuration is in place.

## main() is thin
`main()` does not contain pipeline logic. It loads config, calls
pipelines in sequence, and returns the DataFrame. Business logic
belongs in the pipeline layer, not in the entry point.

## argparse over hardcoded values
The service name is passed as a CLI argument rather than hardcoded.
This makes the pipeline reusable without modifying source code.

## Pipeline execution order matters
The statistical pipeline depends on the feature dataset existing on
disk. `main.py` guarantees the order: features pipeline runs before
statistical pipeline. If the order is violated, the statistical
pipeline raises a `ValueError` because the directory or file does
not exist.

---

# Changes from v5

- Added `run_statistical_pipeline()` as fourth pipeline call —
  loads feature dataset, performs train/test split, and persists
  splits to `output/datasets/`
- Imports `run_statistical_pipeline` from
  `pipelines.run_statistical_pipeline`
- `run_report_pipeline` renamed from `report_pipeline` for naming
  consistency with other pipelines (`run_pipeline`,
  `run_features_pipeline`, `run_statistical_pipeline`)
- System context and pipeline coordination updated to reflect
  four pipelines

---

# Changes from v4

- Added `run_features_pipeline(logs_dataframe, config_data)` as
  third pipeline call — generates feature dataset and persists
  to `output/datasets/features.csv`
- Imports `run_features_pipeline` from
  `pipelines.run_features_pipeline`
- System context and pipeline coordination updated to reflect
  three pipelines

---

# Future Improvements (Planned)

- Replace `logging.basicConfig()` with `logging.config.dictConfig()` for
  production-grade logging configuration — supports multiple handlers,
  log rotation, and environment-specific settings
- Support running multiple services in a single execution
- Add a `--output` argument to persist results to a file
