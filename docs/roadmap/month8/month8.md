# Month 8 — Cloud Structure & Automation

## Primary Goal

Make the cloud deployment production-grade. Introduce Docker for
reproducibility, environment separation for safety, and basic monitoring
to observe the pipeline in production.

---

# Technical Focus

## Environment Separation

- Local vs cloud environments — why they must be separate
- Environment variables for configuration
- Never hardcoding environment-specific values
- `.env` files for local development
- AWS Parameter Store or environment variables on EC2 for production

## Docker

- What Docker is and why it matters for reproducibility
- Dockerfile structure
- Building and running images
- Volumes and bind mounts
- Docker on EC2
- The pipeline runs identically locally and in the cloud

## CloudWatch — Basics

- What CloudWatch is
- Log groups and log streams
- Sending pipeline logs to CloudWatch
- Basic alarms — alert when error rate exceeds threshold

## Reproducible Deployments

- The pipeline should be deployable from scratch with minimal steps
- `requirements.txt` is always up to date
- README has clear deployment instructions
- Docker ensures environment consistency

---

# Pipeline Evolution

By end of Month 8:

```
Local:
  docker build → docker run → pipeline → output/

Cloud:
  EC2 pulls Docker image → runs pipeline → logs to CloudWatch → output to S3
```

The same Docker image runs in both environments.

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── Dockerfile                         ← formalized this month
├── docker-compose.yml                 ← new this month (local dev)
│
├── docs/
│   └── deployment.md                  ← new this month
│   └── monitoring.md                  ← new this month
```

---

# Deliverables

By the end of Month 8 you must have:

- Dockerized pipeline running locally and on EC2
- Environment separation implemented
- Basic CloudWatch monitoring configured
- Deployment documented step by step in `docs/deployment.md`
- Docker image builds from scratch without errors
- Frequent commits

---

# Definition of Done

A task is complete when:

- `docker build` succeeds
- Pipeline runs identically locally and on EC2
- Logs visible in CloudWatch
- Documentation updated
- Commit pushed
