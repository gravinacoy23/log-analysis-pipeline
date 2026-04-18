# Docker Setup — Design (v2)

## Objective

Provide environment isolation for the log analysis pipeline.
The Dockerfile packages the pipeline with all its dependencies
so it runs identically regardless of the host machine.

---

# System Context

Docker sits outside the pipeline logic. It does not change how
the code works — it guarantees the environment in which it runs.

```
Host machine → docker build → Docker image (code + dependencies)
Docker image → docker run  → Container (pipeline executes)
             → volume mount → data/raw/access_logs/ (input)
             → volume mount → output/ (output)
```

---

# File Location

```
Dockerfile          (project root)
.dockerignore       (project root)
```

---

# Dockerfile

## Base Image

```dockerfile
FROM python:3.11-slim
```

Uses the official Python 3.11 slim image. The `slim` variant
includes only what is needed to run Python — no compilers, no
extra OS packages. This keeps the image small and the build fast.

## Working Directory

```dockerfile
WORKDIR /log-analysis-pipeline
```

Creates and sets the working directory inside the container.
Uses an absolute path because `~` does not expand in Docker —
there is no user home directory in a fresh container.

## Dependency Installation

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Dependencies are installed before copying the full codebase.
This is intentional — Docker caches each layer. If the code
changes but `requirements.txt` does not, Docker reuses the
cached dependency layer and skips the install step. This makes
rebuilds faster during development.

`--no-cache-dir` tells pip not to store downloaded packages
locally, reducing the final image size.

## Code

```dockerfile
COPY . .
```

The full codebase is copied into the container. Log data is not
included — it is provided at runtime via volume mount.

## Entry Point

```dockerfile
CMD ["python", "main.py"]
```

`CMD` defines the default command when the container starts.
Unlike `RUN`, which executes during build, `CMD` executes
at runtime.

---

# .dockerignore

```
__pycache__/*
data/*
output/*
.git/*
.gitignore
tests/*
docs/*
```

## Design Decisions

- **`data/` excluded.** Log data is provided at runtime via volume
  mount, not baked into the image. This keeps the image small and
  allows analyzing different datasets without rebuilding.

- **`output/` excluded.** Generated at runtime by the reporting
  pipeline. Copying from the host would introduce stale data.

- **`.git/` excluded.** The Git history is not needed to run the
  pipeline and can be significantly larger than the codebase itself.

- **`tests/` and `docs/` excluded.** Neither is required for
  pipeline execution. Tests are for development, docs are for
  humans reading the repository.

- **`__pycache__/` excluded.** Bytecode compiled on the host may
  not be compatible with the Python version inside the container.
  Python regenerates it automatically when the code runs.

---

# How to Build and Run

## Build the image

```bash
docker build -t log-pipeline .
```

## Run the pipeline

```bash
docker run \
  -v $(pwd)/data/raw/access_logs/:/log-analysis-pipeline/data/raw/access_logs/ \
  -v $(pwd)/output:/log-analysis-pipeline/output \
  --user $(id -u):$(id -g) \
  log-pipeline
```

## Prerequisites

The pipeline expects at least one log file in
`data/raw/access_logs/` on the host machine before running
the container. The reader will raise a `ValueError` if the
directory is empty.

## Volume Mounts

Two volume mounts are used:

- **Input:** `data/raw/access_logs/` — mounts the host log files
  into the container where the reader expects them. This allows
  analyzing different datasets by changing the host directory
  without rebuilding the image.

- **Output:** `output/` — mounts the output directory so plots
  and datasets generated inside the container persist on the
  host after the container exits.

## Volume Mount Ownership

By default, files created inside a Docker container are owned by
root. When using volume mounts to persist `output/` to the host,
this means the generated files (plots, datasets) will have root
ownership on the host machine — requiring `sudo` to modify or
delete them.

The `--user $(id -u):$(id -g)` flag solves this by telling the
container to run as the current host user instead of root. This
ensures all files written to the mounted volume have the correct
ownership.

If you encounter permission issues with existing output files:

```bash
sudo rm -rf output
```

Then re-run the container with the `--user` flag.

---

# Changes from v1

- Removed `RUN python3 scripts/log_generator.py -c 2000` from
  Dockerfile — log generator deprecated, real log data is now
  provided via volume mount
- Added input volume mount for `data/raw/access_logs/` — log
  data provided at runtime instead of generated at build time
- Removed `--service` argument from run examples — service
  parameter no longer exists
- Added prerequisites section documenting the requirement for
  log files to exist before running
- `.dockerignore` unchanged — `data/*` remains excluded because
  data enters via volume mount, not `COPY`
- System context updated to show both volume mounts

---

# Future Improvements (Planned)

- Environment variable support for config path resolution
- Docker Compose for local development
- Cloud deployment with Docker on EC2
