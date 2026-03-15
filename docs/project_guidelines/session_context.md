# Session Context — Log Analysis Pipeline

## Current Status

**Month 1 — Closing out.**
Week 2 complete. Refactoring complete (P1s and P2s resolved, P3s mostly resolved).
Pending: docstrings/type hints (in progress, generator done), Docker intro.

---

## What is Complete

### Pipeline — End to End ✅
```
log_generator.py → data/raw/ → log_reader.py → log_parser.py → log_analysis.py → DataFrame
                                                                                → run_reporting_pipeline.py → output/plots/
```

### `scripts/log_generator.py` ✅ (v3, heavily refactored)
- `generate_logs()` — public orchestrator, manages full lifecycle
- `_generator_loop()` — separated from orchestrator, only generates
- `_load_config()` — returns dict instead of tuple, validates with `.get()`
- `_create_files()` / `_write_log()` / `_close_files()` — lifecycle-managed file handles (dict keyed by service name)
- `_determine_level()` parameter renamed from `messages` to `levels`
- Config key renamed from `message_type` to `levels`
- All helper functions prefixed with `_` (private)
- Docstrings and type hints added (Google style)

### `src/ingestion/log_reader.py` ✅ (refactored)
- `load_service_logs()` — now uses `yield` instead of `readlines()` (lazy iteration)
- File selection order fixed with `log_files.sort()` (deterministic)
- Returns an `Iterator[str]` instead of `list[str]`

### `src/processing/log_parser.py` ✅ (refactored)
- `_parse_logs_without_message()` renamed to `_parse_fields()`
- `splitted_log` renamed to `split_log`
- Guard clause (`len < 2`) replaced `IndexError` exception for malformed lines
- `str.isdigit()` replaced `try int() / except ValueError` for type detection
- Guard clause separated from type detection logic

### `src/analysis/log_analysis.py` ✅ (refactored)
- `_verify_columns()` added — validates required columns before DataFrame creation
- `convert_to_dataframe()` now receives `expected_columns` from pipeline
- Column names are config-driven (loaded from `config.yaml`)
- Validates empty input list and missing columns

### `src/analysis/log_visualizer.py` ✅ (new)
- `plot_metric(metric_dict, metric_name)` — generic bar plot function
- Receives dict (decoupled from pandas)
- Returns `matplotlib.figure.Figure` (does not save or display)
- Uses explicit `fig, ax = plt.subplots()`

### `src/config_loader.py` ✅ (new)
- `load_config()` — shared config loader for the pipeline side
- Validates that `columns` key exists
- Independent from generator's `_load_config()`
- Returns full config dict

### `pipelines/run_pipeline.py` ✅ (refactored)
- Loads config via `config_loader.py`
- Passes expected columns to `convert_to_dataframe()`
- Variable names updated: `raw_logs`, `parsed_logs`

### `pipelines/run_reporting_pipeline.py` ✅ (new)
- `report_level_pipeline()` — specific to level counts
- Converts Series to dict via `.to_dict()`
- Saves figure to `output/plots/level_plot.png`
- `make_output_directory()` creates `output/plots/`

### `main.py` ✅ (updated to v2)
- Calls `run_pipeline()` then `report_level_pipeline()`
- No longer prints DataFrame to stdout
- Remains thin — no business logic

---

## Refactoring Status (code_refinements.md)

### P1 — All Complete ✅
- #1 — log_reader: deterministic file order (sort)
- #2 — log_parser: function renamed to `_parse_fields`
- #3 — log_parser: `splitted_log` → `split_log`

### P2 — All Complete ✅
- #4 — log_generator: `load_config()` returns dict
- #5 — log_generator: parameter renamed to `levels`
- #6 — log_generator: `generate_logs()` split into orchestrator + loop
- #7 — run_pipeline: variable names updated
- #8 — log_parser: guard clause + `isdigit()` replaces exceptions

### P3 — Mostly Complete
- #9 — log_generator: file handle lifecycle ✅
- #10 — log_analysis: column validation added ✅
- #11 — log_reader: `yield` replaces `readlines()` ✅
- #12 — log_analysis: hardcoded test data — deferred to when tests exist
- #13 — main: print removed ✅ (resolved by reporting pipeline)
- #14 — docstrings and type hints — IN PROGRESS (generator done, rest pending)

---

## Documentation Status

- `docs/log_generator_design.md` — v3
- `docs/log_reader_design.md` — v1, updated with yield and sort
- `docs/log_parser_design.md` — v2
- `docs/run_pipeline_design.md` — v2
- `docs/main_design.md` — v2
- `docs/log_analysis_design.md` — v2
- `docs/log_visualizer_design.md` — v1
- `docs/run_reporting_pipeline_design.md` — v1
- `docs/config_loader_design.md` — v1
- `docs/tech_debt.md` — v1, updated with reporting pipeline item
- `docs/code_refinements.md` — v1, 14 items tracked

---

## Current Log Format

```
timestamp=2026-03-09T22:15:52Z service=booking user=15 cpu=35 mem=43 response_time=413 level=INFO msg="Booking failed"
```

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
│   ├── config_loader.py          ← new
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── log_reader.py
│   ├── processing/
│   │   ├── __init__.py
│   │   └── log_parser.py
│   └── analysis/
│       ├── __init__.py
│       ├── log_analysis.py
│       └── log_visualizer.py
├── pipelines/
│   ├── __init__.py
│   ├── run_pipeline.py
│   └── run_reporting_pipeline.py
├── scripts/
│   └── log_generator.py
├── tests/
├── docs/
├── output/
│   └── plots/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## What Comes Next

### Immediate (before Month 2)
- Finish docstrings and type hints across all modules (parser, reader, analysis, pipelines, main, config_loader)
- Docker intro — Dockerfile, run pipeline in container
- Commit and push all pending work

### Month 2 Week 1
- See `week1_month2.md`

---

## Key Concepts Learned This Sprint

- `yield` and generators — lazy iteration, duck typing
- Guard clauses and early return pattern
- Config-driven validation
- File handle lifecycle management
- Type hints (PEP 484) and Google style docstrings
- `dict` vs `tuple` for flexible return types
- Module decoupling — visualizer independent from pandas
- Figure/axes separation in matplotlib

---

## Student Profile

- Works as Critical Incident Manager
- Learning environment: WSL + Vim + Pyright
- Long-term goal: Data / ML Engineering
- Philosophy: depth over speed

---

## Assistant Rules (Scrum Master)

- Guide with questions, do not give solutions directly
- Provide code only when the student is genuinely stuck after trying
- Connect every task to the main project
- Prefer simple solutions
- Remind to commit and document every session
- Never recommend solutions that go against Python best practices
- Quick code review after each module or major refactor
- Full code review at end of each sprint (weekly)
