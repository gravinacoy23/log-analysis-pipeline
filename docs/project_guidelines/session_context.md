# Session Context — Log Analysis Pipeline

## Current Status

**Month 6 — In Progress.**
**Sprint 11 (Week 1) — Complete.**
**Sprint 12 (Week 2) — Next.**

Pipeline fully migrated to real NASA HTTP access logs. Data
pipeline and reporting pipeline running end-to-end on main
branch. Migration branch merged via first PR. Feature engineering
and statistical pipelines pending redesign.

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

### Month 3 — Fully Complete ✅
- Feature engineering module with 5 derived features
- Config-driven thresholds for features
- Feature dataset persisted to `output/datasets/features.csv`
- Features pipeline integrated into `main.py`
- Parser statistics with tuple return and `_skip_report()`
- Config loader refactored: loop-based validation
- `load_config()` moved from `run_pipeline` to `main.py`
- Logging level changed to INFO for observability
- Linux automation: bash script + cron
- Generator: memory as second factor, peak/off-peak hours

### Month 4 — Fully Complete ✅
- Distribution analysis, cross-service comparison
- Correlation analysis: CPU→RT and MEM→RT confirmed
- Train/test split with stratify on `is_error`, random_state=42
- Bias vs variance, evaluation metrics, confusion matrix
- Statistical analysis module and pipeline
- 200+ commits

### Month 5 — Fully Complete ✅

**Sprint 9 (Week 1) — Research and Planning:**
- NASA HTTP dataset downloaded (Aug 1995, ~1.57M lines)
- Format analysis: 7 fields documented field-by-field
- Data quality: 10 malformed lines identified
- Regex pattern verified
- Migration decisions documented
- Sprint checkpoint: 9.5/10

**Sprint 10 (Week 2) — Reader, Parser, and Analysis Migration:**
- Git branch `migration/real-logs` created (first branch)
- Reader migrated: single function, config-driven path,
  `errors="ignore"` for non-UTF-8 bytes
- Parser rewritten: regex with `re.compile()`, `zip()` mapping,
  `HTTP/` prefix detection for protocol disambiguation
- Config updated: new keys (paths, columns, expected_values)
- Analysis layer updated: range validation for http_response,
  None skip for protocol_version, 7 hardcoded functions deprecated
- Run pipeline updated: service parameter removed
- Main updated: service argument removed, downstream pipelines
  commented out
- End-to-end verified: 1,569,887 rows in final DataFrame
- Code review: 8 items (bugs5.md) — all resolved
- Sprint checkpoint: 8.5/10
- 220+ commits

### Sprint 11 (Week 1, Month 6) — Complete ✅

**Reporting pipeline adaptation:**
- `run_reporting_pipeline.py` updated: method count, http_response
  count, response_size distribution, correlation heatmap
- Visualizer unchanged — confirmed generic
- 4 reports instead of 6 (cpu, mem, level, service removed)

**Config cleanup:**
- Deprecated keys removed: `hour_of_day_weights`,
  `feature_thresholds` (old)
- `metric_thresholds` re-added with response_size buckets
- `metric_thresholds` added to `required_keys` in config_loader

**Metric thresholds:**
- `get_metric_thresholds()` updated with dynamic upper bound
  (`"max"` in config resolves to `DataFrame[metric].max()`)
- response_size buckets: low (0–669), normal (669–9200),
  high (9200–max)
- Called from `run_pipeline.py`

**Analysis findings:**
- response_size: right-skewed distribution (median 3.1K,
  mean 17K, max 3.4M)
- http_response: describe() output semantically meaningless
  for categorical-as-int column
- Pearson correlation ~0 between http_response and response_size
  due to class imbalance (89% status 200), categorical nature
  of status codes, and low variance
- Documented in `docs/analysis_findings_month6.md`

**Docker migration:**
- Log generator build step removed
- Input data via volume mount
- `ENV MPLCONFIGDIR=/tmp/matplotlib` added
- Two volume mounts: input (access_logs) + output
- Prerequisite: `mkdir -p output` before docker run

**Documentation and merge:**
- Design docs updated: log_analysis v8, run_pipeline v9,
  reporting v4, config_loader v5, main v7, docker v2
- README rewritten for real data
- `__main__` blocks removed (tech debt: test suite)
- First PR created and merged on GitHub
- Branch `migration/real-logs` deleted
- Sprint checkpoint: 7.7/10

---

## Month 6 — Next

### Sprint 12 (Week 2) — Feature Engineering Redesign

Plan in `docs/week2_month6.md`:
- Design new features for CLF domain
- Implement: status_category, is_error, hour_of_day,
  endpoint_frequency, is_large_response
- Re-enable features pipeline in main.py
- Persist feature dataset to CSV
- Documentation updates

---

## Roadmap — Current Position

- Phase 1 (Months 1–4): Data Science Foundations ✅
- Phase 1.5 (Months 5–6): Real-World Data Migration ← current
  - Month 5: Reader, parser, config, analysis migration ✅
  - Month 6 Week 1: Reporting, thresholds, analysis findings ✅
  - Month 6 Week 2: Feature engineering redesign ← next
  - Month 6 Week 3: Statistical pipeline adaptation
  - Month 6 Week 4: End-to-end verification, documentation
- Phase 2 (Months 7–9): Cloud Engineering (AWS, Docker, databases)
- Phase 3 (Months 10–12): Machine Learning

---

## Pipeline — Current State

```
data/raw/access_logs/ → log_reader.py (lazy iteration, errors="ignore")
    → log_parser.py (regex, re.compile, guard clauses, field validation, stats)
    → log_analysis.py (validation orchestrator, range + list validation, DataFrame)
    → get_metric_thresholds() (response_size_bucket column)
    → run_pipeline.py (orchestrates ingestion → processing → analysis → thresholds)
    → run_report_pipeline.py (method count, status count, size dist, correlation)
    → output/plots/

TEMPORARILY DISABLED:
    → feature_engineering.py (complete redesign — Sprint 12)
    → run_features_pipeline.py (depends on feature_engineering)
    → run_statistical_pipeline.py (depends on features dataset)
```

Orchestrated by `main.py`. Configuration loaded once, passed to
all pipelines. Working on main branch.

---

## Module Status

### Complete and Active

- `log_reader.py` — v4
- `log_parser.py` — v5
- `log_analysis.py` — v8 (get_metric_thresholds updated)
- `config.yaml` — clean, all deprecated keys removed
- `config_loader.py` — v5 (metric_thresholds in required_keys)
- `run_pipeline.py` — v9 (get_metric_thresholds re-enabled)
- `run_reporting_pipeline.py` — v4 (CLF columns)
- `log_visualizer.py` — v2 (unchanged, generic)
- `main.py` — v7 (reporting re-enabled)
- `Dockerfile` — v2 (volume mounts, no generator)

### Needs Redesign (Sprint 12)

- `feature_engineering.py` — complete redesign for CLF domain
- `run_features_pipeline.py` — depends on new features

### Needs Updates (Sprint 13)

- `run_statistical_pipeline.py` — depends on new feature dataset
- `log_statistical_analysis.py` — stratify column may change

---

## Config Structure (current)

```yaml
paths:
  raw_log: data/raw/access_logs/
  output_dir: output/

columns:
  host: str
  identity: str
  user: str
  timestamp: datetime.datetime
  method: str
  endpoint: str
  protocol_version: str
  http_response: int
  response_size: int

expected_values:
  method:
    - GET
    - POST
    - HEAD
  protocol_version:
    - HTTP/1.0
  http_response:
    - 100
    - 599

metric_thresholds:
  response_size:
    low: 669
    normal: 9200
    high: max
```

---

## Data Quality Summary (NASA Dataset)

- **Total lines in file:** 1,569,898
- **Parser output:** 1,569,890 (8 skipped — malformed)
- **Analysis output:** 1,569,887 (3 filtered — 2 binary data,
  1 missing endpoint)
- **Final DataFrame:** 1,569,887 rows × 9 columns + response_size_bucket
- **Key findings:**
  - 89% status 200, right-skewed response_size
  - ~1,400 lines missing protocol (NaN in DataFrame)
  - 10 lines with response_size as `-` (converted to 0)
  - Pearson correlation ~0 (class imbalance, categorical data)
  - Hurricane Erin gap: no data 01/Aug–03/Aug 1995

---

## Key Concepts Learned (Month 6 Week 1)

### Sprint 11
- countplot treats data as categorical regardless of dtype
- right-skewed distribution: mean > median, long tail to the right
- Pearson correlation fails with: low variance, categorical
  relationships, class imbalance
- describe() on categorical-as-int columns produces meaningless
  statistics
- Dynamic bounds in pd.cut(): min() for lower, "max" convention
  for upper
- Docker volume mounts: two mounts (input + output) in same run
- mkdir -p before docker run to avoid root ownership
- MPLCONFIGDIR for matplotlib cache in non-root containers
- GitHub PR workflow: create, review diff, merge, delete branch

---

## Documentation Status

- `docs/log_reader_design.md` — v4
- `docs/log_parser_design.md` — v5
- `docs/log_analysis_design.md` — v8 (updated Sprint 11)
- `docs/run_pipeline_design.md` — v9 (updated Sprint 11)
- `docs/config_loader_design.md` — v5 (updated Sprint 11)
- `docs/main_design.md` — v7 (updated Sprint 11)
- `docs/log_visualizer_design.md` — v2 (no changes needed)
- `docs/run_reporting_pipeline_design.md` — v4 (updated Sprint 11)
- `docs/docker_design.md` — v2 (updated Sprint 11)
- `docs/run_features_pipeline_design.md` — v1 (redesign Sprint 12)
- `docs/feature_engineering_design.md` — v2 (redesign Sprint 12)
- `docs/run_statistical_pipeline_design.md` — v1 (update Sprint 13)
- `docs/log_statistical_analysis_design.md` — v2 (no changes needed)
- `docs/analysis_findings_month6.md` — new (Sprint 11)
- `docs/migration_plan.md` — complete
- `docs/format_analysis.md` — complete
- `docs/statistical_analysis.md` — complete (Month 4)
- `docs/tech_debt.md` — needs test suite entry
- `docs/bugs.md` through `docs/bugs5.md` — all P1/P2 complete

---

## Working Agreements

- Claude writes design docs, user reviews them
- User writes docstrings themselves
- Sprint checkpoints with quiz questions at end of each sprint
- Push back when user is wrong — don't agree to avoid conflict
- Push back gently when user asks before trying
- OOP: introduce when state + behavior need to live together (Month 10+)
- Format vs content: parser validates format, analysis validates content
- When new tech debt appears in design docs, add it to tech_debt.md
- __main__ blocks removed — test suite is tech debt item
- Ubuntu native install
- Conda env: ML
- Neovim, Pyright, Git/GitHub, Docker
- Working on main branch
