# Month 2 — Week 2 (Sprint 4)

## Sprint Goal

Build the visualization and data quality layers. By the end of this
week the pipeline should produce multiple visualizations covering
different analysis objectives, and the analysis layer should include
basic data quality validation.

---

## Context

Sprint 3 closed Month 1 deliverables and started Month 2 work ahead
of schedule. The pipeline now reads all files per service, runs inside
Docker, and supports config-driven computed columns (`cpu_bucket`,
`mem_bucket`) using `pd.cut()`.

The DataFrame has 1996 rows across multiple log files with no missing
values — the generator produces clean data. Data quality checks need
to handle the case where real-world imperfections exist even if the
current dataset does not exhibit them.

---

## Carry-Over

### Missing Values Practice
- `.isna()`, `.fillna()`, `.dropna()`
- The current dataset has no missing values because the generator
  produces complete logs
- The parser gap (missing fields pass through) means NaN values
  could appear if logs are imperfect
- Practice these methods and understand when each is appropriate
- Connect to the parser tech debt item: field presence validation

---

## Sprint Focus

### Seaborn Introduction
- Install seaborn and add to `requirements.txt`
- `seaborn.countplot()` — log counts by level, by service
- `seaborn.histplot()` — response time distribution
- `seaborn.heatmap()` — correlation matrix of numeric columns
- Understand when seaborn adds value over matplotlib

### Visualization Deliverables
Save all plots to `output/plots/`. Required:

1. Bar plot — log count by level (already exists, upgrade with seaborn)
2. Bar plot — log count by service
3. Histogram — response time distribution
4. Heatmap — correlation matrix of numeric columns (cpu, mem, response_time)

The correlation heatmap is important — it should confirm the
CPU → response_time correlation designed into the generator.

### Data Quality Checks
- Are all expected fields present? (connects to parser tech debt)
- Are numeric fields actually numeric?
- Are there unexpected values in categorical fields (level, service)?
- Implement basic validation in the analysis layer

### Generalize Reporting Pipeline
- Current `report_level_pipeline()` is hardcoded to level counts
- With multiple visualizations, the reporting pipeline needs to
  support different report types
- This is tracked in tech debt — now is the time to address it

### Docker Volume Mounts
- Plots generated inside the container are lost when it stops
- Add a volume mount so `output/` persists on the host machine
- `docker run -v $(pwd)/output:/log-analysis-pipeline/output log-pipeline`

---

## Day-by-Day Suggestion

### Day 1
- Missing values: `.isna()`, `.fillna()`, `.dropna()` practice
- Seaborn install and first plot (countplot for log levels)

### Day 2
- Histogram for response time distribution
- Correlation matrix with seaborn heatmap
- Verify CPU → response_time correlation in the data

### Day 3
- Data quality checks in the analysis layer
- Generalize reporting pipeline for multiple report types

### Day 4
- Docker volume mounts
- Verify plots persist outside the container

### Day 5–7 (Buffer)
- Refactor and clean up
- Documentation updated
- Sprint review and checkpoint

---

## Sprint Deliverable

At the end of Week 2 you must have:

- At least 4 visualizations saved to `output/plots/`
- Seaborn used for at least 2 of them
- Data quality checks implemented
- Reporting pipeline generalized
- Docker volume mounts working
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
