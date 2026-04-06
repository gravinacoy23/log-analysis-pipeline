# Month 5 — Log Source Research and Parser Migration

## Primary Goal

Transition the pipeline from synthetic airline booking logs to
real-world web server access logs. By the end of this month, the
reader and parser should handle the new format, and the pipeline
should produce a raw DataFrame from real log data.

---

# Context

The pipeline was built on synthetic logs with a controlled
`key=value` format:

```
timestamp=2026-03-09T22:15:52Z service=booking user=15 cpu=35 mem=43 response_time=413 level=INFO msg="Booking confirmed"
```

Real web server access logs use a fundamentally different format.
The Common Log Format (CLF) and Combined Log Format look like:

```
192.168.1.1 - - [10/Oct/2025:13:55:36 -0700] "GET /api/booking HTTP/1.1" 200 2326
```

Combined format adds referer and user agent:

```
192.168.1.1 - - [10/Oct/2025:13:55:36 -0700] "GET /api/booking HTTP/1.1" 200 2326 "https://example.com" "Mozilla/5.0 ..."
```

This migration touches the ingestion and processing layers. The
analysis, visualization, and pipeline orchestration layers should
require minimal changes if the parser produces a clean DataFrame
with well-defined columns.

---

# Technical Focus

## Week 1 — Research and Format Understanding

- Obtain a real log dataset (public dataset or locally generated)
- Study the Common/Combined Log Format specification
- Identify all fields and their data types
- Compare with the current synthetic format: what maps, what is
  new, what disappears
- Decide which fields to parse and which to skip
- Update `config.yaml` with new column definitions

## Week 2 — Reader and Parser Migration

- Adapt `log_reader.py` to handle the new file structure
  (single file vs per-service directories)
- Rewrite `log_parser.py` for the new format — the current
  `key=value` splitting will not work; the new format requires
  positional parsing or regex
- Maintain guard clauses and validation patterns — the principles
  stay, the implementation changes
- Update `_parse_fields()` for the new field extraction logic
- Update `_verify_columns()` with new expected columns
- Ensure parser statistics still work (lines processed, skipped,
  skip rate)

## Week 3 — Analysis Layer Adaptation

- Update `log_analysis.py` validation to reflect new columns
  and data types
- Update `expected_columns` and `expected_values` in config
- Verify that `convert_to_dataframe()` produces a clean DataFrame
  from the new parsed data
- Run the pipeline end-to-end with real data for the first time
- Identify and fix issues that surface with real-world data
  quality (malformed lines, encoding issues, edge cases)

## Week 4 — Stabilization and Documentation

- Handle edge cases discovered during Week 3
- Update all design documents for modified modules
- Update `README.md` with new log format and setup instructions
- Update `tech_debt.md` with any new items
- Decide: keep synthetic log support or deprecate cleanly

---

# Key Decisions to Make

## Synthetic log support

The generator and current parser are specific to the synthetic
format. Options:

1. **Keep both** — the reader/parser support both formats via
   config or separate modules
2. **Deprecate synthetic** — remove the old parser, keep the
   generator as a reference in git history

This decision depends on whether synthetic logs still have value
for testing or development. Decide during Week 1.

## Parsing strategy

The current parser uses `str.split()` and `str.partition()`. The
new format may require:

- Positional parsing (split by known delimiters)
- Regular expressions
- A combination of both

The choice should prioritize readability and maintainability over
cleverness. Research both approaches before committing.

## Fields and features

The new format has different fields than the synthetic logs. Some
current features (cpu, mem, response_time) will not exist in web
server logs. New features emerge (status code, request method,
endpoint, response size). The feature engineering module will need
a complete redesign in Month 6.

---

# Project Structure Changes

```
log-analysis-pipeline/
│
├── data/
│   └── raw/
│       └── access/                    ← new (or replaces service dirs)
│
├── config/
│   └── config.yaml                    ← updated with new fields
│
├── src/
│   ├── ingestion/
│   │   └── log_reader.py              ← adapted for new structure
│   ├── processing/
│   │   └── log_parser.py              ← rewritten for new format
│   └── ...
```

---

# Deliverables

By the end of Month 5 you must have:

- A real log dataset in `data/raw/`
- Working reader for the new file structure
- Working parser for the new log format
- Updated config with new column definitions
- Pipeline producing a raw DataFrame from real logs
- Design documents updated for all modified modules
- Frequent commits documenting the migration

---

# Definition of Done

A task is complete when:

- Code runs on real log data
- Parser handles malformed lines gracefully
- Pipeline produces a valid DataFrame
- Changes are documented
- Commit pushed
