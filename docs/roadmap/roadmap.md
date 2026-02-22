# Data Pipeline Learning Roadmap (6 Months)

## Overview

This project is a 6‑month learning journey focused on building practical skills in:

* Python
* Data Analysis
* Linux
* Git & Documentation
* Cloud (AWS)

The project will revolve around building a **log analysis data pipeline** that evolves over time from simple local scripts into a cloud‑deployed system.

This roadmap represents **Phase 1 (0–6 months)**. Future phases may include Machine Learning and advanced cloud architecture.

---

# Phase 1 Goal (0–6 Months)

Build a complete log analysis pipeline that:

* Reads logs from files
* Processes and analyzes them
* Stores results
* Generates visualizations
* Runs on Linux
* Uses Git for version control
* Is documented
* Deploys components to AWS

By the end of Phase 1 the system should look like:

Logs → Processing → Analysis → Storage → Visualization → Cloud

---

# Log Sources

The project will gradually evolve log complexity:

Month 1:

* Simple generated logs
* Excel/CSV files

Month 2:

* Structured logs

Month 3:

* Realistic system-style logs

Month 4:

* Linux logs

Month 5:

* Cloud logs

Month 6:

* Integrated pipeline

Logs will include a mix of:

* System events
* Application events
* Errors
* Warnings
* Informational messages

---

# Tools and Technologies

## Core

* Python
* Linux
* Git
* AWS

## Python Libraries

Core libraries planned for data analysis:

* pandas
* numpy
* matplotlib
* seaborn

Additional utilities:

* pathlib
* csv
* json

These libraries will be introduced progressively throughout the project.

## AWS Services (Planned)

* S3
* EC2
* IAM
* CloudWatch (later)

---

# Repository Structure

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

---

# Learning Principles

## Daily

Each working day should include:

* Small coding task
* Git commit
* Documentation update

## Weekly

Each week should include:

* Working feature
* Documentation
* Review

## Monthly

Each month should include:

* Integration
* Refactoring
* Summary

---

# Month 1 – Foundations

Location: docs/roadmap/month1/month1.md

Focus:

* Git workflow
* Linux basics
* Python file handling
* Reading log files
* Basic log parsing
* Environment setup

Data Tools:

* pandas (introduction)
* numpy (basic usage)

Logs:

* Generated logs

Skills:

* File handling
* Python basics
* Terminal usage
* Git commits

Deliverable:

* Scripts that read logs
* Basic statistics
* Initial documentation

---

# Month 2 – Data Analysis

Location: docs/roadmap/month2/month2.md

Focus:

* Pandas
* Data cleaning
* Aggregations
* Grouping
* Time analysis

Data Tools:

* pandas (intermediate)
* numpy
* matplotlib (introduction)

Logs:

* Structured logs

Skills:

* DataFrames
* Filtering
* Aggregations
* Basic plotting

Deliverable:

* Log summaries
* Basic charts

---

# Month 3 – Realistic Logs

Location: docs/roadmap/month3/month3.md

Focus:

* Parsing complex logs
* Regex
* Multiple files
* Automation

Data Tools:

* pandas
* matplotlib
* seaborn (introduction)

Logs:

* System-style logs

Skills:

* Regex
* Parsing
* Automation
* Visualization

Deliverable:

* Multi-file processing
* Visual reports

---

# Month 4 – Linux Integration

Location: docs/roadmap/month4/month4.md

Focus:

* Linux logs
* Bash
* Cron
* Permissions

Data Tools:

* pandas
* matplotlib
* seaborn

Logs:

* Real Linux logs

Skills:

* Bash
* Cron
* Linux tools

Deliverable:

* Automated processing

---

# Month 5 – Cloud Integration

Location: docs/roadmap/month5/month5.md

Focus:

* AWS S3
* EC2
* Uploading files
* Running scripts

Data Tools:

* pandas
* matplotlib
* seaborn

Logs:

* Cloud-hosted logs

Skills:

* AWS CLI
* EC2
* S3

Deliverable:

* Cloud pipeline

---

# Month 6 – Integration

Location: docs/roadmap/month6/month6.md

Focus:

* Full pipeline
* Visualization
* Automation

Data Tools:

* pandas
* numpy
* matplotlib
* seaborn

Logs:

* Mixed logs

Skills:

* Integration
* Debugging

Deliverable:

* Complete system

---

# Phase 2 Preview (6–12 Months)


Focus:

* Pandas
* Data cleaning
* Aggregations
* Grouping
* Time analysis

Logs:

* Structured logs

Skills:

* DataFrames
* Filtering
* Aggregations

Deliverable:

* Log summaries
* Statistics

---

# Month 3 – Realistic Logs


Focus:

* Parsing complex logs
* Regex
* Multiple files
* Automation

Logs:

* System-style logs

Skills:

* Regex
* Parsing
* Automation

Deliverable:

* Multi-file processing

---

# Month 4 – Linux Integration

Focus:

* Linux logs
* Bash
* Cron
* Permissions

Logs:

* Real Linux logs

Skills:

* Bash
* Cron
* Linux tools

Deliverable:

* Automated processing

---

# Month 5 – Cloud Integration

Focus:

* AWS S3
* EC2
* Uploading files
* Running scripts

Logs:

* Cloud-hosted logs

Skills:

* AWS CLI
* EC2
* S3

Deliverable:

* Cloud pipeline

---

# Month 6 – Integration

Focus:

* Full pipeline
* Visualization
* Automation

Logs:

* Mixed logs

Skills:

* Integration
* Debugging

Deliverable:

* Complete system

---

# Phase 2 Preview (6–12 Months)

Possible extensions:

* Machine Learning
* Anomaly detection
* Predictions
* Docker
* CI/CD

This phase will build on the pipeline created in Phase 1.

---

# Definition of Done

A task is done when:

* Code runs
* Code committed
* Documentation updated

---

# Notes

This roadmap is a living document and will evolve over time.

---

# Detailed Monthly Scopes

## Month 1 – Foundations

Primary Goal:
Build fundamental skills in Git, Linux, and Python while working with simple log files.

Key Objectives:

* Set up project structure
* Initialize Git repository
* Learn basic Linux navigation
* Read files using Python
* Convert Excel files to CSV
* Parse simple logs

Technical Skills:

Python:

* File reading
* Basic parsing
* Lists and dictionaries

Linux:

* cd
* ls
* mkdir
* cp
* mv
* cat
* grep

Git:

* init
* add
* commit
* push

Data:

* CSV format
* Basic statistics

Deliverables:

* Working repository
* Basic scripts
* First dataset
* Documentation

---

## Month 2 – Data Analysis

Primary Goal:
Learn to analyze log data using pandas and numpy.

Key Objectives:

* Load CSV into pandas
* Clean data
* Filter logs
* Group logs
* Aggregate results

Technical Skills:

Python:

* pandas DataFrames
* numpy basics

Data:

* Filtering
* Grouping
* Aggregation

Visualization:

* matplotlib basics

Deliverables:

* Analysis scripts
* Summary statistics
* First charts

---

## Month 3 – Log Parsing

Primary Goal:
Handle more complex and realistic logs.

Key Objectives:

* Parse text logs
* Use regex
* Process multiple files
* Merge datasets

Technical Skills:

Python:

* regex
* file iteration

Data:

* Merging
* Transformations

Visualization:

* seaborn basics

Deliverables:

* Log parser
* Processed datasets

---

## Month 4 – Linux Integration

Primary Goal:
Integrate scripts with Linux environments.

Key Objectives:

* Process Linux logs
* Use bash commands
* Automate tasks
* Handle permissions

Technical Skills:

Linux:

* chmod
* crontab
* pipes

Python:

* subprocess

Deliverables:

* Automated scripts
* Scheduled jobs

---

## Month 5 – Cloud Integration

Primary Goal:
Move the pipeline to AWS.

Key Objectives:

* Upload files to S3
* Run scripts on EC2
* Transfer files

Technical Skills:

AWS:

* S3
* EC2

Tools:

* AWS CLI

Deliverables:

* Cloud storage
* Cloud processing

---

## Month 6 – Integration

Primary Goal:
Build a complete pipeline.

Key Objectives:

* Combine scripts
* Automate pipeline
* Generate reports

Technical Skills:

Python:

* Modular code

Data:

* End-to-end pipeline

Deliverables:

* Full pipeline
* Final documentation

