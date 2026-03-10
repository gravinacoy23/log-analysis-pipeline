# Session Context — Log Analysis Pipeline

## Current Status

**Month 1, Week 1 — Sprint completed.**
The base pipeline is fully functional end to end.

---

## What is Complete

### `scripts/log_generator.py` ✅
Synthetic log generator with argparse support.

Key design decisions:
- CPU influences `response_time` — realistic correlation for ML
- `determine_level()` uses thresholds + probabilities with `random.choices()`
- All constants live in `config/config.yaml` — loaded with `yaml.safe_load()`
- `load_config()` validates that keys exist and are not empty — fail fast
- Two separate timestamp functions: `generate_log_timestamp()` for log content, `generate_runtimestamp()` for filenames
- Number of logs configurable from CLI with `-c` / `--count`

### `src/ingestion/log_reader.py` ✅
Reads the first available log file for a given service.

Key design decisions:
- Receives service name as a string
- Returns a list of strings — one per log line
- Handles two errors with descriptive messages:
  - `ValueError` if the service directory does not exist
  - `FileNotFoundError` if the directory is empty

### `src/processing/log_parser.py` ✅
Transforms a list of strings into a list of dictionaries.

Key design decisions:
- `partition(" msg=")` isolates the msg field before splitting
- Type conversion with try/except — no hardcoded field names
- `strip('"\n')` cleans message of quotes and newlines
- Malformed lines are skipped with `logger.warning()` — pipeline does not crash
- `_parse_line()` as a private function — separation of responsibilities
- `None` as sentinel value for malformed lines

### `pipelines/run_pipeline.py` ✅
Pipeline orchestrator.

Key design decisions:
- Orchestration only — no business logic
- Calls reader → parser and returns only the final result
- `pipelines/` is plural by design — ready to scale

### `main.py` ✅
Application entry point.

Key design decisions:
- `logging.basicConfig()` is configured first — before argparse and before any function that logs
- Service configurable from CLI with `-s` / `--service`
- `main()` is thin — only calls `run_pipeline()` and returns the result

---

## Current Log Format

```
timestamp=2026-03-09T22:15:52Z service=booking user=15 cpu=35 mem=43 response_time=413 level=INFO msg="Booking failed"
```

All fields follow the `key=value` pattern — consistent and parseable.

---

## Project Structure

```
log-analysis-pipeline/
│
├── config/
│   └── config.yaml
├── data/
│   └── raw/
│       ├── shopping/
│       ├── pricing/
│       └── booking/
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── log_reader.py
│   ├── processing/
│   │   ├── __init__.py
│   │   └── log_parser.py
│   └── utils/
│       └── features.py
├── pipelines/
│   ├── __init__.py
│   └── run_pipeline.py
├── scripts/
│   └── log_generator.py
├── tests/
├── docs/
├── output/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Documentation Generated

- `docs/log_generator_design.md` — v2, includes argparse
- `docs/log_reader_design.md` — v1
- `docs/log_parser_design.md` — v1, includes implicit handling of malformed msg
- `docs/run_pipeline_design.md` — v1
- `docs/main_design.md` — v1

---

## What Comes Next — Week 2

- Convert the list of dicts into a pandas DataFrame
- Basic analysis operations: counts, groupings, filters
- First matplotlib visualization — bar plot of log levels
- Introduction to pandas data types

---

## Student Profile

- Works as Critical Incident Manager
- Learning environment: WSL + Vim
- Long-term goal: Data / ML Engineering
- Philosophy: depth over speed

---

## Assistant Rules (Scrum Master)

- Guide with questions, do not give solutions directly
- Provide code only when the student is genuinely stuck after trying
- Connect every task to the main project
- Prefer simple solutions
- Remind to commit and document every session
- Never recommend solutions that go against Python best practices, even if they are easier
