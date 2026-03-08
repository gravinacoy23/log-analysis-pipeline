# Log Generator — Implementation (v2)

## Objective

Implement a synthetic log generator for the airline booking backend simulation.

The goal of this phase is to:

- Define a consistent and parseable log format
- Build a modular log generation structure
- Generate valid log lines for multiple services
- Persist generated logs to disk
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

The generator loads configuration at runtime using `load_config()`, which reads the YAML file using `yaml.safe_load()`.

`safe_load()` is used instead of `yaml.load()` because it only parses data and never executes arbitrary code, making it safe for production-oriented systems.

### config.yaml structure (relevant section)

```yaml
services:
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

message_type:
  - INFO
  - WARNING
  - ERROR
```

---

# Implementation Details

## Modular Functions

The generator is structured using small, focused functions:

- `load_config()` — loads services, messages, and log levels from config.yaml
- `generate_timestamp()` — generates current UTC timestamp
- `generate_service(services)` — selects a random service from config
- `generate_message(service, message_list)` — selects a message based on service
- `generate_user()` — generates a random user ID
- `generate_cpu()` — generates a random CPU usage value
- `generate_memory()` — generates a random memory usage value
- `generate_response_time(cpu)` — generates response time correlated with CPU load
- `determine_level(response_time, message_type)` — determines log level based on response time thresholds and probabilities
- `format_log(...)` — builds the final log line string
- `make_raw_directory()` — creates `data/raw/` if it does not exist
- `make_service_directories(raw_dir, services)` — creates per-service subdirectories
- `write_log(target_path, service, run_timestamp, log_line)` — persists log line to disk
- `generate_logs(iterations)` — orchestrates the full generation pipeline

---

# Metric Generation Strategy

## CPU

Generated randomly between 30 and 70.

```python
def generate_cpu():
    return random.randint(30, 70)
```

## Response Time — Correlated with CPU

Response time is not generated independently. It depends on CPU load to introduce realistic correlation that ML models can later detect.

```
cpu < 50      → response_time 200–500 ms
cpu 50–69     → response_time 501–800 ms
cpu >= 70     → response_time 801–1200 ms
```

This ensures coherence: high CPU load produces higher response times. A log with `cpu=30` and `response_time=1100` would be incoherent and pollute the dataset.

> Future improvement: incorporate memory usage as a second factor influencing response time.

## Memory

Generated independently between 40 and 75. No correlation introduced at this stage.

## User

Generated randomly between 1 and 100.

---

# Level Determination — Thresholds and Probabilities

Log level is a **consequence** of system metrics, not an independent random value.

`determine_level(response_time, message_type)` evaluates response time against thresholds and applies weighted probabilities to simulate realistic variability.

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

The script includes a proper execution guard:

```python
if __name__ == "__main__":
    generate_logs(100)
```

This ensures log generation runs only when the script is executed directly, not when imported as a module.

---

# Directory Management

## `make_raw_directory()`

Creates `data/raw/` dynamically if it does not exist.

Uses `pathlib` for OS-independent path resolution. Resolves the project root using `__file__` to ensure portability across environments including Docker.

## `make_service_directories(raw_dir, services)`

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

## `write_log(target_path, service, run_timestamp, log_line)`

Each execution run writes to a timestamped file per service:

```
data/raw/shopping/shopping_<run_timestamp>.log
data/raw/pricing/pricing_<run_timestamp>.log
data/raw/booking/booking_<run_timestamp>.log
```

The run timestamp is generated once at the start of `generate_logs()` and shared across all writes in that run. This groups all logs from a single execution into identifiable files.

Files are opened in append mode to avoid overwriting existing logs.

---

# Future Improvements (Planned)

- Memory usage as a second factor influencing response time
- Peak vs off-peak hour simulation (time-based load patterns)
- Service-specific instability modeling
- Temporal correlation between consecutive events
- Large-scale log generation for dataset creation
- Implement a better way to resolve the path when reading the config file. ex. env variable and project constant.
