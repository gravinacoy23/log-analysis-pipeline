# Month 3 — Week 2 (Sprint 6)

## Sprint Goal

Introduce Linux automation and enhance the dataset for ML readiness.
By the end of this week the pipeline should be runnable via a bash
script, scheduled with cron, and the generator should produce more
realistic data.

---

## Context

Sprint 5 completed the core Month 3 deliverables:

- Feature engineering module with 5 derived features
- Config-driven thresholds for features
- Feature dataset persisted to `output/datasets/features.csv`
- Features pipeline integrated into `main.py`
- Parser statistics with tuple return
- Config loader validates all required keys
- Logging level changed to INFO for observability

The pipeline now produces an ML-ready feature dataset. This sprint
focuses on automation (bash + cron) and improving the generator to
produce more realistic data for that dataset.

---

## Sprint Focus

### Bash Script

Create `scripts/run_daily.sh` — a shell script that runs the full
pipeline. This is the first time writing bash in the project.

The script should:

1. Run the log generator to produce new logs
2. Run the pipeline via `main.py`
3. Handle exit codes — if the generator fails, the pipeline should
   not run
4. Log output to a file for traceability

Concepts to learn:

- Shebang line (`#!/bin/bash`)
- Running Python from bash
- Exit codes (`$?`, `set -e`)
- Redirecting output to a log file
- Environment variables (basic usage)

### Cron Scheduling

Schedule `run_daily.sh` to run automatically using cron.

Concepts to learn:

- Cron syntax (minute, hour, day, month, weekday)
- `crontab -e` to edit the cron table
- Logging cron output to a file
- Common pitfalls: PATH issues, working directory

### Generator Improvements

Address tech debt items that make the dataset more realistic for
the feature engineering work completed in Sprint 5. Pick 2-3 from
the following based on impact:

1. **Memory as second factor for response_time** — adds a second
   correlated feature for ML. Directly enriches `cpu_mem_ratio`.

2. **Peak vs off-peak hour simulation** — makes `hour_of_day`
   feature meaningful. Currently all hours have uniform load, so
   the feature has no predictive value.

3. **Large-scale log generation** — increase dataset size for
   ML readiness. The current ~2000 rows may not be sufficient
   for training in Month 8.

Priority recommendation: #1 and #2 first — they directly improve
the quality of features already built. #3 is important but simpler
to do anytime.

---

## Tech Debt Mapped to This Sprint

| Item | Module | Connection |
|------|--------|------------|
| Memory as second factor | log_generator | Enriches cpu_mem_ratio feature |
| Peak vs off-peak simulation | log_generator | Makes hour_of_day feature meaningful |
| Large-scale log generation | log_generator | ML dataset size requirement |

---

## Day-by-Day Suggestion

### Day 1
- Learn bash basics: shebang, running Python scripts, exit codes
- Create `scripts/run_daily.sh` with generator + pipeline execution
- Test the script manually

### Day 2
- Add error handling to the bash script (exit on failure)
- Add output logging (redirect stdout/stderr to a log file)
- Learn cron syntax

### Day 3
- Configure cron job to run `run_daily.sh` on a schedule
- Test cron execution and verify log output
- Debug common cron issues (PATH, working directory)

### Day 4
- Generator: add memory as second factor for response_time
- Regenerate dataset and verify `cpu_mem_ratio` feature is
  more meaningful

### Day 5
- Generator: add peak vs off-peak hour simulation
- Regenerate dataset and verify `hour_of_day` feature shows
  load patterns

### Day 6–7 (Buffer)
- Large-scale log generation if time allows
- Documentation updated
- Sprint review and checkpoint

---

## Sprint Deliverable

At the end of Week 2 you must have:

- Bash script that runs the full pipeline (`scripts/run_daily.sh`)
- Cron job configured and tested
- At least 2 generator improvements implemented
- Dataset regenerated with improved generator
- Documentation updated
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs
- Script is executable and tested
- Cron job verified
- Transformations documented
- Config values externalized where applicable
- Commit pushed
- Results reproducible
