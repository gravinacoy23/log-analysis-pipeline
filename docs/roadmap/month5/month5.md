# Month 5 — AWS Core

## Primary Goal

Move the local pipeline to the cloud. Learn the fundamental AWS services
required to store, process, and manage data in a production environment.

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

---

# Pipeline Evolution

By end of Month 5 the pipeline runs in two modes:

### Local Mode
```
log_generator.py → data/raw/ → pipeline → output/datasets/
```

### Cloud Mode
```
log_generator.py → S3 bucket (raw/) → pipeline on EC2 → S3 bucket (processed/)
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
```

---

# Security Requirements

- Never commit AWS credentials to Git
- `.gitignore` must include `.env` and `~/.aws/credentials`
- Use IAM roles for EC2 access to S3 — no access keys on the instance
- Use the principle of least privilege for all IAM policies

---

# Deliverables

By the end of Month 5 you must have:

- Logs stored in S3
- Pipeline running on EC2
- IAM role configured correctly
- No credentials in the codebase
- AWS setup documented in `docs/aws_setup.md`
- Frequent commits

---

# Definition of Done

A task is complete when:

- Pipeline runs on EC2
- Data persists in S3
- IAM is configured securely
- Documentation updated
- Commit pushed
