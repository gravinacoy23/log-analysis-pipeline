# Technical Debt — Log Analysis Pipeline

This document tracks known limitations and planned improvements across all pipeline modules.
Each item includes context on why it was deferred and when it makes sense to implement it.

---

## How to read this document

| Symbol | Meaning |
|--------|---------|
| 🟡 | Implement soon — Month 1 or 2 |
| 🔵 | Implement in Phase 1 — Month 3 or 4 |
| 🟣 | Implement in Phase 2 — Month 6+ |

---

## Log Generator

---

### 🔵 Memory as a second factor influencing response_time

**Current behavior**
Response time is only correlated with CPU. Memory usage is generated independently
and has no effect on other metrics.

**Why it matters**
In a real system, high memory pressure also degrades response times. Adding this
correlation will make the dataset more realistic and introduce a second feature
that ML models can learn from.

**Target:** Month 3 — after gaining more experience with data analysis and correlation patterns.

**Status** [Completed]

---

### 🔵 Peak vs off-peak hour simulation

**Current behavior**
All logs are generated with uniform load regardless of the time of day.

**Why it matters**
Real systems experience predictable patterns — higher load during business hours,
lower load at night. Simulating this would add a temporal dimension to the dataset
that is valuable for time-series analysis and anomaly detection.

**Target:** Month 3 — aligns with feature engineering and time-series work.

**Status** [Completed]

---

### 🔵 Service-specific instability modeling

**Current behavior**
All three services behave identically in terms of load and error rates.

**Why it matters**
In reality, different services have different failure profiles. For example,
the pricing service might spike under high demand while booking remains stable.
Modeling this per service would make the dataset richer for ML training.

**Target:** Month 3 — aligns with dataset creation for ML.

---

### 🔵 Temporal correlation between consecutive events

**Current behavior**
Each log entry is generated independently with no memory of previous events.

**Why it matters**
In real systems, a spike in one event often influences the next — a high CPU log
is more likely to be followed by another high CPU log. Adding this introduces the
concept of autocorrelation in the dataset, which is important for anomaly detection.

**Target:** Month 3 — requires time-series understanding before implementing.

---

### 🔵 Large-scale log generation

**Current behavior**
The generator produces small batches suitable for development and testing.

**Why it matters**
ML models require significantly larger datasets to train and evaluate properly.
This improvement involves generating thousands of logs efficiently and storing
them in a way that supports batch processing.

**Target:** Month 3 — needed when building the training dataset for ML.

---

### 🔵 Session-based correlation between services

**Current behavior**
Log entries are generated independently across services. There is no
relationship between a shopping, pricing, and booking event that belongs
to the same user session.

**Why it matters**
In a real airline system, a user flows through shopping → pricing → booking
as part of a single session. Adding a `session_id` that ties these three
events together would allow the pipeline to detect patterns like session
abandonment — users who reached pricing but never completed booking. This
is a high-value signal for ML models.

**What this requires**
This is a major change to the generator's core logic. Instead of generating
independent events, the generator would need to produce complete sessions,
coordinate the order of events (shopping → pricing → booking), and assign
a shared session ID across all three. The log format would also need a new
`session_id` field.

**Target:** Month 3 — aligns with dataset creation for ML and feature
engineering work. Requires solid understanding of the data before redesigning
the generation logic.

---

### 🟣 Better config path resolution using an environment variable

**Current behavior**
The config file path is resolved using `__file__`, which works locally but can
become fragile in containerized environments.

**Why it matters**
Using an environment variable or a project-level constant would make path
resolution explicit and portable across environments.

**Target:** Month 6 — when the pipeline is formally Dockerized for cloud deployment.

---

## Log Reader

---

### 🟡 Read all log files for a service instead of just the first one

**Current behavior**
The reader selects only the first file it finds in the service directory.

**Why it matters**
Analysis is currently limited to a single log file regardless of how many exist.
For meaningful analysis, the reader should aggregate all available files for a
service into a single list of log lines.

**Target:** Month 1 (Week 3–4) — required before analysis results become statistically meaningful.

**Status** [Completed]

---

### 🟡 Read logs across all services and return a consolidated result

**Current behavior**
The reader requires a specific service name and returns logs for that service only.

**Why it matters**
Supporting multi-service reads would allow the pipeline to analyze the full system —
for example, detecting correlations between shopping and booking load patterns.

**Target:** Month 2 — when cross-service analysis becomes part of the work.

**Status** [Completed]

---

### 🔵 Support reading logs within a specific time range

**Current behavior**
There is no way to filter logs by time when reading from disk.

**Why it matters**
Adding this capability would allow the pipeline to process only the last hour of logs,
or logs from a specific date, without loading everything into memory first.

**Target:** Month 3 — aligns with time-series handling and cron automation.

---

### 🔵 Add encoding parameter for flexibility

**Current behavior**
The reader opens files with default encoding. No way to specify
an alternative encoding.

**Why it matters**
If log files are produced by systems using non-UTF-8 encoding,
the reader would fail silently or produce garbled data.

**Target:** Month 3 or later — only if the project encounters
encoding issues.

---

## Log Parser

---

### 🟡 Validate that all expected fields are present before accepting a line

**Status** [Completed — Sprint 4]

Added `_verify_columns()` to the parser — validates each parsed dict
against expected columns from config before accepting it. Also added
empty value guard clause in `_parse_fields()` — rejects fields like
`cpu=` where the value is an empty string. `parse_logs()` now receives
`expected_cols` from the pipeline orchestrator.

---

### 🟡 Return parsing statistics alongside the parsed result

**Status** [Completed — Sprint 5]

`parse_logs` now returns a tuple: `(list[dict], stats_dict)`. Stats
include lines_processed, skipped_lines, and skip_rate. A `_skip_report()`
function builds and logs the statistics at INFO level. Empty input
(0/0) is handled with a WARNING and skip_rate is omitted to avoid
division by zero.

---

### 🔵 Configurable field type mappings from config.yaml

**Current behavior**
`config.yaml` now maps column names to expected types. The analysis
layer validates `int` columns before DataFrame creation. Type detection
in the parser still uses generic `isdigit()` — it does not reference
the config types.

**Why it matters**
Extending validation to all types (`str`, `datetime`) and potentially
moving type-aware parsing into the parser would make the pipeline
fully explicit about data types end to end.

**Target:** Month 3 — the config structure and analysis-layer
validation are already in place. The remaining work is extending
to additional types.

**Status** [Partially completed — int validation in analysis layer]

---

### 🔵 Support for additional log formats

**Current behavior**
The parser is tightly coupled to the `key=value` format used by this project.

**Why it matters**
Supporting alternative formats (e.g. JSON logs or space-separated logs without keys)
would make the module more reusable in future projects.

**Target:** Month 3 or later — only if the project requires it.

---

## Run Pipeline

---

### 🟡 Accept a list of services and run the pipeline for each

**Current behavior**
The pipeline processes one service per execution. To analyze the full system,
the user must run `main.py` three times.

**Why it matters**
Supporting a list of services would allow a single execution to process all
services and return consolidated results.

**Target:** Month 1 (Week 3–4) — coordinate with reader and main.py improvements.

---

### 🟡 Read all log files for a service, not just the first

**Current behavior**
The orchestrator instructs the reader to return only the first log file found.

**Why it matters**
This is the pipeline-level counterpart of the reader improvement above.
The orchestrator should support aggregating all files for a service.

**Status** [Completed — Sprint 3]

---

### 🟡 Return pipeline metadata alongside the parsed result

**Current behavior**
`run_pipeline` returns only the list of parsed log dicts with no additional context.

**Why it matters**
Adding metadata such as lines processed, lines skipped, and execution time would
improve observability and make the pipeline easier to monitor and debug.

**Status** [Partially completed — Sprint 5]

`parse_logs` now returns stats alongside parsed data. The pipeline
unpacks `parse_stats` but does not yet surface it to the caller or
use it beyond the parser's own logging.

---

### 🟡 Add a reporting or persistence step after parsing

**Status** [Completed — Sprint 4]

Reporting pipeline and features pipeline both consume the DataFrame
produced by `run_pipeline`.

---

### 🔵 Surface parse_stats to caller or logs

**Current behavior**
`parse_stats` is available in `run_pipeline` after unpacking the
tuple from `parse_logs`, but it is not used or surfaced.

**Why it matters**
The pipeline has no visibility into data loss between raw logs and
the final DataFrame beyond what the parser logs internally. Surfacing
stats to the caller or to pipeline-level logs would improve
observability.

**Target:** Month 3–4 — when pipeline monitoring becomes a focus.

---

## Run Reporting Pipeline

---

### 🟡 Generalize reporting pipeline to support multiple report types

**Status** [Completed — Sprint 4]

Renamed to `report_pipeline()`. Uses a dict collector pattern — each
report function returns `{filename: Figure}`, the orchestrator merges
and saves in a single loop. Supports 4 report types: count by level,
count by service, response time distribution, and correlation heatmap.

---

### 🔵 Selective report execution in reporting pipeline

**Current behavior**
`report_pipeline()` runs all 4 reports unconditionally on every
execution. There is no way to generate only specific reports.

**Why it matters**
As the number of reports grows, running all of them every time
becomes wasteful. Allowing the caller to specify which reports to
run would make the pipeline more flexible and faster for targeted
analysis.

**Target:** Month 3–4 — when the report count grows enough that
selective execution provides clear value.

---

### 🔵 Accept output path as parameter

**Current behavior**
The output directory is resolved internally using `__file__`. There
is no way for the caller to specify an alternative output location.

**Why it matters**
Accepting the output path as a parameter would make the pipeline
more flexible for testing and for cloud deployments where output
goes to a different location.

**Target:** Month 3–4.

---

### 🔵 Dynamic filenames with timestamp to avoid overwriting

**Current behavior**
Plot filenames are static (e.g. `level_count_plot.png`). Each
pipeline run overwrites the previous output with no history.

**Why it matters**
With cron running the pipeline automatically, each run should
produce a distinct set of outputs. Timestamped filenames would
preserve history and make it possible to compare results across
runs.

**Target:** Month 3–4.

---

### 🔵 Summary metadata file alongside plots

**Current behavior**
The reporting pipeline saves only plot files. There is no metadata
about the report run (date, service analyzed, record count).

**Why it matters**
A small summary file alongside the plots would make report runs
traceable and reproducible.

**Target:** Month 3–4.

---

## Run Features Pipeline

---

### 🔵 Accept output path as parameter

**Current behavior**
The output directory is resolved internally using `__file__`. There
is no way for the caller to specify an alternative output location.

**Why it matters**
Accepting the output path as a parameter would make the pipeline
more flexible for different runs or environments. Same improvement
as the reporting pipeline.

**Target:** Month 3–4.

---

### 🔵 Dynamic filenames with timestamp to avoid overwriting

**Current behavior**
The output filename is hardcoded as `features.csv`. Each pipeline
run overwrites the previous dataset with no history.

**Why it matters**
With cron running the pipeline automatically, each run should
produce a distinct dataset. Timestamped filenames would preserve
history and make it possible to compare feature datasets across
runs.

**Target:** Month 3–4.

---

### 🔵 Log summary of persisted dataset

**Current behavior**
The features pipeline saves the CSV silently. There is no log message
confirming what was saved (row count, column count, file size).

**Why it matters**
A summary log would confirm the pipeline completed successfully and
provide visibility into the dataset size without opening the file.

**Target:** Month 3–4.

---

## Feature Engineering

---

### 🔵 Feature documentation describing ML relevance

**Current behavior**
Each feature has a docstring explaining what it does, but there is
no documentation explaining why each feature matters for ML — what
signal it captures and how a model would use it.

**Why it matters**
When Month 8 arrives and ML training begins, this documentation will
be essential for understanding which features to keep, modify, or
discard.

**Target:** Month 3–4 — while the features are fresh in memory.

---

## Main

---

### 🟣 Replace logging.basicConfig() with logging.config.dictConfig()

**Current behavior**
Logging is configured using `basicConfig`, which is simple and sufficient
for local development.

**Why it matters**
`dictConfig` supports multiple handlers, log rotation, file output, and
environment-specific configuration — the standard for production Python applications.

**Target:** Month 6 — when the pipeline is deployed to the cloud and production-grade
logging is required.

---

### 🟡 Support running multiple services in a single execution

**Current behavior**
`main.py` accepts a single service name via `--service`.

**Why it matters**
Adding support for multiple services (e.g. `--service booking pricing`) would
allow the user to run the full pipeline in one command.

**Target:** Month 1 (Week 3–4) — implement together with the reader and pipeline
improvements above. These three items are coordinated and should be tackled as a unit.

---

### 🟡 Add a --output argument to persist analysis results to a file

**Current behavior**
`main.py` prints results to stdout with no option to redirect to a file.

**Why it matters**
Adding `--output` would allow the user to save results to CSV or JSON without
modifying the source code, making the pipeline more practical as a CLI tool.

**Target:** Month 2 — when the pipeline starts producing formal analysis outputs.

---

## Log Analysis

---

### 🟡 Expand metric combinations for dashboard support

**Current behavior**
The analysis layer covers a fixed set of metric combinations:
response_time by service and CPU by log level.

**Why it matters**
A production dashboard would need more combinations — memory by service,
error rate over time, response time trends by hour. The current functions
are a foundation but not sufficient for full observability.

**Target:** Month 2 — when the analysis layer matures and visualization
work begins in depth.

---

### 🔵 Handle edge case where .min() exceeds first threshold boundary

**Current behavior**
`get_metric_thresholds()` uses `logs_dataframe[metric].min()` as the
lower edge of the first bin. If the dataset is small or filtered and
the minimum value is higher than the first threshold in the config,
the edges are not monotonically increasing and `pd.cut()` raises a
`ValueError`.

**Why it matters**
With the full dataset (~2000 rows) this does not occur because the
generator's ranges guarantee values below the first threshold. But
with filtered or partial datasets — for example after quality checks
remove lines — the edge case can surface.

**Target:** Month 3 — when the pipeline handles more diverse datasets
and edge cases become more likely.

---

## Log Visualizer

---

### 🔵 Color customization per category

**Current behavior**
All plots use seaborn default colors. There is no way to assign
specific colors to categories (e.g. red for ERROR, yellow for WARNING).

**Why it matters**
Color-coded categories improve readability and make plots immediately
interpretable without reading labels.

**Target:** Month 3–4.

---

### 🔵 Annotation support for heatmap cells

**Current behavior**
The correlation heatmap displays colors but does not show the
numeric correlation values on each cell.

**Why it matters**
Displaying values directly on the heatmap makes it easier to read
exact correlations without relying only on color gradients.

**Target:** Month 3–4.

---

### 🔵 Save figures with optional path parameter

**Current behavior**
Visualizer functions return Figure objects. Saving is handled by
the reporting pipeline. There is no option to save directly from
the visualizer.

**Why it matters**
An optional `save_path` parameter would allow standalone usage of
the visualizer outside the pipeline context.

**Target:** Month 3–4 — low priority since the pipeline pattern works.

---

## Docker

---

### 🟣 Docker Compose for local development

**Current behavior**
The pipeline runs with manual `docker build` and `docker run` commands.

**Why it matters**
Docker Compose would allow defining the full local development
environment (volumes, environment variables, services) in a single
file.

**Target:** Month 6.

---

### 🟣 Cloud deployment with Docker on EC2

**Current behavior**
Docker is used only for local environment isolation.

**Why it matters**
Deploying the containerized pipeline to EC2 is a key Phase 2
deliverable for cloud readiness.

**Target:** Month 6.
