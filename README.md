# Airline Booking Log Pipeline

## Overview

This project simulates a production-style backend logging system for an
airline booking platform. The goal is to design and build a structured
log pipeline that evolves into a data-driven and cloud-ready system.

The project progressively develops strong foundations in:

- Data Science
- Cloud Engineering
- Machine Learning
- Linux
- Git & Documentation discipline

---

## System Simulation

The system simulates an airline booking backend composed of three services:

- shopping
- pricing
- booking

Each service generates structured logs containing operational metrics such as:

- CPU usage
- Memory usage
- Response time
- Log level (INFO, WARNING, ERROR)

Logs are intentionally designed to be ML-ready — they contain structured,
quantifiable features with realistic correlations suitable for future
modeling and anomaly detection.

---

## Log Format

Each log entry follows this structure:

```
timestamp=<value> service=<service> user=<id> cpu=<value> mem=<value> response_time=<ms> level=<LEVEL> msg="<message>"
```

Example:

```
timestamp=2026-03-09T22:15:52Z service=booking user=15 cpu=35 mem=43 response_time=413 level=INFO msg="Booking confirmed"
```

All fields follow the `key=value` pattern for consistent parsing.

---

## Project Structure

```
log-analysis-pipeline/
│
├── config/
│   └── config.yaml
│
├── data/
│   └── raw/
│       ├── shopping/
│       ├── pricing/
│       └── booking/
│
├── src/
│   ├── ingestion/
│   │   └── log_reader.py
│   ├── processing/
│   │   └── log_parser.py
│   ├── analysis/
│   │   ├── log_analysis.py
│   │   └── log_visualizer.py
│   ├── features/
│   │   └── feature_engineering.py
│   └── config_loader.py
│
├── pipelines/
│   ├── run_pipeline.py
│   └── run_reporting_pipeline.py
│
├── scripts/
│   └── log_generator.py
│
├── output/
│   ├── plots/
│   └── datasets/
│
├── docs/
├── tests/
├── main.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run

### Generate logs

```bash
python scripts/log_generator.py -c 2000
```

### Run the pipeline

```bash
python main.py -s booking
```

### Run with Docker

```bash
docker build -t log-pipeline .
docker run -v $(pwd)/output:/log-analysis-pipeline/output log-pipeline
```

To analyze a different service:

```bash
docker run -v $(pwd)/output:/log-analysis-pipeline/output log-pipeline python main.py -s pricing
```

---

## Pipeline Architecture

```
log_generator.py → data/raw/<service>/
    → log_reader.py (lazy iteration via generators)
    → log_parser.py (guard clauses, field validation)
    → log_analysis.py (validation orchestrator, DataFrame creation)
    → run_reporting_pipeline.py → output/plots/
    → feature_engineering.py → output/datasets/
```

Orchestrated by `run_pipeline.py` and `main.py`.
Configuration driven via `config/config.yaml`.

---

## Current Phase

**Phase 1 — Data Science Foundations (Month 3 in progress)**

### Month 1 — Complete ✅
- Modular log pipeline end to end
- Synthetic log generation with realistic metric correlations
- Structured log parsing into Python dictionaries
- DataFrame creation and basic analysis
- Basic matplotlib visualization
- Dockerfile and containerized execution
- Google-style docstrings and type hints across all modules

### Month 2 — Complete ✅
- Pandas intermediate: groupby, aggregation, computed columns
- Data quality checks at two layers (parser and analysis)
- Validation orchestrator with single-loop architecture
- Seaborn visualizations: countplot, histplot, heatmap
- Generalized reporting pipeline with dict collector pattern
- Config-driven thresholds for metric bucketing
- Docker volume mounts for output persistence
- Missing values handling: .isna(), .fillna(), .dropna()

### Month 3 — In Progress
- Feature engineering module for ML-ready dataset creation
- Config-driven feature thresholds
- Pipeline persistence to CSV
- Linux automation (bash, cron)

---

## Long-Term Vision

This repository will evolve into:

- A structured data pipeline with feature engineering
- A cloud-deployable system (AWS)
- A foundation for ML model training
- A reproducible engineering project

The focus is not just functionality, but engineering discipline,
reproducibility, and production-oriented thinking.
