# Session Context — Log Analysis Pipeline

## Current Status

**Month 3 — Starting.**
Sprint 4 (Month 2 Week 2) complete. Sprint 5 (Month 3 Week 1) ready to begin.
Sprint 4 refinements pending (7 items, all minor).

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

### Sprint 4 (Month 2 Week 2) — Complete ✅
- Missing values practice: .isna(), .fillna(), .dropna()
- Seaborn introduction: countplot, histplot, heatmap
- 4 visualizations saved to output/plots/
- Removed plot_metric(), replaced with seaborn-based functions
- Generalized reporting pipeline with dict collector pattern
- Data quality checks — 3 initiatives:
  1. Parser: field presence validation + empty value guard
  2. Analysis: int dtype validation via _verify_col_dtype()
  3. Analysis: categorical value validation via _verify_col_values()
- Validation orchestrator: single-loop architecture in analysis layer
- Config refactored: columns changed from list to dict (name → type)
- Config keys renamed: services → service, levels → level
- Docker volume mounts for output persistence
- Correlation matrix function in analysis layer
- Sprint checkpoint: 7.5/10
- Sprint refinements: 7 items identified (P1: 1, P2: 4, P3: 2) — pending

---

## Pipeline — End to End

```
log_generator.py → data/raw/ → log_reader.py → log_parser.py → log_analysis.py → DataFrame
                                                                                → run_reporting_pipeline.py → output/plots/
```

Orchestrated by run_pipeline.py and main.py.

---

## Current Module Status

### `scripts/log_generator.py` ✅ (v4)
- Config-driven, lifecycle-managed file handles
- CPU → response_time → level correlation
- Uses config keys: service, messages, level (renamed from services/levels)

### `src/ingestion/log_reader.py` ✅ (v2)
- `load_service_logs(service)` — reads all files for one service, yields lines
- `load_all_logs(services)` — reads all files across all services, yields lines
- Two private helpers for multi-service reading

### `src/processing/log_parser.py` ✅ (v3)
- Guard clauses, isdigit(), partition for msg field
- Empty value guard: rejects fields like cpu= with no value
- Empty message validation: rejects lines with missing msg
- _verify_columns(): validates field presence per line against config
- Receives expected_cols from pipeline orchestrator
- Returns list of dicts

### `src/analysis/log_analysis.py` ✅ (v6)
- `_validation_orchestrator()` — single-loop validation before DataFrame creation
- `_verify_columns()` — hard stop if list empty or columns missing
- `_verify_col_dtype()` — rejects lines where int columns have wrong type
- `_verify_col_values()` — rejects lines where categorical columns have unexpected values
- `convert_to_dataframe()` — delegates to orchestrator, creates DataFrame
- `convert_corr_matrix()` — Pearson correlation for numeric columns
- `get_metric_thresholds()` — pd.cut() with config-driven thresholds
- Analysis functions: filter, select, count, mean by service/level

### `src/analysis/log_visualizer.py` ✅ (v2)
- `plot_count_metric()` — seaborn countplot, receives DataFrame
- `plot_distribution()` — seaborn histplot
- `plot_correlation()` — seaborn heatmap
- plot_metric() removed — replaced by seaborn functions

### `src/config_loader.py` ✅ (v2)
- Independent from generator's _load_config()
- Validates columns key exists

### `pipelines/run_pipeline.py` ✅ (v5)
- Loads config, extracts column names for parser, full dict for analysis
- Builds expected_values dict for categorical validation
- Runs reader → parser → DataFrame → metric thresholds

### `pipelines/run_reporting_pipeline.py` ✅ (v2)
- `report_pipeline()` — generalized with dict collector pattern
- 4 report types: count by level, count by service, distribution, correlation
- Private functions: _count_report, _corr_report, _dist_report

### `main.py` ✅ (v3)
- Thin entry point, argparse, logging config
- Calls run_pipeline then report_pipeline

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
  cpu:
    low: 44
    normal: 57
    high: 70
  mem:
    low: 52
    normal: 63
    high: 75
```

Note: `service` and `level` keys renamed from `services` and `levels`
to match DataFrame column names — enables direct use as keys in
categorical validation.

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

### Month 2
- pd.cut() for binning continuous data into categories
- .loc[] with two arguments (rows, column) for conditional assignment
- include_lowest parameter for boundary handling
- Generator code doesn't execute until iterated
- Docker fundamentals: images, containers, Dockerfile, RUN vs CMD
- Docker volume mounts: -v host_path:container_path at runtime
- .isna() treats None and NaN as equivalent
- .fillna() with dict for column-specific fill values
- .dropna() returns new DataFrame, does not mutate by default
- inplace=True more dangerous with .dropna() (destroys data) than .fillna()
- Empty string '' is worse than NaN — invisible to .isna()/.fillna()/.dropna()
- Seaborn built on matplotlib, complements it for statistical plots
- Seaborn needs raw DataFrame (countplot counts internally)
- fig, ax = plt.subplots() — figure is canvas, ax is drawing area
- Seaborn accepts ax= parameter to draw on explicit axes
- Pearson correlation: -1 to 1, measures linear relationship
- select_dtypes(include="number") for filtering numeric columns
- isinstance() for runtime type checking
- Boolean flag pattern for nested loops where continue can't reach outer loop
- break on first failure in inner loop for efficiency
- Format vs content validation: parser validates format, analysis validates content
- Validation orchestrator: single loop, multiple validation functions per dict
- KeysView from typing/collections.abc for dict.keys() type hints

---

## Documentation Status

- `docs/log_generator_design.md` — v4
- `docs/log_reader_design.md` — v3
- `docs/log_parser_design.md` — v3
- `docs/run_pipeline_design.md` — v5
- `docs/main_design.md` — v3
- `docs/log_analysis_design.md` — v6
- `docs/log_visualizer_design.md` — v2
- `docs/run_reporting_pipeline_design.md` — v2
- `docs/config_loader_design.md` — v2
- `docs/docker_design.md` — v1 (needs volume mount update)
- `docs/tech_debt.md` — updated
- `docs/bugs.md` — 14 original items + 7 Sprint 4 items

---

## Sprint 5 Plan (Month 3 Week 1)

1. Feature engineering module: is_error, is_slow, hour_of_day, service_encoded, cpu_mem_ratio
2. Config extension: feature_thresholds in config.yaml
3. Persist feature dataset to output/datasets/features.csv
4. Integrate feature module into pipeline
5. Parser: return parsing statistics (tech debt)
6. Documentation updated

---

## Tech Debt Status

### Recently Completed (Sprint 4)
- Parser: field presence validation ✅
- Reporting pipeline: generalized ✅
- Configurable field type mappings: partially completed (int only)

### Active for Month 3
- Parser: return parsing statistics
- Generator: memory as second factor for response_time
- Generator: peak vs off-peak hour simulation
- Generator: service-specific instability modeling
- Generator: temporal correlation between events
- Generator: session-based correlation (session_id)
- Generator: large-scale log generation
- Reader: time range filtering
- Parser: full type mappings from config
- Analysis: handle edge case where .min() exceeds threshold
- Reporting: selective report execution

### Deferred
- Main: support multiple services
- Main: add --output argument
- Main: dictConfig logging (Month 6)
- Config: environment variable path resolution (Month 6)

---

## Sprint 4 Refinements (Pending)

| ID | Module | Issue | Priority |
|----|--------|-------|----------|
| #15 | log_analysis | Incorrect test data in __main__ (level mapped to int) | P1 |
| #16 | log_analysis | Duplicate typing imports | P2 |
| #17 | log_analysis | Docstring param names don't match code | P2 |
| #18 | run_reporting_pipeline | Hardcoded filename in _dist_report | P2 |
| #19 | log_visualizer | Broken __main__ block (dict passed to countplot) | P2 |
| #20 | log_analysis | Outdated __main__ block | P3 |
| #21 | main | print(main()) still dumps DataFrame | P3 |

---

## Working Agreements

- Claude writes design docs, user reviews them
- User writes docstrings themselves
- Sprint checkpoints with quiz questions at end of each sprint
- Push back when user is wrong — don't agree to avoid conflict
- Push back gently when user asks before trying
- OOP: introduce when state + behavior need to live together (likely Month 8-9)
- Format vs content: parser validates format, analysis validates content
