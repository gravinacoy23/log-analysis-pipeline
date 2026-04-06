# Month 9 — Cloud-Native Thinking

## Primary Goal

Consolidate cloud skills and refactor the pipeline to follow
cloud-native principles. By the end of this month the pipeline
should be portfolio-ready and deployable by anyone from the README.

---

# Technical Focus

## Stateless Processing

- What stateless means and why it matters in the cloud
- The pipeline should not depend on local state between runs
- All state lives in S3 — not on the instance

## Object Storage Principles

- S3 as the single source of truth
- Prefix structure for organized data access
- Versioning and lifecycle policies
- Reading directly from S3 without downloading

## Modular Deployments

- Each component of the pipeline should be independently deployable
- Configuration drives behavior — not code changes
- Feature flags via config

## Reproducibility Audit

Go through the entire project and verify:
- Anyone can clone the repo and run the pipeline
- README covers all setup steps
- No hardcoded paths, credentials, or environment assumptions
- Docker build works from scratch on a clean machine

---

# Portfolio Preparation

This month the repository becomes portfolio-ready.

### README Must Include
- Project overview
- Architecture diagram (simple text diagram is fine)
- Setup instructions
- How to run locally
- How to deploy to AWS
- Technologies used

### Documentation Must Include
- Design docs for all major modules
- Architecture decisions
- Known limitations and future improvements

---

# Deliverables

By the end of Month 9 you must have:

- Fully stateless cloud pipeline
- Portfolio-ready repository
- Complete README
- All documentation up to date
- Clean Git history with meaningful commits
- Pipeline deployable from scratch by following the README

---

# Definition of Done

A task is complete when:

- Code runs
- README instructions work on a clean environment
- Documentation updated
- Commit pushed
- Pipeline is reproducible end to end
