# Month 2 — Week 1 (Sprint 3)

## Sprint Goal

Close out Month 1 deliverables and begin the transition into data
analysis depth. By the end of this week the project should have
complete documentation, a working Docker setup, and the first steps
toward Month 2's analytical objectives.

---

## Carry-Over from Month 1

These must be completed before starting new Month 2 work.

### Docstrings and Type Hints (P3 #14)
- Finish all remaining modules:
  - `src/ingestion/log_reader.py`
  - `src/processing/log_parser.py`
  - `src/analysis/log_analysis.py`
  - `src/analysis/log_visualizer.py`
  - `src/config_loader.py`
  - `pipelines/run_pipeline.py`
  - `pipelines/run_reporting_pipeline.py`
  - `main.py`
- Follow the style guide established with the generator
- Single commit for all modules

### Docker Introduction
- Create a simple `Dockerfile`
- Run the full pipeline inside the container
- Verify that `output/plots/` is generated
- Understand volume mounts — persist output outside the container
- No complex Docker setup — just enough to prove environment isolation

---

## Month 2 Focus Begins

Once Month 1 is closed, start the analytical depth work.

### Reader Upgrade — Read All Files
- Currently the reader returns only the first file per service
- Upgrade to read all log files in a service directory
- Concatenate results while maintaining the generator/yield pattern
- This is tracked in tech debt as a Month 1 Week 3–4 item
- Required before analysis results become statistically meaningful

### Generate a Meaningful Dataset
- Generate at least 1000 logs using the generator
- Verify logs are distributed across all three services
- This dataset will be the foundation for all Month 2 analysis

### Pandas Intermediate
- Start working with the larger dataset
- `.describe()` — understand distributions of numeric columns
- `.info()` — verify dtypes are correct
- Handling missing values: `.isna()`, `.fillna()`, `.dropna()`
- Adding computed columns to the DataFrame

---

## Day-by-Day Suggestion

### Day 1–2
- Finish docstrings and type hints across all modules
- Commit and push

### Day 3
- Docker introduction
- Dockerfile, build, run pipeline in container
- Volume mount for output persistence

### Day 4
- Reader upgrade: read all files for a service
- Generate 1000+ logs for testing

### Day 5
- Pandas intermediate: explore the larger dataset
- `.describe()`, `.info()`, distribution analysis

### Day 6–7 (Buffer)
- Refactor and clean up
- Documentation updated
- Sprint review

---

## Sprint Deliverable

At the end of Week 1 you must have:

- All modules with docstrings and type hints
- Working Dockerfile that runs the pipeline
- Reader upgraded to handle all files per service
- Dataset of 1000+ logs generated
- Initial exploration of the larger dataset
- Documentation updated
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs
- Structure is clean
- Documentation updated
- Commit pushed
- Behavior is reproducible
