# Config Loader — Design (v5)

## Objective

Provide a shared configuration loading function for the pipeline.
Reads `config.yaml` and validates that all required keys exist before
returning the config to the caller.

---

# System Context

The config loader is a shared utility called by `main.py` to load
configuration for all pipelines.

```
config/config.yaml → config_loader.py → main.py → (passes config to pipelines)
```

---

# Module Location

```
src/config_loader.py
```

---

## Function: load_config()

### Parameters

- None

### Returns

- `dict` — the full config dictionary as loaded from `config.yaml`

### Implementation Details

- Resolves the config file path using `pathlib` relative to `__file__`
- Reads and parses the YAML file using `yaml.safe_load()`
- Defines a `required_keys` list containing all keys the pipeline
  depends on: `paths`, `columns`, `expected_values`,
  `metric_thresholds`
- Iterates over `required_keys` and validates each one exists and
  is not empty using `.get()`
- Raises a descriptive `ValueError` identifying the missing key
- Returns the full dict — callers access only the keys they need

### Design Decisions

- **Returns the full dict, not individual values.** This allows adding
  new config keys without changing the loader's return type or signature.
  Callers access values by key, which is resilient to changes in other
  parts of the config.

- **Required keys updated for CLF metric thresholds.** The required
  keys are now:
  - `paths` — log directory location
  - `columns` — column names and types for parser and analysis
  - `expected_values` — valid values and ranges for content
    validation
  - `metric_thresholds` — threshold boundaries for computed
    bucket columns (e.g. response_size)

- **Loop-based validation over individual checks.** The loop
  eliminates repetition and makes it easy to add new keys. The
  error message includes the key name via f-string, so each
  failure is still descriptive.

- **Validation uses `.get()` instead of direct key access.** If a
  required key is missing from the YAML file, `.get()` returns `None`
  instead of raising a `KeyError`. The `not` check then catches both
  missing keys and empty values in a single condition.

- **Fail fast with descriptive errors.** If a required key is missing,
  a `ValueError` is raised immediately with a message that identifies
  which key is missing.

---

# Config Structure (current)

```yaml
paths:
  raw_log: data/raw/access_logs/
  output_dir: output/

columns:
  host: str
  identity: str
  user: str
  timestamp: datetime.datetime
  method: str
  endpoint: str
  protocol_version: str
  http_response: int
  response_size: int

expected_values:
  method:
    - GET
    - POST
    - HEAD
  protocol_version:
    - HTTP/1.0
  http_response:
    - 100
    - 599

metric_thresholds:
  response_size:
    low: 669
    normal: 9200
    high: max
```

Each key serves a different pipeline stage:

- **`paths`** — used by the reader to locate log files on disk
- **`columns`** — column names for parser field mapping, column-to-type
  mapping for analysis layer dtype validation
- **`expected_values`** — valid values for categorical columns
  (method, protocol_version) and valid range for numeric columns
  (http_response) used by the analysis layer for content validation
- **`metric_thresholds`** — threshold boundaries for computed
  bucket columns, used by `get_metric_thresholds()` in the
  analysis layer via `run_pipeline`

---

# Deprecated Config Keys

| Key | Reason |
|---|---|
| `service` | Per-service directory structure removed |
| `level` | Log levels do not exist in CLF |
| `feature_thresholds` | Features being redesigned in Month 6 |
| `hour_of_day_weights` | Generator-specific — generator deprecated |

---

# Changes from v4

- `metric_thresholds` added back to `required_keys` — new
  thresholds defined for `response_size` with CLF-relevant
  boundaries (low: 669, normal: 9200, high: max)
- Config structure section updated to include `metric_thresholds`
  with the current response_size configuration
- `metric_thresholds` removed from deprecated keys table — it
  is now active again with new content
- Deprecated keys table updated: `metric_thresholds` removed,
  remaining deprecated keys kept for reference

---

# Future Improvements (Planned)

- Support environment variable override for config file path —
  useful for Docker and cloud deployments
