# Main — Implementation (v1)

## Objective

Implement the entry point for the log analysis pipeline.

The goal of this file is to:

- Configure logging for the entire application
- Accept runtime arguments from the user
- Call the pipeline orchestrator and return results

---

# System Context

`main.py` is the entry point of the application. It does not contain
business logic or pipeline logic — it is responsible for bootstrapping
the application and delegating to the appropriate pipeline.

```
user → main.py → run_pipeline.py → log_reader.py → log_parser.py
```

---

# File Location

```
main.py  (project root)
```

---

# Interface

## `main(service_name)`

Calls the pipeline orchestrator and returns the parsed log data.

**Parameters:**
- `service_name` (str) — name of the service to analyze

**Returns:**
- List of dicts — parsed log entries as returned by `run_pipeline`

---

# Implementation Details

## Logging Configuration

Logging is configured using `logging.basicConfig()` before any other
call in the `if __name__` block. This ensures all loggers across the
application — including those in `log_parser.py` — inherit the same
configuration.

```python
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

The format includes timestamp, module name, level, and message — enough
context to identify when and where an issue occurred.

> Important: `logging.basicConfig()` is called before `argparse` and
> before any function that could trigger a log event. Order matters.

## Argument Parsing

Uses `argparse` to accept the service name from the command line:

```bash
python main.py -s booking
python main.py --service pricing
```

If no argument is provided, the default service is `booking`.

---

# Design Decisions

## Logging before everything else
`logging.basicConfig()` is the first call inside `if __name__`. This
guarantees no log event is emitted before the configuration is in place.

## main() is thin
`main()` does not contain pipeline logic. It only calls `run_pipeline()`
and returns the result. Business logic belongs in the pipeline layer,
not in the entry point.

## argparse over hardcoded values
The service name is passed as a CLI argument rather than hardcoded.
This makes the pipeline reusable without modifying source code.

---

# Changes from v1
 
- `main()` no longer returns a DataFrame — it coordinates two pipelines
- `report_level_pipeline()` added as the second pipeline call
- `print(main(service_name))` removed — output is now saved to disk
  by the reporting pipeline
 
---

# Future Improvements (Planned)

- Replace `logging.basicConfig()` with `logging.config.dictConfig()` for
  production-grade logging configuration — supports multiple handlers,
  log rotation, and environment-specific settings
- Support running multiple services in a single execution
- Add a `--output` argument to persist results to a file
