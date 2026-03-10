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
│   └── utils/
│       └── features.py
│
├── pipelines/
│   └── run_pipeline.py
│
├── scripts/
│   └── log_generator.py
│
├── output/
├── tests/
├── docs/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run

### Generate logs

```bash
python scripts/log_generator.py -c 1000
```

### Run the pipeline

```bash
python main.py -s booking
```

---

## Current Phase

**Phase 1 — Data Science Foundations (Month 1, Week 1 complete)**

- Synthetic log generation with realistic metric correlations ✅
- Structured log parsing into Python dictionaries ✅
- Pipeline integrated end to end ✅
- DataFrame creation and analysis (coming Week 2)
- Visualization with matplotlib (coming Week 2)

---

## Long-Term Vision

This repository will evolve into:

- A structured data pipeline
- A cloud-deployable system (AWS)
- A foundation for ML model training
- A reproducible engineering project

The focus is not just functionality, but engineering discipline,
reproducibility, and production-oriented thinking.
