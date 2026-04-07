# Session Context — Log Analysis Pipeline

## Current Status

**Month 4 — Complete.**
**Month 5 — In Progress. Sprint 9 (Week 1) complete. Sprint 10 (Week 2) starting.**

Currently migrating the pipeline from synthetic airline booking
logs to real NASA HTTP access logs (Common Log Format).

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
- Config loader refactored: loop-based validation of 5 required keys
- `load_config()` moved from `run_pipeline` to `main.py`
- Logging level changed to INFO for observability
- Linux automation: bash script + cron
- Generator: memory as second factor, peak/off-peak hours
- Sprint 5: 9.5/10, Sprint 6: 8/10

### Month 4 — Fully Complete ✅
- Distribution analysis: response_time, cpu, mem (uniform for
  cpu/mem, skewed toward high for RT due to OR condition)
- Cross-service comparison: identical statistics across all three
  services (generator does not differentiate)
- Correlation analysis: confirmed CPU→RT and MEM→RT correlations,
  no correlation with user
- Correlation vs causation documented
- Train/test split with stratify on `is_error`, random_state=42
- Bias vs variance concepts documented
- Evaluation metrics: accuracy trap, precision, recall, F1
- Confusion matrix function (manual implementation)
- Simulated model comparison: dumb model vs is_slow model
- Statistical analysis module (`log_statistical_analysis.py`)
- Statistical pipeline (`run_statistical_pipeline.py`)
- `docs/statistical_analysis.md` complete
- Sprint 7: 9.5/10, Sprint 8: 8/10
- 200+ commits

### Sprint 9 (Month 5 Week 1) — Complete ✅
- NASA HTTP dataset downloaded (Aug 1995, ~1.57M lines)
- Format analysis: 7 fields documented field-by-field
- Data quality: 10 malformed lines identified, all status 400
  with binary/garbled request data
- Status code distribution: 89% are 200, <1% are 4xx/5xx
- HTTP method distribution: 99.7% GET
- Edge cases: `-` in response size, malformed requests,
  Hurricane Erin data gap
- Regex pattern verified: `r"(\S+) (\S+) (\S+) \[(.+?)\] \"(.+?)\" (\d+) (\S+)"`
- Migration decisions:
  - Deprecate synthetic logs (keep in git history)
  - Use regex for new parser (re.match with capture groups)
  - Update config layer by layer
- All findings documented in `docs/migration_plan/`

---

## Sprint 10 (Month 5 Week 2) — In Progress

Migration sprint. Plan in `docs/week2_month5.md`:
- Day 1: Reader migration (new directory structure)
- Day 2: Parser migration (regex, field extraction)
- Day 3: Config and analysis layer updates
- Day 4: End-to-end verification and cleanup

**Current position: Starting Day 1 — Reader migration.**

---

## Roadmap — Restructured

The roadmap was extended from 10 to 12 months. Phase 1.5 added
for real-world data migration.

- Phase 1 (Months 1–4): Data Science Foundations ✅
- Phase 1.5 (Months 5–6): Real-World Data Migration ← current
- Phase 2 (Months 7–9): Cloud Engineering (AWS, Docker, databases)
- Phase 3 (Months 10–12): Machine Learning

---

## Pipeline — Current State

```
log_generator.py → data/raw/<service>/          ← being deprecated
    → log_reader.py (lazy iteration via generators)
    → log_parser.py (guard clauses, field validation, stats)
    → log_analysis.py (validation orchestrator, DataFrame creation)
    → run_report_pipeline.py → output/plots/
    → feature_engineering.py → run_features_pipeline.py → output/datasets/features.csv
    → log_statistical_analysis.py → run_statistical_pipeline.py → output/datasets/
```

Orchestrated by `run_pipeline.py` and `main.py`.
Configuration loaded once in `main.py`, passed to all pipelines.
Automated via `scripts/run_daily.sh` + cron.

---

## Module Status

### Being Migrated (Sprint 10)

- `log_reader.py` — rewriting for single directory structure
  (no more per-service dirs)
- `log_parser.py` — rewriting with regex for CLF format
- `config.yaml` — updating columns, types, expected values
- `run_pipeline.py` — updating reader call, expected_values,
  metric thresholds
- `main.py` — removing --service argument

### Being Deprecated

- `log_generator.py` — no longer needed with real logs
- `load_service_logs()` / `load_all_logs()` — service concept
  removed
- Synthetic-specific analysis functions in `log_analysis.py`

### Stable (no changes needed)

- `log_visualizer.py` — all functions generic
- `log_analysis.py` — validation layer generic
- `config_loader.py` — only required_keys list changes
- `run_report_pipeline.py` — only column name arguments change
- `run_features_pipeline.py` — minor config key changes
- `run_statistical_pipeline.py` — stratify column may change
- `log_statistical_analysis.py` — all functions generic

### Deferred to Month 6

- `feature_engineering.py` — complete redesign for new domain
- New features: status code category, is_error (from status),
  endpoint frequency, response size buckets, request rate

---

## Config Structure (transitioning)

Current config will be replaced layer by layer. New columns:

```yaml
columns:
  host: str
  identity: str
  user: str
  timestamp: datetime
  method: str
  endpoint: str
  http_version: str
  status_code: int
  response_size: int  # or str to handle "-"
```

Full new config to be defined during Sprint 10 Day 3.

---

## Key Migration Documents

- `docs/migration_plan.md` — module impact analysis, migration
  order, decisions
- `docs/migration_plan/format_analysis.md` — field-by-field
  format documentation, data quality findings, edge cases
- `docs/week2_month5.md` — Sprint 10 plan

---

## Key Concepts Learned (Months 1–4)

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

### Month 4
- Uniform distribution from random.randint
- Law of large numbers (small sample noise vs large sample convergence)
- OR condition producing skewed response_time distribution
- df.describe() — 50th percentile is the median
- Correlation vs causation in synthetic data
- train_test_split with stratify and random_state
- Accuracy trap with imbalanced data
- Precision, recall, F1 — manual computation
- Confusion matrix: TP, TN, FP, FN
- Recall prioritized for error detection systems

### Month 5 (in progress)
- Common Log Format (CLF) field structure
- re.match with capture groups for log parsing
- Data quality exploration with grep, awk, wc
- Mixed delimiters require regex over str.split()
- re.compile() for performance with large files

---

## Documentation Status

- `docs/log_generator_design.md` — v6 (being deprecated)
- `docs/log_reader_design.md` — v3 (being migrated)
- `docs/log_parser_design.md` — v4 (being migrated)
- `docs/run_pipeline_design.md` — v7 (being updated)
- `docs/main_design.md` — v6
- `docs/log_analysis_design.md` — v6
- `docs/log_visualizer_design.md` — v2
- `docs/run_reporting_pipeline_design.md` — v3
- `docs/run_features_pipeline_design.md` — v1
- `docs/feature_engineering_design.md` — v2 (deferred to Month 6)
- `docs/config_loader_design.md` — v3
- `docs/docker_design.md` — v1
- `docs/log_statistical_analysis_design.md` — v2
- `docs/run_statistical_pipeline_design.md` — v1
- `docs/statistical_analysis.md` — complete (Month 4 report)
- `docs/migration_plan.md` — migration impact and decisions
- `docs/migration_plan/format_analysis.md` — CLF format analysis
- `docs/tech_debt.md` — updated end of Month 3
- `docs/bugs.md` — 14 items (all P1/P2 complete)
- `docs/bugs2.md` — 7 items (all complete except P3 #20, #21)
- `docs/bugs3.md` — 5 items (all complete)
- `docs/bugs4.md` — 2 items (#27 resolved, #28 resolved)

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
- Ubuntu native install (no longer WSL)
- Conda env: ML
- Neovim, Pyright, Git/GitHub, Docker
