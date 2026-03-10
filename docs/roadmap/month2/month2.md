# Month 2 — Data Analysis Deep Dive

## Primary Goal

Build strong pandas and visualization skills using the log pipeline
built in Month 1 as the data source. By the end of this month you
should be able to take a dataset, clean it, analyze it, and communicate
findings through visualizations.

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── src/
│   └── analysis/
│       └── log_analysis.py       ← new this month
│
├── output/
│   └── plots/                    ← new this month
│
├── notebooks/                    ← new this month (optional exploration)
```

---

# Technical Focus

## Pandas — Intermediate to Advanced

- Creating DataFrames from list of dicts
- Inspecting: `.head()`, `.info()`, `.describe()`
- Understanding and fixing dtypes
- Parsing timestamps with `pd.to_datetime()`
- Selecting columns and filtering rows
- `.value_counts()`, `.groupby()`, `.agg()`
- Handling missing values: `.isna()`, `.fillna()`, `.dropna()`
- Sorting and ranking
- Adding computed columns

## Matplotlib — Deeper Usage

- Bar plots, line plots, histograms
- Subplots and figure layout
- Labels, titles, legends
- Saving plots to `output/plots/`

## Seaborn — Introduction

- `seaborn.countplot()`
- `seaborn.histplot()`
- `seaborn.heatmap()` for correlation matrices
- Style and color palettes

---

# Analysis Objectives

Using the airline log data, produce the following analyses:

### Log Level Distribution
- Count of logs per level (INFO / WARNING / ERROR)
- Per service breakdown

### Response Time Analysis
- Average response time per service
- Distribution of response times
- Identify slowest percentile of requests

### CPU Analysis
- Average CPU per service
- Correlation between CPU and response time
- (This correlation was designed into the generator — verify it holds in the data)

### Temporal Analysis
- Log volume over time
- Error rate over time

---

# DataFrame Integration

The pipeline should evolve this month:

```
Before: run_pipeline.py → list of dicts
After:  run_pipeline.py → pandas DataFrame
```

The DataFrame conversion lives in `src/analysis/log_analysis.py`.
`run_pipeline.py` calls it after parsing.

---

# Visualization Deliverables

Save all plots to `output/plots/`. Required plots:

1. Bar plot — log count by level
2. Bar plot — log count by service
3. Histogram — response time distribution
4. Line plot — log volume over time (if enough data)

---

# Data Quality

This month introduces the concept of data quality checks:

- Are all expected fields present?
- Are numeric fields actually numeric?
- Are timestamps parseable?
- Are there unexpected values in categorical fields (level, service)?

Implement basic validation in the analysis layer.

---

# Docker (Continuation)

By end of Month 2:

- Dockerfile runs the full pipeline including analysis
- Output plots are generated inside the container
- Volume mount for `output/` so plots persist outside the container

---

# Deliverables

By the end of Month 2 you must have:

- DataFrame created from parsed logs
- All analysis functions implemented
- At least 4 matplotlib/seaborn visualizations saved to `output/plots/`
- Pipeline returning a DataFrame
- Data quality checks in the analysis layer
- Clean documentation
- Frequent commits

---

# Definition of Done

A task is complete when:

- Code runs
- Structure is clean
- Documentation updated
- Commit pushed
- Results reproducible
