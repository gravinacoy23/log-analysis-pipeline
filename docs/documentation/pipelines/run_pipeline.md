# Run Pipeline — Implementation (v1)

## Objective

Implement the pipeline orchestrator for the log analysis pipeline.

The goal of this file is to:

- Coordinate the ingestion and processing layers
- Pass data between reader and parser
- Return structured log data to the caller

---

# System Context

`run_pipeline.py` is the orchestration layer. It knows about the
pipeline stages and connects them together. It does not know about
application configuration, CLI arguments, or logging setup — those
are the responsibility of `main.py`.

```
main.py → run_pipeline.py → log_reader.py → log_parser.py
```

---

# File Location

```
pipelines/run_pipeline.py
```

---

# Interface

## `run_pipeline(service)`

Orchestrates the full log ingestion and parsing pipeline for a given service.

**Parameters:**
- `service` (str) — name of the service to process (e.g. `"booking"`)

**Returns:**
- List of dicts — parsed log entries ready for analysis

---

# Implementation Details

## Pipeline Flow

```
1. load_service_logs(service)  → list of raw strings
2. parse_logs(logs_list)       → list of dicts
3. return logs_dict
```

The raw strings returned by the reader are passed directly to the parser.
`run_pipeline` does not inspect or transform the data between stages.

## Return Value

Only the parsed result is returned — the raw strings are an intermediate
step and are not exposed to the caller.

---

# Design Decisions

## Single responsibility
`run_pipeline` only orchestrates. It does not validate inputs, configure
logging, or handle CLI arguments. Each layer has one job.

## Thin orchestrator
The function is intentionally simple — it connects the reader and parser
without adding logic. Complexity lives in the individual modules.

## pipelines/ directory
The `pipelines/` directory is plural by design. As the project grows,
additional pipelines can be added here — for example a training pipeline
or a reporting pipeline — each with its own file and clear responsibility.

---

# Future Improvements (Planned)

- Accept a list of services and run the pipeline for each
- Support reading all log files for a service, not just the first
- Return pipeline metadata alongside results (lines processed, lines skipped)
- Add a reporting or persistence step after parsing
