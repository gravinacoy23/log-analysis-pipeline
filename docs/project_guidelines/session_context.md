# Session Context — Log Analysis Pipeline

## Current Status

**Month 3 — Complete.**
Sprint 5 (Month 3 Week 1) and Sprint 6 (Month 3 Week 2) complete.
Month 4 ready to begin.

---

## What is Complete

### Month 1 — Fully Complete ✅
- Pipeline end to end
- All modules with Google style docstrings and type hints
- Code review: 14 refinement items (all P1 and P2 complete)
- Dockerfile and .dockerignore
- Pipeline runs inside Docker container
- 92+ commits

### Month 2 — Fully Complete ✅
- Pandas intermediate: groupby, aggregation, computed columns
- Data quality checks at two layers (parser and analysis)
- Validation orchestrator with single-loop architecture
- Seaborn visualizations: countplot, histplot, heatmap
- Generalized reporting pipeline with dict collector pattern
- Config-driven thresholds for metric bucketing
- Docker volume mounts for output persistence
- Missing values handling: .isna(), .fillna(), .dropna()

### Sprint 5 (Month 3 Week 1) — Complete ✅
- Feature engineering module with 5 derived features
- Config-driven thresholds for features
- Feature dataset persisted to `output/datasets/features.csv`
- Features pipeline integrated into `main.py`
- Parser statistics with tuple return and `_skip_report()`
- Config loader refactored: loop-based validation of 5 required keys
- `load_config()` moved from `run_pipeline` to `main.py`
- Logging level changed to INFO for observability
- Sprint checkpoint: 9.5/10

### Sprint 6 (Month 3 Week 2) — Complete ✅
- Bash script `scripts/run_daily.sh` with:
  - Portable shebang (`#!/usr/bin/env bash`)
  - `set -e` for exit on failure
  - Portable root navigation via `cd "$(dirname "$0")/.."`
  - `mkdir -p logs/` for execution log directory
  - Conda environment activation via `source`
  - UTC-timestamped execution log files
  - `&>>` for stdout+stderr redirection
- Cron job configured for scheduled execution
- Generator: memory as second factor for response_time (config-driven)
- Generator: peak vs off-peak hour simulation (24 weighted hours)
- Generator: large-scale generation verified (scales without issues)
- Generator reorganized for top-down readability
- Sprint checkpoint: 8/10

---

## Pipeline — End to End

```
log_generator.py → data/raw/<service>/
    → log_reader.py (lazy iteration via generators)
    → log_parser.py (guard clauses, field validation, stats)
    → log_analysis.py (validation orchestrator, DataFrame creation)
    → run_reporting_pipeline.py → output/plots/
    → feature_engineering.py → run_features_pipeline.py → output/datasets/features.csv
```

Orchestrated by `run_pipeline.py` and `main.py`.
Configuration loaded once in `main.py`, passed to all pipelines.
Automated via `scripts/run_daily.sh` + cron.

---

## Current Module Status

### `scripts/log_generator.py` ✅ (v6)
- Config-driven, lifecycle-managed file handles
- CPU + memory → response_time correlation (worst-case evaluation)
- Config-driven thresholds from `metric_thresholds`
- Peak/off-peak hour simulation with 24 weighted hours
- Uses config keys: service, messages, level, metric_thresholds,
  hour_of_day_weights

### `scripts/run_daily.sh` ✅ (v1)
- Portable bash script for automated pipeline execution
- `set -e`, portable root navigation, conda activation
- Timestamped execution logs in `logs/`

### `src/ingestion/log_reader.py` ✅ (v2)
- `load_service_logs(service)` — reads all files for one service
- `load_all_logs(services)` — reads all files across all services

### `src/processing/log_parser.py` ✅ (v4)
- Guard clauses, isdigit(), partition for msg field
- Field presence, empty value, empty message validation
- Returns tuple: (parsed_logs, stats_dict)
- `_skip_report()` logs stats at INFO level

### `src/analysis/log_analysis.py` ✅ (v6)
- Validation orchestrator with single-loop architecture
- Column presence, int dtype, categorical value validation
- Analysis functions: filter, select, count, mean, correlation
- Config-driven metric thresholds via pd.cut()

### `src/analysis/log_visualizer.py` ✅ (v2)
- Seaborn: countplot, histplot, heatmap
- Returns Figure objects for pipeline persistence

### `src/features/feature_engineering.py` ✅ (v2)
- 5 features: is_error, is_slow, hour_of_day, service_encoded, cpu_mem_ratio
- Context columns: timestamp, service, user
- Orchestrator assembles via pd.concat(axis=1)
- Config-driven thresholds, no input mutation

### `src/config_loader.py` ✅ (v3)
- Loop-based validation of 5 required keys
- Called by main.py, independent from generator

### `pipelines/run_pipeline.py` ✅ (v7)
- Receives config from main.py
- Unpacks parser tuple: parsed_logs, parse_stats

### `pipelines/run_reporting_pipeline.py` ✅ (v2)
- Dict collector pattern, 4 report types
- Saves to output/plots/

### `pipelines/run_features_pipeline.py` ✅ (v1)
- Extracts config values, calls orchestrate_features
- Saves to output/datasets/features.csv with index=False

### `main.py` ✅ (v5)
- Loads config once, passes to all pipelines
- Logging at INFO level
- Calls: run_pipeline → report_pipeline → run_features_pipeline

---

## Config Structure (current)

```yaml
service: [shopping, pricing, booking]
messages: {shopping: [...], pricing: [...], booking: [...]}
level: [INFO, WARNING, ERROR]
columns:
  timestamp: datetime.datetime
  service: str
  user: int
  cpu: int
  mem: int
  response_time: int
  level: str
  msg: str
metric_thresholds:
  cpu: {low: 44, normal: 57, high: 70}
  mem: {low: 52, normal: 63, high: 75}
feature_thresholds:
  high_rt: 800
  high_cpu: 70
hour_of_day_weights: [1,2,3,4,5,6,7,8,9,10,11,12,12,11,10,9,8,7,6,5,4,3,2,1]
```

---

## Key Concepts Learned

### Month 1
- yield and generators — lazy iteration, duck typing
- Guard clauses and early return pattern
- Config-driven validation
- File handle lifecycle management
- Type hints (PEP 484) and Google style docstrings
- Module decoupling
- Figure/axes separation in matplotlib

### Month 2
- pd.cut() for binning, .loc[] for conditional assignment
- Generator code doesn't execute until iterated
- Docker: images, containers, Dockerfile, RUN vs CMD, volume mounts
- Missing values: .isna(), .fillna(), .dropna()
- Seaborn: countplot, histplot, heatmap on raw DataFrames
- Pearson correlation, select_dtypes, isinstance()
- Validation orchestrator: single loop, multiple checks per dict
- Format vs content validation across layers

### Month 3
- Feature engineering: Series return, orchestrator assembly, pd.concat(axis=1)
- .rename() for Series naming, .dt.hour accessor, .map() with dict
- Tuple return for data + metadata (parsed logs + stats)
- Config centralization: load once in main, pass to pipelines
- Logging levels: DEBUG < INFO < WARNING < ERROR
- index=False on CSV writes to avoid Unnamed:0
- Bash: shebang, set -e, dirname $0, stdout vs stderr, &>> redirect
- Cron: syntax, PATH issues, local-only config
- source vs bash execution (shell scope)
- chmod +x for execution permissions
- random.choices with weights for weighted randomness

---

## Documentation Status

- `docs/log_generator_design.md` — v6
- `docs/log_reader_design.md` — v3
- `docs/log_parser_design.md` — v4
- `docs/run_pipeline_design.md` — v7
- `docs/main_design.md` — v5
- `docs/log_analysis_design.md` — v6
- `docs/log_visualizer_design.md` — v2
- `docs/run_reporting_pipeline_design.md` — v2
- `docs/run_features_pipeline_design.md` — v1
- `docs/feature_engineering_design.md` — v2
- `docs/config_loader_design.md` — v3
- `docs/docker_design.md` — v1 (updated with volume mount ownership)
- `docs/tech_debt.md` — updated end of Month 3
- `docs/bugs.md` — 14 items (all P1/P2 complete)
- `docs/bugs2.md` — 7 items (all complete except P3 #20, #21)
- `docs/bugs3.md` — 5 items (all complete)

---

## Month 4 Plan

Statistical Foundations for ML:
1. Probability basics and distributions
2. Descriptive statistics on the feature dataset
3. Correlation analysis — verify designed correlations
4. Train/test split with sklearn
5. Bias vs variance concepts
6. Evaluation metrics (accuracy, precision, recall, F1)
7. Statistical analysis report

---

## Working Agreements

- Claude writes design docs, user reviews them
- User writes docstrings themselves
- Sprint checkpoints with quiz questions at end of each sprint
- Push back when user is wrong — don't agree to avoid conflict
- Push back gently when user asks before trying
- OOP: introduce when state + behavior need to live together (Month 8-9)
- Format vs content: parser validates format, analysis validates content
- When new tech debt appears in design docs, add it to tech_debt.md
