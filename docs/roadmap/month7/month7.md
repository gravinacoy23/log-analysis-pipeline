# Month 7 — AWS Core

## Primary Goal

Move the local pipeline to the cloud. Learn the fundamental AWS services
required to store, process, and manage data in a production environment.
Introduce databases as a persistence layer for processed data.

---

# Technical Focus

## S3 — Object Storage

- What object storage is and why it exists
- Buckets, keys, and prefixes
- Uploading and downloading files with AWS CLI
- Uploading and downloading files with `boto3` (Python SDK)
- S3 bucket structure for the log pipeline
- Lifecycle policies basics

## EC2 — Compute

- What an EC2 instance is
- Instance types — choosing the right size
- SSH into an EC2 instance
- Running the pipeline on EC2
- Stopping vs terminating instances

## IAM — Identity and Access Management

- Users, roles, and policies
- Principle of least privilege
- Creating a role for EC2 to access S3
- Never hardcoding credentials — environment variables and instance roles

## AWS CLI

- Installation and configuration
- `aws s3 cp`, `aws s3 ls`, `aws s3 sync`
- `aws ec2` basics
- Profiles for multiple environments

## Databases — Introduction

- SQL fundamentals: CREATE, INSERT, SELECT, WHERE, GROUP BY, JOIN
- When to use a database vs flat files (CSV) vs object storage (S3)
- Relational databases: tables, schemas, primary keys, foreign keys
- AWS RDS basics — managed relational database service
- DynamoDB basics — when NoSQL makes sense vs relational
- Connecting to a database from Python using a database driver
- Persisting the feature dataset to a database instead of only CSV
- Querying processed data with SQL

The goal is not to become a DBA — it is to understand how data lives
in production systems and how to read from and write to databases
from a pipeline. This is a core skill for Data and ML Engineering.

---

# Pipeline Evolution

By end of Month 7 the pipeline runs in two modes:

### Local Mode
```
log_generator.py → data/raw/ → pipeline → output/datasets/
```

### Cloud Mode
```
log_generator.py → S3 bucket (raw/) → pipeline on EC2 → S3 bucket (processed/)
                                                       → RDS (feature dataset)
```

The code does not change between modes — only the paths and
configuration change. This is achieved via environment variables.

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── config/
│   └── config.yaml               ← extended with cloud config section
│
├── scripts/
│   └── deploy_ec2.sh             ← new this month
│   └── sync_to_s3.sh             ← new this month
│
├── docs/
│   └── aws_setup.md              ← new this month
│   └── database_design.md        ← new this month
```

---

# Data Persistence Strategy

By end of Month 7 the pipeline should support multiple persistence
targets:

- **S3** — raw logs and processed datasets (bulk storage)
- **RDS** — feature dataset for structured queries (SQL access)
- **CSV** — local development and quick inspection (already exists)

The decision of where to persist is configuration-driven. The pipeline
does not hardcode the persistence target.

---

# Security Requirements

- Never commit AWS credentials to Git
- `.gitignore` must include `.env` and `~/.aws/credentials`
- Use IAM roles for EC2 access to S3 and RDS — no access keys on the instance
- Use the principle of least privilege for all IAM policies
- Database credentials managed via environment variables or AWS Secrets Manager

---

# Deliverables

By the end of Month 7 you must have:

- Logs stored in S3
- Pipeline running on EC2
- IAM role configured correctly
- No credentials in the codebase
- Feature dataset persisted to a database
- Basic SQL queries against the stored data
- AWS setup documented in `docs/aws_setup.md`
- Database design documented in `docs/database_design.md`
- Frequent commits

---

# Definition of Done

A task is complete when:

- Pipeline runs on EC2
- Data persists in S3 and database
- IAM is configured securely
- Documentation updated
- Commit pushed
