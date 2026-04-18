# Main — Implementation (v7)

## Objective

Implement the entry point for the log analysis pipeline.

The goal of this file is to:

- Configure logging for the entire application
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
```

Temporarily disabled (pending Month 6 Weeks 2–3):
```
              → run_features_pipeline.py (feature redesign)
              → run_statistical_pipeline.py (depends on features)
```

---

# File Location

```
main.py  (project root)
```

---

# Interface

## `main()`

Loads configuration, calls the data pipeline and the reporting
pipeline in sequence, and returns the DataFrame.

**Parameters:**
- None

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

## Pipeline Coordination

`main()` coordinates pipelines in sequence:

1. `load_config()` — loads configuration once
2. `run_pipeline(config_data)` — ingestion, parsing, DataFrame
   creation with computed columns (including response_size_bucket)
3. `run_report_pipeline(logs_dataframe)` — generates all
   visualizations and saves them to `output/plots/`

Temporarily disabled pending Month 6 adaptation:

4. `run_features_pipeline(logs_dataframe, config_data)` — feature
   engineering redesign for CLF domain (Week 2)
5. `run_statistical_pipeline()` — depends on new feature dataset
   (Week 3)

The config dict is passed to pipelines that need it. The DataFrame
produced by the data pipeline is passed to the reporting pipeline.
`main()` does not modify or inspect any intermediate results.

---

# Design Decisions

## Service argument removed
The previous interface accepted a `--service` CLI argument to
select which service directory to read. With the migration to real
NASA HTTP access logs, the per-service directory structure no longer
exists. The reader now receives a single directory path from config.
The `argparse` definition remains in the `__main__` block for future
use but the `--service` argument has been removed.

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

## Downstream pipelines temporarily disabled
The features and statistical pipelines are commented out because
they reference synthetic log columns that no longer exist. They
will be re-enabled after redesign in Month 6 Weeks 2–3. The
imports remain in the file to make re-enabling straightforward.

## Pipeline execution order matters
When all pipelines are active, the statistical pipeline depends on
the feature dataset existing on disk. `main.py` guarantees the
order: features pipeline runs before statistical pipeline. If the
order is violated, the statistical pipeline raises a `ValueError`
because the directory or file does not exist.

---

# Changes from v6

- Removed `service_name` parameter from `main()` — function now
  takes no arguments
- Removed `--service` / `-s` CLI argument from argparse — the
  per-service directory structure no longer exists
- `run_report_pipeline()` re-enabled — reporting pipeline updated
  with CLF column names (method, http_response, response_size)
- `run_features_pipeline()` and `run_statistical_pipeline()` remain
  commented out — pending feature engineering redesign in Month 6
  Weeks 2–3
- System context updated to show active vs temporarily disabled
  pipelines
- Pipeline coordination updated to reflect 2 active pipelines
  and 2 pending

---

# Future Improvements (Planned)

- Re-enable features and statistical pipelines after Month 6
  redesign
- Replace `logging.basicConfig()` with `logging.config.dictConfig()`
  for production-grade logging configuration — supports multiple
  handlers, log rotation, and environment-specific settings
- Add a `--output` argument to persist results to a file
