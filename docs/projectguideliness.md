# Project Guidelines – Log Analysis Pipeline

## Project Purpose

This project is designed as a 6-month learning journey combining:

* Python
* Data Analysis
* Linux
* Git and Documentation
* Cloud
* (Later) Machine Learning basics

The goal is to simulate a real-world data pipeline environment while building practical skills that can be used in industry.

The project will focus on analyzing system logs, starting from small generated logs and gradually moving toward more realistic datasets and cloud-based workflows.

---

## Core Rules

### 1. Always Use Git

Every work session should include:

* Pulling the latest changes (if needed)
* Making small commits
* Writing meaningful commit messages
* Pushing changes to GitHub

Example commit messages:

* "Add log parser"
* "Fix timestamp parsing"
* "Add error analysis"
* "Update documentation"

---

### 2. Documentation Is Mandatory

Every session must include documentation updates.

This can include:

* What was done
* What was learned
* Problems encountered
* Solutions found

Documentation should be stored inside:

```
docs/
```

---

### 3. Prefer Simple Solutions

The goal is learning, not complexity.

Prefer:

* Simple scripts
* Readable code
* Clear structure

Avoid:

* Over-engineering
* Large frameworks
* Unnecessary abstractions

---

### 4. Work With Realistic Data

Logs should look realistic whenever possible.

Logs will be:

* Generated manually at first
* Stored as text files
* Parsed using Python
* Analyzed using pandas

Excel is NOT required for this project.

---

### 5. Project Structure

Expected structure:

```
log-analysis-pipeline/
│
├── data/
├── scripts/
├── output/
├── docs/
└── README.md
```

---

## Session Workflow

Each session should follow this structure:

1. Pull repository
2. Work on a small task
3. Test the code
4. Document the work
5. Commit changes
6. Push to GitHub

---

## Learning Goals

### Python

* File handling
* Data parsing
* Pandas
* Numpy

### Data Analysis

* Aggregations
* Filtering
* Visualization
* Pattern detection

### Linux

* File navigation
* Permissions
* Processes
* Scheduling

### Git

* Commits
* Branches
* Pull requests (later)

### Cloud

* Storage
* Data transfer
* Remote processing

---

## Rules for the Assistant

The assistant should:

* Provide small daily tasks
* Keep tasks practical
* Connect tasks to the main project
* Gradually increase difficulty
* Encourage documentation
* Encourage commits

The assistant should NOT:

* Skip fundamentals
* Introduce unnecessary complexity
* Jump too far ahead

---

## Long-Term Vision

By the end of this project, the repository should include:

* A working log analysis pipeline
* Data processing scripts
* Visualizations
* Documentation
* Cloud integration

This project should be useful as:

* A portfolio project
* A learning reference
* A base for future projects

---

## Important Reminders

Every session:

* Write documentation
* Commit changes
* Push to GitHub

Progress over perfection.

