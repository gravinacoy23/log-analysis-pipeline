# Airline Booking Log Pipeline

## Overview

This project simulates a production-style backend logging system for an
airline booking platform.\
The goal is to design and build a structured log pipeline that evolves
into a data-driven and cloud-ready system.

The project progressively develops strong foundations in:

-   Data Science
-   Cloud Engineering
-   Machine Learning
-   Linux
-   Git & Documentation discipline

------------------------------------------------------------------------

## System Simulation

The system simulates an airline booking backend composed of three
services:

-   shopping-service
-   pricing-service
-   booking-service

Each service generates structured logs containing operational metrics
such as:

-   CPU usage
-   Memory usage
-   Response time
-   Log level (INFO, WARNING, ERROR)

Logs are intentionally designed to be ML-ready, meaning they contain
structured, quantifiable features suitable for future modeling and
anomaly detection.

------------------------------------------------------------------------

## Log Format

Each log entry follows this structure:

`<timestamp>`service=`<service_name>`user=`<id>` cpu=`<value>` mem=`<value>` response_time=`<ms>` level=`<LEVEL>` msg="`<message>`"

Example:

2026-03-02T18:23:11Z service=pricing-service user=42 cpu=73 mem=68 response=842 level=INFO msg="Price calculation completed"

Full detailed specification is available in:

docs/logs.md

------------------------------------------------------------------------

## Project Structure
```
log-analysis-pipeline/
│
├── config/
│   └── config.yaml
│
├── data/
│   └── raw/
│
├── src/
│   └── log_pipeline/
│
├── scripts/
│
├── output/
│
├── tests/
│
├── docs/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

## Current Phase

Phase 1 -- Data Science Foundations

-   Synthetic log generation
-   Structured parsing
-   Feature extraction
-   DataFrame creation
-   Exploratory data analysis

------------------------------------------------------------------------

## Long-Term Vision

This repository will evolve into:

-   A structured data pipeline
-   A cloud-deployable system
-   A foundation for ML model training
-   A reproducible engineering project

The focus is not just functionality, but engineering discipline,
reproducibility, and production-oriented thinking.

