# Config Loader — Design (v3)

## Objective

Provide a shared configuration loading function for the pipeline.
Reads `config.yaml` and validates that all required keys exist before
returning the config to the caller.

---

# System Context

The config loader is a shared utility called by `main.py` to load
configuration for all pipelines. It is independent from the log
generator, which has its own private `_load_config()`.

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
  depends on: `service`, `level`, `columns`, `metric_thresholds`,
  `feature_thresholds`
- Iterates over `required_keys` and validates each one exists and
  is not empty using `.get()`
- Raises a descriptive `ValueError` identifying the missing key
- Returns the full dict — callers access only the keys they need

### Design Decisions

- **Returns the full dict, not individual values.** This allows adding
  new config keys without changing the loader's return type or signature.
  Callers access values by key (`config["columns"]`), which is resilient
  to changes in other parts of the config.

- **Required keys defined as a list in the function.** The list of
  keys to validate is a code-level decision, not external configuration.
  It is hardcoded because it represents what the pipeline requires —
  similar to guard clauses that encode application rules. Adding a new
  required key means adding one string to the list.

- **Loop-based validation over individual checks.** Previously each
  key was validated with a separate `if not data.get()` statement.
  The loop eliminates repetition and makes it easy to add new keys.
  The error message includes the key name via f-string, so each
  failure is still descriptive.

- **Validation uses `.get()` instead of direct key access.** If a
  required key is missing from the YAML file, `.get()` returns `None`
  instead of raising a `KeyError`. The `not` check then catches both
  missing keys and empty values (empty dicts, empty strings, `None`)
  in a single condition.

- **Separate from the generator's config loader.** The log generator
  (`scripts/log_generator.py`) has its own private `_load_config()`
  that validates generator-specific keys (service, messages, level).
  The pipeline's config loader validates pipeline-specific keys.
  The two are intentionally independent — the pipeline does not
  depend on the generator and vice versa.

- **Fail fast with descriptive errors.** If a required key is missing,
  a `ValueError` is raised immediately with a message that identifies
  which key is missing. This follows the same fail-fast principle
  applied across the project.

---

# Config Structure (pipeline-relevant section)

```yaml
service: [shopping, pricing, booking]
level: [INFO, WARNING, ERROR]
columns:
  timestamp: datetime.datetime
  service: str
  user: int
  cpu: int
  mem: int
  response_time: int
  level: str
  msg: str
metric_thresholds:
  cpu:
    low: 44
    normal: 57
    high: 70
  mem:
    low: 52
    normal: 63
    high: 75
feature_thresholds:
  high_rt: 800
  high_cpu: 70
```

All five keys are validated on load. Each key serves a different
pipeline stage:

- **`service`** — used by the generator, the pipeline for categorical
  validation, and the feature engineering module for service encoding
- **`level`** — used by the generator and the pipeline for categorical
  validation
- **`columns`** — column names for parser validation, column-to-type
  mapping for analysis layer dtype validation
- **`metric_thresholds`** — boundaries for `pd.cut()` bucketing of
  CPU and memory in the analysis layer
- **`feature_thresholds`** — boundaries for feature engineering
  (e.g. slow response time threshold)

---

# Changes from v2

- Validation refactored from single `columns` check to loop over
  `required_keys` list — validates `service`, `level`, `columns`,
  `metric_thresholds`, and `feature_thresholds`
- Error message now uses f-string to identify the specific missing key
- System context updated to reflect that `main.py` calls `load_config`,
  not `run_pipeline`
- Config structure section expanded to show all validated keys and
  their purpose
- "Validate additional pipeline config keys" removed from Future
  Improvements — resolved

---

# Future Improvements (Planned)

- Support environment variable override for config file path —
  useful for Docker and cloud deployments
- Full type validation for all data types (Month 3) — currently
  only `int` columns are validated
