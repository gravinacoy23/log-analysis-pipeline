# Session Context — Log Analysis Pipeline

## Current Status

**Month 5 — Complete.**
**Month 6 — Starting. Sprint 11 (Week 1) next.**

Pipeline successfully migrated from synthetic airline booking
logs to real NASA HTTP access logs (Common Log Format). Core
pipeline (reader → parser → analysis → DataFrame) running
end-to-end on real data. Downstream pipelines (reporting,
features, statistical) temporarily disabled pending adaptation.

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

---

## Month 6 — Starting

### Sprint 11 (Week 1) — Analysis Layer and Visualization

Plan in `docs/week1_month6.md`:
- Reporting pipeline column adaptation
- Config cleanup (remove deprecated keys)
- Re-enable reporting pipeline in main.py
- Correlation and distribution analysis on real data
- Documentation updates and __main__ blocks
- Merge `migration/real-logs` branch to main

---

## Roadmap — Current Position

- Phase 1 (Months 1–4): Data Science Foundations ✅
- Phase 1.5 (Months 5–6): Real-World Data Migration ← current
  - Month 5: Reader, parser, config, analysis migration ✅
  - Month 6: Analysis adaptation, feature redesign, reporting ← starting
- Phase 2 (Months 7–9): Cloud Engineering (AWS, Docker, databases)
- Phase 3 (Months 10–12): Machine Learning

---

## Pipeline — Current State

```
data/raw/access_logs/ → log_reader.py (lazy iteration, errors="ignore")
    → log_parser.py (regex, re.compile, guard clauses, field validation, stats)
    → log_analysis.py (validation orchestrator, range + list validation, DataFrame)
    → run_pipeline.py (orchestrates ingestion → processing → analysis)

TEMPORARILY DISABLED:
    → run_report_pipeline.py (needs column name updates — Sprint 11)
    → feature_engineering.py (complete redesign — Month 6 Week 2)
    → run_features_pipeline.py (depends on feature_engineering)
    → run_statistical_pipeline.py (depends on features dataset)
```

Orchestrated by `main.py`. Configuration loaded once, passed to
all pipelines. Working on branch `migration/real-logs`.

---

## Module Status

### Complete (Sprint 10)

- `log_reader.py` — v4, single function, config-driven path
- `log_parser.py` — v5, regex-based CLF parsing
- `log_analysis.py` — v7, range validation, deprecated functions removed
- `config.yaml` — new keys, old keys pending cleanup
- `config_loader.py` — v4, new required keys
- `run_pipeline.py` — v8, service parameter removed

### Needs Updates (Sprint 11)

- `run_reporting_pipeline.py` — column name arguments
- `main.py` — re-enable reporting, update docs
- `__main__` blocks — real data examples
- `config.yaml` — remove deprecated keys

### Deferred to Month 6 Weeks 2–3

- `feature_engineering.py` — complete redesign for CLF domain
- `run_features_pipeline.py` — depends on new features
- `run_statistical_pipeline.py` — depends on new feature dataset
- `log_statistical_analysis.py` — stratify column may change

### Deprecated

- `log_generator.py` — removed from active pipeline
- `load_service_logs()` / `load_all_logs(services)` — replaced
- Hardcoded analysis functions (7 functions) — removed

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
```

Deprecated keys still present: `metric_thresholds`,
`feature_thresholds`, `hour_of_day_weights`. Cleanup in Sprint 11.

---

## Data Quality Summary (NASA Dataset)

- **Total lines in file:** 1,569,898
- **Parser output:** 1,569,890 (8 skipped — malformed)
- **Analysis output:** 1,569,887 (3 filtered — 2 binary data,
  1 missing endpoint)
- **Final DataFrame:** 1,569,887 rows × 9 columns
- **Key findings:**
  - ~1,400 lines missing protocol (None/NaN in DataFrame)
  - 10 lines with response_size as `-` (converted to 0)
  - 2 lines with binary request data pass parser, caught by
    analysis (method not in expected values, status 400)
  - Hurricane Erin gap: no data 01/Aug–03/Aug 1995

---

## Key Concepts Learned (Month 5)

### Sprint 9
- Common Log Format (CLF) field structure
- re.match with capture groups for log parsing
- Data quality exploration with grep, awk, wc
- Mixed delimiters require regex over str.split()
- re.compile() for performance with large files

### Sprint 10
- Git branching: create, push, work on branch
- `errors="ignore"` on file open — drops invalid bytes, not lines
- `re.compile()` — compile once, match many
- `zip()` for parallel iteration — cleaner than index counters
- `HTTP/` prefix check for protocol detection in ambiguous
  request lines
- `strptime` with `%z` for timezone-aware datetime parsing
- `None` in dict → `NaN` in DataFrame automatically
- `if/elif` mutual exclusivity for multi-path validation
- Range validation vs list validation in same function
- Format vs content validation across parser and analysis layers
- Refactoring is cognitively harder than writing from scratch

---

## Documentation Status

- `docs/log_reader_design.md` — v4 (updated Sprint 10)
- `docs/log_parser_design.md` — v5 (updated Sprint 10)
- `docs/log_analysis_design.md` — v7 (updated Sprint 10)
- `docs/run_pipeline_design.md` — v8 (updated Sprint 10)
- `docs/config_loader_design.md` — v4 (updated Sprint 10)
- `docs/main_design.md` — v6 (update deferred to Sprint 11)
- `docs/log_visualizer_design.md` — v2 (no changes needed)
- `docs/run_reporting_pipeline_design.md` — v3 (update Sprint 11)
- `docs/run_features_pipeline_design.md` — v1 (redesign Month 6 Week 2)
- `docs/feature_engineering_design.md` — v2 (redesign Month 6 Week 2)
- `docs/run_statistical_pipeline_design.md` — v1 (update Month 6 Week 3)
- `docs/log_statistical_analysis_design.md` — v2 (no changes needed)
- `docs/migration_plan.md` — complete
- `docs/migration_plan/format_analysis.md` — complete
- `docs/statistical_analysis.md` — complete (Month 4)
- `docs/tech_debt.md` — updated Sprint 10
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
- Ubuntu native install
- Conda env: ML
- Neovim, Pyright, Git/GitHub, Docker
- Working on branch `migration/real-logs` — merge to main in Sprint 11
