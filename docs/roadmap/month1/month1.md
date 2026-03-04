# Month 1 -- Python Foundations for Log Analysis (Improved)

## Primary Goal

Build a structured and reproducible log parsing system with:

-   Clean project architecture
-   Strong Python fundamentals
-   Introductory pandas usage
-   Basic visualization (matplotlib)
-   First exposure to Docker

------------------------------------------------------------------------

# Project Structure (Required From Day 1)
```
log-analysis-pipeline/
│
├── config/
│   └── config.yaml
│
├── data/
│   └── raw/
├── src
│   ├── ingestion
│   │   └── log_reader.py
│   │
│   ├── processing
│   │   └── log_parser.py
│   │
│   └── utils
│       └── features.py
│
├── pipelines
│   └── run_pipeline.py
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

# Technical Focus

## Python Foundations

-   Variables
-   Loops
-   Functions
-   Lists and dictionaries
-   Exception handling
-   Modular code design

## File Handling

-   Reading text files
-   Writing files
-   Working with directories
-   Processing multiple files

## Log Concepts

-   Log structure
-   Timestamps
-   Log levels (INFO, WARNING, ERROR)
-   Messages

------------------------------------------------------------------------

# Log Generation (New Requirement)

Instead of manually writing logs, you will:

-   Create a Python script: `log_generator.py`
-   Generate realistic synthetic logs
-   Store logs inside `data/raw/`
-   Include variability in:
    -   Log levels
    -   Timestamps
    -   Messages
    -   Random errors

This simulates real-world unpredictability.

------------------------------------------------------------------------

# Data Handling

-   Parse logs into dictionaries
-   Convert structured logs into pandas DataFrame
-   Compute basic counts per log level

------------------------------------------------------------------------

# Visualization (Intro)

Using matplotlib:

-   Create at least one bar plot:
    -   Count of logs by level (INFO/WARNING/ERROR)

Save plots inside `output/`

------------------------------------------------------------------------

# Docker (Intro Exposure)

By the end of Month 1:

-   Create a simple Dockerfile
-   Run the pipeline inside the container
-   Understand environment isolation

No complex Docker setup required yet.

------------------------------------------------------------------------

# Deliverables

By the end of Month 1 you must have:

-   Structured modular project
-   Log generator script
-   Reader and parser modules
-   DataFrame creation
-   Basic matplotlib visualization
-   Dockerfile that runs the pipeline
-   Clean documentation
-   Frequent commits

------------------------------------------------------------------------

# Definition of Done

A task is complete when:

-   Code runs
-   Structure is clean
-   Documentation updated
-   Commit pushed
-   Feature reproducible

