# Session Context — Log Analysis Pipeline

## Current Status

**Month 2 — In progress.**
Sprint 3 (Month 2 Week 1) complete. Sprint 4 (Month 2 Week 2) just started.
Currently practicing missing values (.isna(), .fillna(), .dropna()).

---

## What is Complete

### Month 1 — Fully Complete ✅
- Pipeline end to end
- All modules with Google style docstrings and type hints
- Code review: 14 refinement items (all P1 and P2 complete)
- Dockerfile and .dockerignore
- Pipeline runs inside Docker container
- 92+ commits

### Sprint 3 (Month 2 Week 1) — Complete ✅
- Docstrings and type hints across all modules
- Docker installed in WSL, Dockerfile working
- Reader upgrade: reads all files per service
- Reader upgrade: reads all services (load_all_logs)
- Generated 1996 row dataset
- Pandas intermediate: .describe(), .info()
- Computed columns: cpu_bucket and mem_bucket via pd.cut()
- Config-driven thresholds in config.yaml
- Sprint checkpoint: 6/6

### Sprint 4 (Month 2 Week 2) — Just Started
- Missing values practice: .isna() started, .fillna() and .dropna() next
- Remaining: seaborn intro, 4+ visualizations, data quality checks,
  generalize reporting pipeline, Docker volume mounts

---

## Pipeline — End to End

```
log_generator.py → data/raw/ → log_reader.py → log_parser.py → log_analysis.py → DataFrame
                                                                                → run_reporting_pipeline.py → output/plots/
```

Orchestrated by run_pipeline.py and main.py.

---

## Current Module Status

### `scripts/log_generator.py` ✅ (v3)
- Config-driven, lifecycle-managed file handles
- CPU → response_time → level correlation
- All helpers private, docstrings and type hints complete

### `src/ingestion/log_reader.py` ✅ (v2, upgraded)
- `load_service_logs(service)` — reads all files for one service, yields lines
- `load_all_logs(services)` — reads all files across all services, yields lines
- `_load_all_path_names(services)` — builds paths from service names
- `_load_all_files(paths)` — collects and sorts all files
- No validation needed in load_all_logs — services come from config

### `src/processing/log_parser.py` ✅ (v2)
- Guard clauses, isdigit(), partition for msg field
- Returns list of dicts

### `src/analysis/log_analysis.py` ✅ (v3)
- `_verify_columns()` — validates before DataFrame creation
- `convert_to_dataframe()` — config-driven column validation
- `get_metric_thresholds()` — pd.cut() with config-driven thresholds
- Analysis functions: filter, select, count, mean by service/level
- Mutates DataFrame directly (acceptable for linear pipeline)

### `src/analysis/log_visualizer.py` ✅ (v1)
- `plot_metric()` — generic bar plot, dict-based, decoupled from pandas

### `src/config_loader.py` ✅ (v1)
- Independent from generator's _load_config()

### `pipelines/run_pipeline.py` ✅ (v3)
- Loads config, runs reader → parser → DataFrame → metric thresholds
- Calls get_metric_thresholds for cpu and mem

### `pipelines/run_reporting_pipeline.py` ✅ (v1)
- report_level_pipeline() — hardcoded to level counts
- Needs generalization in Sprint 4

### `main.py` ✅ (v2)
- Thin entry point, argparse, logging config

---

## Config Structure (current)

```yaml
services: [shopping, pricing, booking]
messages: {shopping: [...], pricing: [...], booking: [...]}
levels: [INFO, WARNING, ERROR]
columns: [timestamp, service, user, cpu, mem, response_time, level, msg]
metric_thresholds:
  cpu:
    low: 44
    normal: 57
    high: 70
  mem:
    low: 52
    normal: 63
    high: 75
```

---

## Key Concepts Learned

### Month 1
- yield and generators — lazy iteration, duck typing
- Guard clauses and early return pattern
- Config-driven validation
- File handle lifecycle management
- Type hints (PEP 484) and Google style docstrings
- Module decoupling — visualizer independent from pandas
- Figure/axes separation in matplotlib

### Month 2 (so far)
- pd.cut() for binning continuous data into categories
- .loc[] with two arguments (rows, column) for conditional assignment
- include_lowest parameter for boundary handling
- Generator code doesn't execute until iterated
- Docker fundamentals: images, containers, Dockerfile, RUN vs CMD
- .isna() treats None and NaN as equivalent

---

## Documentation Status

- `docs/log_generator_design.md` — v3
- `docs/log_reader_design.md` — v2 (multi-file)
- `docs/log_parser_design.md` — v2
- `docs/run_pipeline_design.md` — v2
- `docs/main_design.md` — v2
- `docs/log_analysis_design.md` — v3 (with get_metric_thresholds)
- `docs/log_visualizer_design.md` — v1
- `docs/run_reporting_pipeline_design.md` — v1
- `docs/config_loader_design.md` — v1
- `docs/docker_design.md` — v1
- `docs/tech_debt.md` — updated (reader items completed)
- `docs/bugs.md` — 14 items tracked

---

## Sprint 4 Plan (Month 2 Week 2)

1. Missing values: .isna(), .fillna(), .dropna() — IN PROGRESS
2. Seaborn introduction: countplot, histplot, heatmap
3. 4+ visualizations saved to output/plots/
4. Data quality checks in analysis layer
5. Generalize reporting pipeline for multiple report types
6. Docker volume mounts for output persistence

---

## Tech Debt Status

### Recently Completed
- Reader: read all files per service ✅
- Reader: read all services ✅

### Active for Month 2
- Parser: validate all expected fields present
- Parser: return parsing statistics
- Reporting pipeline: generalize for multiple report types
- Main: support multiple services
- Main: add --output argument
- Analysis: expand metric combinations

---

## Working Agreements

- Claude writes design docs, user reviews them
- User writes docstrings themselves
- Sprint checkpoints with quiz questions at end of each sprint
- Push back when user is wrong — don't agree to avoid conflict
- Push back gently when user asks before trying
- OOP: introduce when state + behavior need to live together (likely Month 8-9)
