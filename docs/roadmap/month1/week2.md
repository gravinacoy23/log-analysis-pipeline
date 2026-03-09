# Month 1 — Week 2 (Sprint 2)

## Sprint Goal

Introduce pandas and build the first analytical layer on top of the pipeline.

- Convert parsed log data into a pandas DataFrame
- Perform basic data analysis operations
- Build first visualization with matplotlib
- Understand pandas data types and their importance

---

## Context

The pipeline is now functional end to end:

```
log_generator.py → data/raw/ → log_reader.py → log_parser.py → list of dicts
```

This week the list of dicts becomes a DataFrame — the foundation for
all future analysis, feature engineering, and ML work.

---

## Focus Areas

### Pandas Foundations
- Creating a DataFrame from a list of dicts
- Inspecting a DataFrame: `.head()`, `.info()`, `.describe()`
- Understanding dtypes — why they matter for analysis and ML
- Selecting columns and filtering rows
- Basic aggregations: `.value_counts()`, `.groupby()`, `.mean()`

### First Analysis
- Count of logs by level (INFO / WARNING / ERROR)
- Count of logs by service
- Average response time per service
- Average CPU per log level

### Matplotlib Introduction
- Bar plot of log counts by level
- Save plot to `output/`

---

## Where pandas fits in the pipeline

```
log_parser.py → list of dicts → DataFrame → analysis → visualization
```

The DataFrame layer will live in `src/utils/features.py` or a new
`src/analysis/` module — to be decided at the start of the sprint.

---

## Day-by-Day Breakdown

## Day 1
- Install pandas
- Load list of dicts into a DataFrame
- Inspect with `.head()`, `.info()`, `.describe()`
- Identify dtype issues (timestamp as string, numerics correct)

## Day 2
- Fix dtypes — parse timestamp to datetime
- Filter rows by log level
- Select specific columns

## Day 3
- Aggregations: log counts by level and service
- Average response time per service
- Average CPU per log level

## Day 4
- First matplotlib bar plot — log counts by level
- Save to `output/`

## Day 5
- Integrate DataFrame creation into the pipeline
- `run_pipeline.py` returns a DataFrame instead of list of dicts
- Update `main.py` accordingly

## Day 6–7 (Buffer)
- Refactor and clean up
- Documentation updated
- Sprint review

---

## Sprint Deliverable

At the end of Week 2 you must have:

- DataFrame created from parsed logs
- Basic analysis operations working
- At least one matplotlib visualization saved to `output/`
- Pipeline returning a DataFrame
- Documentation updated
- At least 5–7 commits with clear messages

---

## Definition of Done

A task is complete when:

- Code runs
- Structure is clean
- Documentation updated
- Commit pushed
- Behavior is reproducible
