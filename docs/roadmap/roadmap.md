# Data Pipeline to ML Engineering Roadmap (8 Months)

## Vision

Build a production-oriented data pipeline that evolves into a
cloud-native ML-ready system.

Primary Priorities (in order):

1.  Strong Data Science + Linux foundations
2.  Solid ML foundations (TensorFlow-ready)
3.  Cloud-native application architecture
4.  Professional Git & documentation discipline

This roadmap keeps the original structure but strengthens: -
Reproducibility - Docker usage (early introduction) - ML foundations -
Cloud-native mindset

------------------------------------------------------------------------

# Phase 1 (Months 1--3): Data + Linux Foundations

## Global Goal

Build a robust log-analysis pipeline locally with automation,
visualization, and clean project structure.

------------------------------------------------------------------------

# Month 1 -- Foundations

## Focus

-   Python file handling
-   Log parsing basics
-   Linux navigation
-   Git workflow discipline
-   Docker introduction
-   Basic statistics
-   Pandas (intro)
-   NumPy (intro)
-   Matplotlib (intro)

## Technical Skills

### Python

-   File reading (txt, csv)
-   Lists, dictionaries
-   Basic parsing
-   pathlib
-   csv module
-   json handling

### Data

-   CSV format
-   Basic descriptive statistics
-   Intro to pandas DataFrames
-   Intro to numpy arrays

### Visualization

-   matplotlib basics
-   Simple plots (counts, distributions)

### Linux

-   cd, ls, mkdir, cp, mv
-   cat, grep
-   File permissions basics

### Docker (New -- Early Exposure)

-   What containers are
-   Write first Dockerfile
-   Run Python script inside container
-   Understand environment isolation

## Deliverable

-   Script that parses generated logs
-   Basic statistical summary
-   At least 2 simple plots using matplotlib
-   Project runs inside Docker
-   Documentation updated
-   Code pushed to GitHub

------------------------------------------------------------------------

# Month 2 -- Data Analysis & Visualization

## Focus

-   Pandas (intermediate)
-   Data cleaning
-   Aggregations
-   Grouping
-   Time-based analysis
-   Matplotlib (deeper)
-   Seaborn (introduction)

## Technical Skills

### Data Manipulation

-   Filtering
-   GroupBy
-   Aggregations
-   Merging datasets
-   Handling missing values

### Visualization

-   matplotlib advanced usage
-   seaborn basics
-   Distribution plots
-   Time-series plots

### Engineering Discipline

-   Config file (config.yaml)
-   Separate raw/processed data
-   Modular code structure

## Deliverable

-   Log summaries
-   Visual reports (matplotlib + seaborn)
-   Clean modular structure
-   Dockerized analysis environment

------------------------------------------------------------------------

# Month 3 -- Realistic Logs + Automation

## Focus

-   Parsing complex logs
-   Regex
-   Multiple file processing
-   Automation
-   Linux integration
-   Cron jobs
-   Bash scripting
-   subprocess in Python

## Technical Skills

### Parsing

-   Regex patterns
-   Error handling
-   Multi-file iteration

### Linux Integration

-   Cron
-   chmod
-   Pipes and redirection

### Automation

-   Automated execution
-   Logging output files
-   Structured output folder

## Deliverable

-   Automated local pipeline
-   Multi-file log processing
-   Scheduled job (cron)
-   Visual reports generated automatically

------------------------------------------------------------------------

# Phase 2 (Months 4--5): ML Foundations

## Goal

Build ML knowledge on top of your structured pipeline.

------------------------------------------------------------------------

# Month 4 -- ML Basics

## Focus

-   Feature engineering
-   Train/test split
-   Linear regression
-   Logistic regression
-   Evaluation metrics
-   Overfitting vs underfitting

## Technical Skills

-   Implement basic model manually with NumPy
-   Use scikit-learn
-   Model evaluation metrics
-   Save model artifacts

## Deliverable

-   ML model trained on processed logs
-   Evaluation report
-   Model saved and versioned
-   Docker image including model

------------------------------------------------------------------------

# Month 5 -- Toward TensorFlow

## Focus

-   Neural network fundamentals
-   Intro to TensorFlow
-   Data pipelines for training
-   Reproducible experiments

## Technical Skills

-   TensorFlow basics
-   Simple feedforward network
-   Training loop understanding
-   Model serialization
-   Structured experiment logging

## Deliverable

-   Basic TensorFlow model
-   Training pipeline
-   Versioned experiments
-   Clear documentation

------------------------------------------------------------------------

# Phase 3 (Months 6--8): Cloud-Native Application

## Goal

Move the pipeline + ML model to AWS in a cloud-native way.

------------------------------------------------------------------------

# Month 6 -- AWS Foundations

## Focus

-   S3
-   EC2
-   IAM
-   AWS CLI
-   CloudWatch (intro)

## Deliverable

-   Logs stored in S3
-   Processing running on EC2
-   Results stored in S3
-   Basic monitoring

------------------------------------------------------------------------

# Month 7 -- Cloud Automation

## Focus

-   Automated deployments mindset
-   Environment separation (local vs cloud)
-   Secure IAM roles
-   Logging & monitoring

## Deliverable

-   Automated cloud processing
-   Proper IAM permissions
-   Logs observable in CloudWatch

------------------------------------------------------------------------

# Month 8 -- Cloud-Native ML Pipeline

## Focus

-   Stateless processing
-   Reproducibility
-   Model inference in cloud
-   Ready for container orchestration (future Docker/Kubernetes phase)

## Deliverable

-   Cloud-native log + ML pipeline
-   Fully Dockerized system
-   Clean documentation
-   Portfolio-ready repository

------------------------------------------------------------------------

# Definition of Done

A task is complete when:

-   Code runs correctly
-   Docker build works
-   Documentation updated
-   Commit pushed
-   Feature reproducible

------------------------------------------------------------------------

Progress over perfection.

