# Month 1 — Week 1 (Sprint 1)

## Sprint Goal

Build the foundation of the log pipeline:

- Design and implement a production-oriented log generator
- Implement log reader
- Implement basic parser
- Integrate reader + parser in main.py

No pandas yet. No visualization yet. No Docker yet.

---

## Progress Note

This sprint went deeper than originally planned.

The log generator was not just implemented — it was designed, documented,
and refined with production-oriented thinking from day one.

This is intentional. The goal is not speed. The goal is learning things well.

---

# Day-by-Day Breakdown

## Day 1 ✅
- Created repository structure
- Initialized Git
- Created README
- First commit

## Day 2 ✅
- Created `log_generator.py` (initial version)
- Generated synthetic log entries
- Saved logs to `data/raw/` with per-service subdirectories

## Day 3–5 ✅ (Refinement Sprint)
The generator went through a full refinement cycle:

- Separated `level` from `generate_metrics()` — level is a consequence, not a metric
- Introduced CPU → response_time correlation for realistic data
- Implemented threshold + probability logic in `determine_level()`
- Externalized all constants (services, messages, log levels) to `config/config.yaml`
- Implemented `load_config()` using `yaml.safe_load()`
- Renamed `response` to `response_time` for clarity
- Removed unnecessary `return` from `make_service_directories()`
- Updated `log_generator_design.md` to reflect v2 implementation
- Added `*.swp` and `*.swo` to `.gitignore`

## Day 6 — Current
- Implement `reader.py`
  - Lives in `src/ingestion/`
  - Receives a file path
  - Returns a list of raw strings (one per log line)
  - Handles file-not-found gracefully

## Day 7
- Implement `parser.py`
  - Lives in `src/processing/`
  - Receives a list of raw strings
  - Returns a list of dictionaries (one per log line)
  - Handles malformed lines gracefully

## Day 8
- Integrate reader + parser in `main.py`
- Print structured logs to verify pipeline works end to end

## Day 9 (Sprint Review)
- Document what was learned
- Document difficulties encountered
- Reflect on improvements
- Push final version

---

# Sprint Deliverable

At the end of Week 1 you must have:

- Synthetic logs generated automatically with realistic correlations
- Logs read from file safely
- Logs parsed into structured dictionaries
- Pipeline integrated in main.py
- At least 7–10 commits with clear messages
- Documentation updated

---

# Definition of Done

A task is complete when:

- Code runs
- Structure is clean
- Documentation updated
- Commit pushed
- Behavior is reproducible
