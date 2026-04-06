# Data Science → Cloud → ML Engineering Roadmap (10–12 Months)

## Priority Order

1.  Become strong in Data Science
2.  Transition pipeline to real-world data
3.  Become strong in Cloud Engineering fundamentals
4.  Build solid Machine Learning foundations
5.  Master Git and documentation discipline

This roadmap reflects that order strictly.

------------------------------------------------------------------------

# Phase 1 (Months 1–4): Strong Data Science Foundations ✅

## Global Goal

Develop deep comfort with data manipulation, analysis, and structured
problem solving using Python and Linux.

------------------------------------------------------------------------

## Month 1 — Python + Log Parsing Foundations ✅

Focus: - Python fundamentals (loops, functions, dicts, exceptions) -
Modular project structure - Synthetic log generation (ML-ready design) -
Parsing structured logs - Intro to pandas - Basic matplotlib
visualization

Deliverables: - Modular log pipeline - Structured dictionaries from
logs - DataFrame creation - Bar plot (log counts) - Clean repo
structure - Frequent commits + documentation

------------------------------------------------------------------------

## Month 2 — Data Analysis Deep Dive ✅

Focus: - Pandas (intermediate → advanced) - Grouping & aggregation -
Time-series handling - Data cleaning techniques - Handling missing /
malformed data - Matplotlib deeper usage - Seaborn introduction

Deliverables: - Analytical reports from logs - Multiple visualizations -
Clean feature extraction - Refactored modular code

------------------------------------------------------------------------

## Month 3 — Data Engineering Thinking ✅

Focus: - Feature engineering from logs - Dataset creation for ML -
Reproducible transformations - Config-driven pipeline - Linux automation
(cron) - Bash basics

Deliverables: - Clean feature dataset - Automated local pipeline -
Scheduled execution - Documented transformations

------------------------------------------------------------------------

## Month 4 — Statistical Foundations for ML ✅

Focus: - Probability basics - Distributions - Correlation vs causation -
Train/test split - Bias vs variance - Evaluation metrics (accuracy,
precision, recall, F1)

Deliverables: - Statistical analysis report - Proper dataset splitting -
Documented EDA

------------------------------------------------------------------------

# Phase 1.5 (Months 5–6): Real-World Data Migration

## Goal

Transition the pipeline from synthetic logs to real-world web server
access logs. This phase transforms the project from an academic
exercise into a system that processes data the engineer does not
control — a fundamental shift in complexity and realism.

------------------------------------------------------------------------

## Month 5 — Log Source Research and Parser Migration

Focus: - Research and select a real log source (Nginx/Apache access
logs) - Understand the new log format (Common/Combined Log Format) -
Adapt the reader to handle the new file structure - Rewrite the parser
for the new format - Update config to reflect new fields and
validation rules - Maintain backward compatibility or cleanly
deprecate synthetic log support

Deliverables: - Working reader for real log files - Working parser
for the new format - Updated config.yaml with new fields - Raw
DataFrame from real logs - Documented design decisions for the
migration

------------------------------------------------------------------------

## Month 6 — Analysis and Feature Adaptation

Focus: - Adapt the analysis layer to new columns and data types -
Design new features relevant to web server logs (e.g. status code
patterns, request rate, endpoint frequency) - Update the reporting
pipeline for new metrics - Adapt the statistical analysis and
train/test split for the new dataset - Verify correlations and
distributions in real data - Update feature engineering for the
new domain

Deliverables: - Full pipeline running end-to-end on real logs -
New feature dataset with domain-relevant features - Updated
distribution and correlation analysis - Train/test split on real
data - Documented comparison: synthetic vs real data behavior

------------------------------------------------------------------------

# Phase 2 (Months 7–9): Cloud Engineering Foundations

## Goal

Learn how to move data systems to cloud properly.

------------------------------------------------------------------------

## Month 7 — AWS Core

Focus: - S3 - EC2 - IAM - AWS CLI - Moving data to cloud

Deliverables: - Logs stored in S3 - Pipeline running on EC2 - Secure IAM
configuration

------------------------------------------------------------------------

## Month 8 — Cloud Structure & Automation

Focus: - Environment separation (local vs cloud) - CloudWatch intro -
Dockerizing pipeline properly - Reproducible deployments

Deliverables: - Dockerized pipeline - Cloud execution reproducible -
Basic monitoring

------------------------------------------------------------------------

## Month 9 — Cloud-Native Thinking

Focus: - Stateless processing mindset - Object storage principles -
Modular deployments - Reproducibility in cloud

Deliverables: - Clean cloud-native log pipeline - Portfolio-ready
repository

------------------------------------------------------------------------

# Phase 3 (Months 10–12): Machine Learning Foundations

## Goal

Build ML on top of strong Data + Cloud foundations.

------------------------------------------------------------------------

## Month 10 — Classical ML

Focus: - Linear regression (from scratch + sklearn) - Logistic
regression - Feature scaling - Model evaluation - Overfitting vs
underfitting

Deliverables: - Trained model on log dataset - Evaluation metrics -
Versioned model artifacts

------------------------------------------------------------------------

## Month 11 — Structured ML Pipeline

Focus: - Reproducible training - Experiment tracking (manual logging
first) - Hyperparameter testing - Saving/loading models

Deliverables: - Clean ML training pipeline - Structured experiment
results

------------------------------------------------------------------------

## Month 12 — Introduction to TensorFlow

Focus: - Neural network fundamentals - Loss functions - Gradients
(conceptual understanding) - Simple feedforward network - Model
serialization

Deliverables: - Basic TensorFlow model - Documented training process -
Reproducible setup

------------------------------------------------------------------------

# Git & Documentation (Continuous Requirement)

Every week:

-   Small commits
-   Clear commit messages
-   Updated docs/
-   README improvements
-   Reflection notes

Definition of Done:

-   Code runs
-   Results reproducible
-   Docker build works (when applicable)
-   Documentation updated
-   Commit pushed

------------------------------------------------------------------------

# Strategic Outcome

After completion you should:

-   Be strong in Data Science fundamentals
-   Have a pipeline that processes real-world data
-   Understand Cloud architecture basics
-   Have solid ML foundations
-   Have a professional Git-based portfolio
