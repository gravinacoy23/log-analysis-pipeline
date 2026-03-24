# Technical Debt — Log Analysis Pipeline

This document tracks known limitations and planned improvements across all pipeline modules.
Each item includes context on why it was deferred and when it makes sense to implement it.

---

## How to read this document

| Symbol | Meaning |
|--------|---------|
| 🟡 | Implement soon — Month 1 or 2 |
| 🔵 | Implement in Phase 1 — Month 3 |
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

**Target:** Month 2 — after gaining more experience with data analysis and correlation patterns.

---

### 🔵 Peak vs off-peak hour simulation

**Current behavior**
All logs are generated with uniform load regardless of the time of day.

**Why it matters**
Real systems experience predictable patterns — higher load during business hours,
lower load at night. Simulating this would add a temporal dimension to the dataset
that is valuable for time-series analysis and anomaly detection.

**Target:** Month 3 — aligns with feature engineering and time-series work.

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

## Log Parser

---

### 🟡 Validate that all expected fields are present before accepting a line

**Current behavior**
A line is only rejected if a field cannot be split into a `key=value` pair.
A syntactically valid line missing a field like `cpu` or `response_time` would
pass through and produce an incomplete dictionary.

**Why it matters**
Adding field presence validation would catch this class of errors explicitly
and prevent incomplete data from reaching the analysis layer.

**Target:** Month 2 — aligns with data cleaning and handling malformed data in depth.

**Status** [Completed]

Added `_verify_columns()` to the parser — validates each parsed dict
against expected columns from config before accepting it. Also added
empty value guard clause in `_parse_fields()` — rejects fields like
`cpu=` where the value is an empty string. `parse_logs()` now receives
`expected_cols` from the pipeline orchestrator.

---

### 🟡 Return parsing statistics alongside the parsed result

**Current behavior**
The parser silently skips malformed lines and logs a warning. There is no way
for the caller to know how many lines were skipped or what percentage of the
input was valid.

**Why it matters**
Returning a summary (lines processed, lines skipped, skip rate) would improve
observability and make the pipeline easier to monitor and debug.

**Target:** Month 2 — useful for data quality analysis and pipeline monitoring.

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

**Target:** Month 1 (Week 3–4) — same priority as the reader improvement.

---

### 🟡 Return pipeline metadata alongside the parsed result

**Current behavior**
`run_pipeline` returns only the list of parsed log dicts with no additional context.

**Why it matters**
Adding metadata such as lines processed, lines skipped, and execution time would
improve observability and make the pipeline easier to monitor and debug.

**Target:** Month 2 — when reporting becomes part of the pipeline output.

---

### 🟡 Add a reporting or persistence step after parsing

**Current behavior**
The pipeline ends after parsing. Results are returned to the caller with no
persistence or reporting.

**Why it matters**
Adding an optional step to persist results to a file (CSV, JSON) or generate
a summary report would make the pipeline more useful as a standalone tool.

**Target:** Month 2 — when the analysis layer is more mature.

---

## Run Reporting Pipeline

---

### 🟡 Generalize reporting pipeline to support multiple report types

**Current behavior**
`report_level_pipeline()` is hardcoded to produce a single report:
log count by level. Each new report type would require a new dedicated
function.

**Why it matters**
Month 2 introduces additional analyses — log count by service, response
time distribution, CPU analysis. The reporting pipeline will need to
support multiple report types without duplicating the orchestration
logic.

**Target:** Month 2 — when the second and third report types are needed,
the pattern for generalization will be clear.

**Status** [Completed]

Renamed to `report_pipeline()`. Uses a dict collector pattern — each
report function returns `{filename: Figure}`, the orchestrator merges
and saves in a single loop. Supports 4 report types: count by level,
count by service, response time distribution, and correlation heatmap.

---

### 🟡 Selective report execution in reporting pipeline

**Current behavior**
`report_pipeline()` runs all 4 reports unconditionally on every
execution. There is no way to generate only specific reports.

**Why it matters**
As the number of reports grows, running all of them every time
becomes wasteful. Allowing the caller to specify which reports to
run would make the pipeline more flexible and faster for targeted
analysis.

**Target:** Month 2–3 — when the report count grows enough that
selective execution provides clear value.

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

## Log analyzer


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
