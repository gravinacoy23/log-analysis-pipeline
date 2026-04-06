# Month 6 — Analysis and Feature Adaptation

## Primary Goal

Adapt the analysis, feature engineering, visualization, and
reporting layers to work with real web server log data. By the
end of this month, the full pipeline should run end-to-end on
real logs, producing features, reports, and train/test splits
relevant to the new domain.

---

# Context

Month 5 delivered a working reader and parser for real web server
access logs. The pipeline produces a raw DataFrame with new
columns — IP address, timestamp, HTTP method, endpoint, status
code, response size, and possibly referer and user agent.

This month adapts everything downstream of the parser: analysis
validation, feature engineering, visualization, reporting, and
the statistical pipeline.

---

# Technical Focus

## Week 1 — Analysis Layer and Visualization

- Update `_validation_orchestrator()` for new column types and
  expected values (e.g. status codes: 200, 301, 404, 500)
- Update `_verify_col_dtype()` for new numeric columns
  (status code, response size)
- Update `_verify_col_values()` for new categorical columns
  (HTTP method: GET, POST, PUT, DELETE)
- Adapt `get_metric_thresholds()` for new metrics if applicable
- Update reporting pipeline with relevant distribution and
  count plots for the new columns
- Run correlation analysis on the new DataFrame — discover
  what correlates in real data vs what you designed in
  synthetic data

## Week 2 — Feature Engineering Redesign

- Design new features relevant to web server logs:
  - **Status code category:** 2xx (success), 4xx (client error),
    5xx (server error)
  - **Is error:** status code >= 400 (or >= 500 depending on
    definition)
  - **Hour of day:** same concept, new timestamp format
  - **Request rate:** requests per time window per IP
  - **Endpoint frequency:** how often each endpoint is hit
  - **Response size bucket:** small, medium, large
- Implement new feature functions following the same pattern:
  each returns a Series, orchestrator assembles with pd.concat
- Update config with new feature thresholds

## Week 3 — Statistical Pipeline and Train/Test Split

- Update the statistical pipeline for the new feature dataset
- Identify the new target variable — what will the ML model
  predict? (e.g. is_error based on status code >= 500)
- Perform train/test split with appropriate stratification
- Run descriptive statistics on the new dataset
- Compare distributions and correlations with synthetic data —
  document the differences
- Evaluate: are the new features suitable for ML?

## Week 4 — End-to-End Verification and Documentation

- Run the full pipeline end-to-end: reader → parser → analysis
  → reporting → features → statistical
- Verify all outputs: plots, feature dataset, train/test splits
- Update all design documents for modified modules
- Write a comparison document: synthetic vs real data pipeline
- Update README.md with the complete new setup
- Update tech_debt.md
- Verify Docker build still works with the new pipeline

---

# Key Differences: Synthetic vs Real Data

| Aspect | Synthetic | Real |
|--------|-----------|------|
| Format | key=value | Common/Combined Log Format |
| Fields | cpu, mem, response_time, level | IP, method, endpoint, status, size |
| Correlations | Designed and known | Discovered through analysis |
| Data quality | Perfect (by design) | Messy (real world) |
| Volume | Controlled | Potentially much larger |
| Feature target | is_error (from level) | is_error (from status code) |

This comparison is itself a deliverable — documenting it
demonstrates understanding of the difference between controlled
experiments and real-world data engineering.

---

# Deliverables

By the end of Month 6 you must have:

- Full pipeline running end-to-end on real logs
- New feature dataset with domain-relevant features
- Updated reporting pipeline with new visualizations
- Distribution and correlation analysis on real data
- Train/test split on the new feature dataset
- Comparison document: synthetic vs real data
- All design documents updated
- Docker build verified
- Frequent commits

---

# Definition of Done

A task is complete when:

- Code runs on real log data
- Analysis includes interpretation of real-world patterns
- Features are documented with ML relevance
- Changes are documented
- Commit pushed
- Results reproducible
