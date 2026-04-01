# Log Generator — Implementation (v6)

## Objective

Implement a synthetic log generator for the airline booking backend simulation.

The goal of this phase is to:

- Define a consistent and parseable log format
- Build a modular log generation structure
- Generate valid log lines for multiple services
- Persist generated logs to disk efficiently
- Introduce realistic correlations between system metrics
- Prepare the foundation for future ML pipelines

---

# System Context

The simulated system represents an airline booking platform composed of three services:

- shopping
- pricing
- booking

Each generated log represents a single backend request event.

The log generator simulates operational metrics typically found in backend service logs: CPU usage, memory usage, response time, log level, and event messages.

---

# Log Format

Each log entry follows this structure:

```
timestamp=<timestamp> service=<service> user=<id> cpu=<value> mem=<value> response_time=<ms> level=<LEVEL> msg="<message>"
```

Example:

```
timestamp=2026-03-02T18:23:11Z service=pricing user=42 cpu=73 mem=68 response_time=842 level=WARNING msg="Dynamic price applied"
```

### Design Considerations

The format is intentionally designed to be:

- **Human readable**
- **Machine parseable**
- **Feature-friendly for ML pipelines**

Each field can be extracted into structured features for analysis and model training.

> Note: Field was renamed from `response` to `response_time` for clarity.

---

# Configuration

All constants (services, messages, log levels) are externalized to `config/config.yaml`.

This follows the principle of separating configuration from logic.

The generator loads configuration at runtime using `_load_config()`, which reads the YAML file using `yaml.safe_load()`.

`safe_load()` is used instead of `yaml.load()` because it only parses data and never executes arbitrary code, making it safe for production-oriented systems.

### config.yaml structure (relevant section)

```yaml
service:
  - shopping
  - pricing
  - booking

messages:
  shopping:
    - "FareSearch completed"
    - "AirShopping completed"
    - "No fares available"
  pricing:
    - "OfferPrice completed"
    - "Dynamic price applied"
    - "Fare rules evaluated"
  booking:
    - "Booking confirmed"
    - "Booking failed"
    - "Seat booked"

level:
  - INFO
  - WARNING
  - ERROR

metric_thresholds:
  cpu:
    low: 44
    normal: 57
    high: 70
  mem:
    low: 52
    normal: 63
    high: 75

hour_of_day_weights:
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

### Return Format

`_load_config()` returns the config as a dictionary. This allows adding
new config fields without breaking existing code — callers access values
by key (`config["service"]`) instead of relying on positional unpacking.

Validation uses `.get()` to check that required keys exist and are not
empty before returning the dict. If a key is missing or falsy, a
descriptive `ValueError` is raised immediately.

---

# Implementation Details

## Module Structure

The generator has one public function and multiple private helpers:

### Public Interface
- `generate_logs(iterations)` — entry point, orchestrates the full
  generation pipeline

### Private Functions — Setup
- `_load_config()` — loads and validates config from config.yaml,
  returns a dict
- `_make_raw_directory()` — creates `data/raw/` if it does not exist
- `_make_service_directories(raw_dir, services)` — creates per-service
  subdirectories
- `_create_files(services, target_path, run_timestamp)` — opens one
  file per service and returns a dict of file handles
- `_close_files(file_handles)` — closes all open file handles

### Private Functions — Generation
- `_generate_log_timestamp(hour_weights)` — generates a UTC timestamp
  with a weighted random hour to simulate peak/off-peak patterns
- `_generate_runtimestamp()` — generates timestamp used for output
  filenames
- `_generate_service(services)` — selects a random service from config
- `_generate_message(service, message_list)` — selects a message based
  on service
- `_generate_user()` — generates a random user ID
- `_generate_cpu()` — generates a random CPU usage value
- `_generate_memory()` — generates a random memory usage value
- `_generate_response_time(cpu, mem, thresholds)` — generates response
  time correlated with CPU and memory load using config-driven thresholds
- `_determine_level(response_time, levels)` — determines log level
  based on response time thresholds and probabilities
- `_format_log(...)` — builds the final log line string

### Private Functions — Persistence
- `_write_log(file_handles, service, log_line)` — writes a log line
  to the correct file using the service name as key

### Orchestration
- `_generator_loop(iterations, raw_data, file_handles)` — runs the
  generation loop, producing one log per iteration

All helper functions are prefixed with `_` to signal they are internal
to the module. Only `generate_logs()` is part of the public interface.

---

## Orchestration — generate_logs()

`generate_logs()` is the entry point. It handles the full lifecycle:

1. **Setup** — create directories, load config, generate run timestamp
2. **Open files** — create one file handle per service
3. **Generate** — delegate to `_generator_loop()`
4. **Cleanup** — close all file handles

```
generate_logs(iterations)
    → _make_raw_directory()
    → _load_config()
    → _make_service_directories()
    → _create_files()
    → _generator_loop()
    → _close_files()
```

This separation ensures setup and cleanup live in the orchestrator,
while the loop only generates logs.

## Generation Loop — _generator_loop()

The loop produces one log per iteration. Each iteration:
1. Generates all fields (timestamp, service, metrics, level, message)
2. Formats the log line
3. Writes to the correct file via `_write_log()`

The loop does not perform setup, file management, or cleanup.

---

# Metric Generation Strategy

## Timestamp — Peak vs Off-Peak Hour Simulation

Timestamps are not generated using the current system time. Instead,
the hour component is selected using weighted randomness to simulate
realistic load patterns across the 24-hour day.

`_generate_log_timestamp(hour_weights)` uses `random.choices` with
config-driven weights to select the hour. Minutes and seconds are
generated randomly (0-59). The date is today's date, and the timezone
is UTC.

The weights follow a bell curve centered around midday — business
hours (8am-6pm) have higher weights, producing more logs during peak
hours. Overnight hours (midnight-6am) have low weights, producing
fewer logs.

```yaml
hour_of_day_weights:
  - 1   # 00:00
  - 2   # 01:00
  - 3   # 02:00
  - 4   # 03:00
  - 5   # 04:00
  - 6   # 05:00
  - 7   # 06:00
  - 8   # 07:00
  - 9   # 08:00
  - 10  # 09:00
  - 11  # 10:00
  - 12  # 11:00
  - 12  # 12:00
  - 11  # 13:00
  - 10  # 14:00
  - 9   # 15:00
  - 8   # 16:00
  - 7   # 17:00
  - 6   # 18:00
  - 5   # 19:00
  - 4   # 20:00
  - 3   # 21:00
  - 2   # 22:00
  - 1   # 23:00
```

### Design Decisions

- **Config-driven weights per hour.** Each of the 24 hours has an
  explicit weight in `config.yaml`. This gives full control over the
  load distribution — adjusting a single hour's weight does not
  require code changes.

- **24 individual hours, not grouped periods.** The `hour_of_day`
  feature in the feature engineering module produces values 0-23.
  Matching the granularity of the weights to the feature ensures
  the ML model can detect patterns at the same resolution.

- **Uses `random.choices` with weights.** Same pattern used in
  `_determine_level` — consistent approach to weighted randomness
  across the generator.

- **Date is today, not randomized.** The simulation generates logs
  as if they happened today at various hours. Randomizing the date
  is deferred — the current focus is hour-of-day patterns, not
  multi-day trends.

## CPU

Generated randomly between 30 and 70.

## Memory

Generated randomly between 40 and 75.

## Response Time — Correlated with CPU and Memory

Response time is not generated independently. It depends on both CPU
and memory load to introduce realistic correlations that ML models can
later detect. The function evaluates the **worst case** of the two
metrics — if either CPU or memory is high, response time is high.

Thresholds are read from `metric_thresholds` in `config.yaml`, reusing
the same boundaries used by the analysis layer for bucketing. This
ensures the generator and the analysis layer share a consistent
definition of "low", "normal", and "high".

```
cpu > normal OR mem > normal     → response_time 801–1200 ms  (high)
cpu > low OR mem > low           → response_time 501–800 ms   (medium)
otherwise                        → response_time 200–500 ms   (low)
```

The worst-case-first evaluation order ensures that a high value in
either metric produces a high response time, regardless of the other.
This models real system behavior where either CPU saturation or memory
pressure alone can degrade performance.

### Design Decisions

- **Config-driven thresholds.** Previously the thresholds were
  hardcoded (`cpu < 50`, `cpu 50-69`, `cpu >= 70`). Now they come
  from `metric_thresholds` in the config, which are the same
  boundaries used by `pd.cut()` in the analysis layer.

- **Worst-case evaluation.** Using `or` between CPU and memory
  conditions ensures the response time reflects the worst of the
  two metrics. This is realistic — a server with low CPU but
  saturated memory still responds slowly.

- **Memory as second factor.** Adding memory as a correlated factor
  enriches the dataset for ML. The `cpu_mem_ratio` feature in the
  feature engineering module now captures a meaningful relationship
  instead of noise.

## User

Generated randomly between 1 and 100.

---

# Level Determination — Thresholds and Probabilities

Log level is a **consequence** of system metrics, not an independent random value.

`_determine_level(response_time, levels)` evaluates response time against thresholds and applies weighted probabilities to simulate realistic variability.

```
response_time < 600      → 100% INFO

600 <= response_time < 900 →
    80% INFO
    20% WARNING

response_time >= 900     →
    50% WARNING
    50% ERROR
```

Using probabilities instead of hard thresholds ensures the dataset is not artificially perfect. A system under moderate load will mostly produce INFO logs but occasionally generate WARNING — which is how real systems behave.

Implementation uses `random.choices()` with `weights` parameter.

---

# Execution Behavior

The script includes a proper execution guard with `argparse` support:

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Log generator",
        description="Program to generate airline shopping, pricing and booking logs",
    )
    parser.add_argument(
        "-c", "--count", type=int, default=1, help="number of logs you wanna generate"
    )
    arguments = parser.parse_args()
    number_of_logs = arguments.count
    generate_logs(number_of_logs)
```

This ensures log generation runs only when the script is executed directly, not when imported as a module.

The number of logs to generate is controlled via the `-c` / `--count` argument:

```bash
python scripts/log_generator.py -c 1000
```

If no argument is provided, the default is 1 log.

---

# Directory Management

## `_make_raw_directory()`

Creates `data/raw/` dynamically if it does not exist.

Uses `pathlib` for OS-independent path resolution. Resolves the project root using `__file__` to ensure portability across environments including Docker.

## `_make_service_directories(raw_dir, services)`

Creates one subdirectory per service inside `data/raw/`.

```
data/raw/
    shopping/
    pricing/
    booking/
```

Services are read from config, not hardcoded.

---

# Log Persistence

## File Handle Management

File handles are managed with a lifecycle approach:

1. `_create_files()` opens one file per service before the generation
   loop starts, storing the handles in a dict keyed by service name
2. `_write_log()` accesses the correct handle using the service name
   as key and writes a single line
3. `_close_files()` closes all handles after the loop completes

This avoids opening and closing files on every write — with 1000 logs,
the previous approach performed 1000 open/close cycles. The current
approach opens 3 files once and closes them once.

### File Naming

Each execution run writes to a timestamped file per service:

```
data/raw/shopping/shopping_<run_timestamp>.log
data/raw/pricing/pricing_<run_timestamp>.log
data/raw/booking/booking_<run_timestamp>.log
```

The run timestamp is generated once at the start of `generate_logs()` and shared across all writes in that run. This groups all logs from a single execution into identifiable files.

Files are opened in append mode to avoid overwriting existing logs.

---

# Changes from v5

- `_generate_log_timestamp()` now receives `hour_weights` parameter —
  hour is selected via `random.choices` with config-driven weights
  instead of using `datetime.now()`
- Timestamp uses `date.today()` for the date component and
  `datetime.combine()` to assemble date + time
- Added `hour_of_day_weights` to `config.yaml` — 24 weights defining
  the load distribution across hours of the day
- `_generator_loop()` updated to pass `raw_data["hour_of_day_weights"]`
  to `_generate_log_timestamp()`
- Metric Generation Strategy section expanded with Timestamp section
  documenting peak/off-peak simulation
- "Peak vs off-peak hour simulation" removed from Future Improvements
  — resolved

---

# Changes from v4

- `_generate_response_time()` now receives `cpu`, `mem`, and
  `thresholds` — response time is correlated with both CPU and
  memory load
- Thresholds for response time bands are config-driven from
  `metric_thresholds` instead of hardcoded values
- Worst-case evaluation: `or` logic ensures either high CPU or
  high memory produces high response time
- `_generator_loop()` updated to pass `mem` and
  `raw_data["metric_thresholds"]` to `_generate_response_time()`
- Metric Generation Strategy section rewritten to document
  dual-factor correlation
- "Memory as second factor influencing response time" removed from
  Future Improvements — resolved

---

# Changes from v3

- Config key `services` renamed to `service` — matches the column name
  in the log format and the DataFrame, enabling the pipeline to use
  config keys directly as column names for categorical validation
- Config key `levels` renamed to `level` — same rationale as above
- All internal references updated: `raw_data["service"]`,
  `raw_data["level"]`, `data.get("service")`, `data.get("level")`

---

# Changes from v2

- `load_config()` now returns a dict instead of a tuple — adding new
  config fields no longer breaks existing call sites
- Config key `message_type` renamed to `level` — consistent naming
  throughout the module
- `determine_level()` parameter renamed from `messages` to `levels`
- `generate_logs()` refactored into setup orchestrator +
  `_generator_loop()` — clear separation of concerns
- File I/O changed from open/close per write to lifecycle-managed
  file handles with `_create_files()` / `_write_log()` / `_close_files()`
- All helper functions prefixed with `_` to signal private scope

---

# Future Improvements (Planned)

- Service-specific instability modeling
- Temporal correlation between consecutive events
- Large-scale log generation for dataset creation
- Session-based correlation between services — introduce a `session_id`
  to tie shopping, pricing, and booking events from the same user session
  together, enabling session-level analysis and abandonment detection
- Better config path resolution using an environment variable (Month 6)
