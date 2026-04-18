# Log Analysis Pipeline

## Overview

A production-style log analysis pipeline that processes real web server
access logs through a structured data pipeline. The project started with
synthetic airline booking logs and has been migrated to real NASA HTTP
access logs (August 1995, ~1.57M entries).

The project progressively develops strong foundations in:

- Data Science
- Cloud Engineering
- Machine Learning
- Linux
- Git & Documentation discipline

---

## Data Source

NASA Kennedy Space Center WWW server access logs.
Source: https://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html

The dataset contains HTTP access logs from August 1995 in Common Log
Format (CLF). Each entry records a request to the NASA web server
including the client host, timestamp, HTTP method, requested endpoint,
status code, and response size.

---

## Log Format

Each log entry follows Common Log Format:

```
host identity user [timestamp] "method endpoint protocol" status size
```

Example:

```
ppptky455.asahi-net.or.jp - - [01/Aug/1995:06:10:01 -0400] "GET /images/WORLD-logosmall.gif HTTP/1.0" 200 669
```

Fields:

- **host** — client hostname or IP address
- **identity** — RFC 1413 identity (always `-` in this dataset)
- **user** — authenticated username (usually `-`)
- **timestamp** — request date and time with timezone
- **method** — HTTP method (GET, POST, HEAD)
- **endpoint** — requested URL path
- **protocol** — HTTP version (HTTP/1.0)
- **status** — HTTP response status code
- **size** — response body size in bytes

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
│       └── access_logs/
│
├── src/
│   ├── ingestion/
│   │   └── log_reader.py
│   ├── processing/
│   │   └── log_parser.py
│   ├── analysis/
│   │   ├── log_analysis.py
│   │   ├── log_visualizer.py
│   │   └── log_statistical_analysis.py
│   ├── features/
│   │   └── feature_engineering.py
│   └── config_loader.py
│
├── pipelines/
│   ├── run_pipeline.py
│   ├── run_reporting_pipeline.py
│   ├── run_features_pipeline.py
│   └── run_statistical_pipeline.py
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

### Prerequisites

Place at least one log file in `data/raw/access_logs/` before
running the pipeline. The reader will raise a `ValueError` if the
directory is empty.

### Run the pipeline

```bash
python main.py
```

### Run with Docker

Build the image:

```bash
docker build -t log-pipeline .
```

Create output directory and run:

```bash
mkdir -p output
docker run \
  -v $(pwd)/data/raw/access_logs/:/log-analysis-pipeline/data/raw/access_logs/ \
  -v $(pwd)/output:/log-analysis-pipeline/output \
  --user $(id -u):$(id -g) \
  log-pipeline
```

> Note: `mkdir -p output` must be run before the container to
> ensure the directory is owned by your user. If Docker creates
> it automatically, it will be owned by root and the container
> will fail with a permission error when running with `--user`.

---

## Pipeline Architecture

```
data/raw/access_logs/
    → log_reader.py (lazy iteration via generators)
    → log_parser.py (regex, guard clauses, field validation)
    → log_analysis.py (validation orchestrator, DataFrame creation)
    → get_metric_thresholds() (response_size bucketing)
    → run_reporting_pipeline.py → output/plots/
```

Orchestrated by `run_pipeline.py` and `main.py`.
Configuration driven via `config/config.yaml`.

---

## Current Phase

**Phase 1.5 — Real-World Data Migration (Month 6 in progress)**

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

### Month 3 — Complete ✅
- Feature engineering module for ML-ready dataset creation
- Config-driven feature thresholds
- Pipeline persistence to CSV
- Linux automation (bash, cron)

### Month 4 — Complete ✅
- Distribution and correlation analysis
- Train/test split with stratification
- Bias vs variance, evaluation metrics, confusion matrix
- Statistical analysis module and pipeline

### Month 5 — Complete ✅
- Migration from synthetic to real NASA HTTP access logs
- Regex-based parser for Common Log Format
- Config-driven validation for new columns and data types
- End-to-end pipeline verified on ~1.57M log lines

### Month 6 — In Progress
- Reporting pipeline adapted for CLF columns
- Metric thresholds defined for response_size
- Correlation and distribution analysis on real data
- Feature engineering redesign (pending)
- Statistical pipeline adaptation (pending)

---

## Long-Term Vision

This repository will evolve into:

- A structured data pipeline processing real-world data
- A cloud-deployable system (AWS)
- A foundation for ML model training
- A reproducible engineering project

The focus is not just functionality, but engineering discipline,
reproducibility, and production-oriented thinking.
