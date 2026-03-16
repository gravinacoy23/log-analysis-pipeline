# Docker Setup — Design (v1)

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

## Code and Log Generation

```dockerfile
COPY . .
RUN python3 scripts/log_generator.py -c 100
```

The full codebase is copied into the container. Then the log
generator runs during build to create the dataset the pipeline
needs. This ensures the container is self-contained — it does
not depend on logs existing on the host machine.

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

- **`data/` and `output/` excluded.** Both are generated during
  execution — `data/` by the log generator during build, `output/`
  by the reporting pipeline at runtime. Copying them from the host
  would add unnecessary size and could introduce stale data.

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
docker run log-pipeline
```

## Run with a different service

```bash
docker run log-pipeline python main.py -s pricing
```

---

# Current Limitations

- **Output does not persist.** Plots generated inside the container
  are lost when it stops. Volume mounts will be added in Month 2
  to persist `output/` to the host machine.

- **Logs are generated at build time.** The dataset is baked into
  the image. To analyze different data, the image must be rebuilt.
  This is acceptable for Month 1 — dynamic data loading will evolve
  in later phases.

---

# Future Improvements (Planned)

- Volume mounts for `output/` persistence (Month 2 Week 1)
- Environment variable support for config path resolution (Month 6)
- Docker Compose for local development (Month 6)
- Cloud deployment with Docker on EC2 (Month 6)
