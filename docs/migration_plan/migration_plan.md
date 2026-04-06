# Migration Plan — Synthetic to Real Logs

## Overview

This document tracks the migration of the log analysis pipeline
from synthetic airline booking logs (`key=value` format) to real
web server access logs (Common/Combined Log Format).

The migration preserves the pipeline architecture — orchestration
patterns, validation patterns, config-driven design, and module
separation all survive. What changes is the format-specific code
inside modules.

---

## Format Comparison

### Current: Synthetic (key=value)

```
timestamp=2026-03-09T22:15:52Z service=booking user=15 cpu=35 mem=43 response_time=413 level=INFO msg="Booking confirmed"
```

### Target: Web Server Access Logs (Combined Log Format)

```
192.168.1.1 - frank [10/Oct/2025:13:55:36 -0700] "GET /api/booking HTTP/1.1" 200 2326 "http://www.example.com" "Mozilla/5.0 ..."
```

### Field Mapping

| Current (synthetic) | New (access log) | Notes |
|---------------------|------------------|-------|
| timestamp | timestamp | Different format — ISO 8601 vs CLF datetime |
| service | — | Does not exist in access logs |
| user | remote user | May be empty (`-`) |
| cpu | — | Does not exist |
| mem | — | Does not exist |
| response_time | — | Not in standard CLF |
| level | — | Does not exist |
| msg | — | Does not exist |
| — | IP address | New — client IP |
| — | HTTP method | New — GET, POST, etc. |
| — | endpoint | New — requested URL path |
| — | HTTP version | New — HTTP/1.0, HTTP/1.1 |
| — | status code | New — 200, 404, 500, etc. |
| — | response size | New — bytes sent |
| — | referer | New — Combined format only |
| — | user agent | New — Combined format only |

---

## Module Impact Analysis

### Survives Intact (generic code)

These modules and functions require **no changes** because they
are already generic — they receive column names and config from
the caller, not hardcoded:

**`log_analysis.py` — validation layer:**
- `convert_to_dataframe()` — receives any list of dicts
- `_validation_orchestrator()` — config-driven, no hardcoded columns
- `_verify_columns()` — checks against config keys
- `_verify_col_dtype()` — checks against config types
- `_verify_col_values()` — checks against config values
- `convert_corr_matrix()` — auto-selects numeric columns
- `select_col()` — receives column name as parameter

**`log_visualizer.py` — all functions:**
- `plot_count_metric()` — receives any categorical column
- `plot_distribution()` — receives any numeric column
- `plot_correlation()` — receives any correlation matrix

**`log_statistical_analysis.py` — most functions:**
- `general_statistics()` — wraps `describe()`, works on any DataFrame
- `create_confusion_matrix()` — receives any two boolean lists

**Patterns and infrastructure:**
- Pipeline orchestration (main → pipelines → modules)
- Validation orchestrator pattern (single loop, per-dict checks)
- Dict collector pattern (reporting pipeline)
- Guard clause pattern (parser, analysis)
- Logging infrastructure
- `_skip_report()` in parser
- `_verify_columns()` in parser

---

### Requires Rewrite (format-specific code)

**`log_parser.py` — `parse_logs()` and `_parse_fields()`**

Level: **Complete rewrite** of parsing logic.

Current code uses `str.partition(" msg=")`, `str.split(" ")`,
`str.split("=")`, and `isdigit()` — all specific to `key=value`
format. The new format requires positional parsing or regex.

What survives in the parser:
- `_verify_columns()` — generic
- `_skip_report()` — generic
- The orchestration flow in `parse_logs()` (iterate, validate,
  skip bad lines, collect good lines) — the structure survives,
  the parsing logic inside changes

**`log_reader.py` — directory and path logic**

Level: **Rewrite** of path resolution.

Current code assumes per-service directories (`data/raw/booking/`,
`data/raw/shopping/`, `data/raw/pricing/`). Real logs will likely
be in a single directory or a single file.

What survives in the reader:
- The generator pattern (`yield` per line) — core concept intact
- File iteration and sorting logic
- Error handling pattern (fail fast)

**`feature_engineering.py` — all feature functions**

Level: **Complete rewrite** of feature functions.

Every current feature references synthetic columns:
- `_is_error()` → uses `"level" == "ERROR"`
- `_is_slow()` → uses `"response_time"`
- `_service_encoded()` → uses `"service"`
- `_cpu_mem_ratio()` → uses `"cpu" / "mem"`
- `_hour_of_day()` → **may survive** if timestamp parsing is similar

What survives in feature engineering:
- Orchestrator pattern (`orchestrate_features()` with list collector)
- `_context_cols()` — generic, receives column list as parameter
- The principle: each function returns a Series, orchestrator assembles

**`log_generator.py`**

Level: **Deprecated.** Not needed when using real logs. Stays in
git history as reference.

---

### Requires Targeted Changes (partially format-specific)

**`config.yaml`**

Level: **Content rewrite**, structure survives.

Changes needed:
- `columns` — new column names and types
- `service` — removed or replaced
- `level` — removed or replaced
- `metric_thresholds` — new metrics (status code ranges, response
  size ranges)
- `feature_thresholds` — new thresholds for new features
- `messages` — removed
- `hour_of_day_weights` — removed (no generator)

**`config_loader.py`**

Level: **Minor change** — update `required_keys` list.

**`run_pipeline.py`**

Level: **Targeted changes** (4–5 lines).

- `load_service_logs(service)` → new reader function call
- `expected_values` dict — new keys (`"method"`, `"status_code"`)
  instead of `"service"` and `"level"`
- `get_metric_thresholds()` calls — new metric names

**`run_reporting_pipeline.py`**

Level: **Targeted changes** in report calls.

- `_count_report(df, "level")` → new categorical column
- `_count_report(df, "service")` → new categorical column
- `_dist_report(df, "response_time")` → new numeric column
- `_dist_report(df, "cpu")` → new numeric column
- `_dist_report(df, "mem")` → new numeric column

The functions themselves are generic — only the arguments change.

**`run_features_pipeline.py`**

Level: **Minor changes** — config key extraction adapts to new
feature thresholds.

**`run_statistical_pipeline.py`**

Level: **1 line** — stratify column may change from `"is_error"`.

**`main.py`**

Level: **Minor change** — `--service` argument removed or
repurposed.

**`run_daily.sh`**

Level: **Minor change** — remove log generator call, update
`main.py` invocation if arguments change.

**`Dockerfile`**

Level: **Minor change** — remove `RUN python3 scripts/log_generator.py`
build step, add real log data handling.

**`log_analysis.py` — hardcoded analysis functions**

Level: **Rewrite or deprecate** these specific functions:
- `filter_loglevel()` — hardcodes `"level"` column
- `count_by_level()` / `count_by_level_all()` — hardcode `"level"`
- `count_by_service()` / `count_by_service_all()` — hardcode `"service"`
- `mean_rt_by_service()` — hardcodes `"service"` and `"response_time"`
- `mean_cpu_by_level()` — hardcodes `"level"` and `"cpu"`
- `get_metric_thresholds()` — **generic**, survives as-is

**`__main__` blocks**

Level: **Update** test data in all modules to reflect new format.

---

## Migration Summary

| Category | Modules | Estimated effort |
|----------|---------|------------------|
| No changes | Visualizer, validation layer, corr matrix, describe, confusion matrix | 0% |
| Minor changes (1–5 lines) | config_loader, run_features_pipeline, run_statistical_pipeline, main, run_daily.sh, Dockerfile | ~10% |
| Targeted changes (config + calls) | run_pipeline, run_reporting_pipeline, config.yaml | ~15% |
| Rewrite or deprecate | Analysis hardcoded functions | ~15% |
| Complete rewrite | Parser (parse logic), reader (path logic), feature engineering (all features) | ~40% |
| Deprecated | Log generator | Removed |

**Architecture survival rate: 100%**
**Code rewrite: ~40%**

---

## Migration Order

Recommended sequence to minimize breakage:

1. **Config** — define new columns, types, expected values, thresholds
2. **Reader** — adapt to new file/directory structure
3. **Parser** — rewrite parsing logic for new format
4. **Run pipeline** — update to use new reader and new config keys
5. **Verify** — pipeline produces a valid DataFrame from real logs
6. **Analysis** — rewrite or deprecate hardcoded functions
7. **Reporting** — update column names in report calls
8. **Feature engineering** — design and implement new features
9. **Features pipeline** — update config extraction
10. **Statistical pipeline** — update stratification column
11. **Main** — update CLI arguments
12. **Docker / bash** — update build and automation scripts
13. **Documentation** — update all design docs and README

---

## Decisions Pending

- **Synthetic log support:** Keep both formats (via config/separate
  modules) or deprecate synthetic? Decide during Week 1 research.
- **Parsing approach:** String splitting vs regex vs combination.
  Research during Week 1.
- **New features:** What features are relevant for web server logs?
  Design during Month 6.
- **New target variable:** What will the ML model predict?
  Decide during Month 6.
