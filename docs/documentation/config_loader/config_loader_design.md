# Config Loader — Design (v2)

## Objective

Provide a shared configuration loading function for the pipeline.
Reads `config.yaml` and validates that required keys exist before
returning the config to the caller.

---

# System Context

The config loader is a shared utility used by pipeline modules that
need access to configuration values. It is independent from the log
generator, which has its own private `_load_config()`.

```
config/config.yaml → config_loader.py → run_pipeline.py → (passes values to modules)
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
- Validates that the `columns` key exists and is not empty
- Returns the full dict — callers access only the keys they need

### Design Decisions

- **Returns the full dict, not individual values.** This allows adding
  new config keys without changing the loader's return type or signature.
  Callers access values by key (`config["columns"]`), which is resilient
  to changes in other parts of the config.

- **Validation uses `.get()` instead of direct key access.** If a
  required key is missing from the YAML file, `.get()` returns `None`
  instead of raising a `KeyError`. The `not` check then catches both
  missing keys and empty values (empty dicts, empty strings, `None`)
  in a single condition.

- **Separate from the generator's config loader.** The log generator
  (`scripts/log_generator.py`) has its own private `_load_config()`
  that validates generator-specific keys (service, messages, level).
  The pipeline's config loader validates pipeline-specific keys
  (columns). The two are intentionally independent — the pipeline
  does not depend on the generator and vice versa.

- **Fail fast with descriptive errors.** If a required key is missing,
  a `ValueError` is raised immediately with a message that identifies
  what is missing.

---

# Config Structure (pipeline-relevant section)

```yaml
columns:
  timestamp: datetime.datetime
  service: str
  user: int
  cpu: int
  mem: int
  response_time: int
  level: str
  msg: str
```

The `columns` key is a dictionary mapping column names to their
expected data types. This structure serves two purposes:

- **Column name extraction.** The pipeline orchestrator extracts
  column names using `.keys()` and passes them as a `list[str]` to
  the parser for field presence validation.
- **Type validation.** The full dict is passed to the analysis layer's
  `convert_to_dataframe()` which validates that numeric columns
  contain the correct data types before creating the DataFrame.

---

# Changes from v1

- `columns` changed from a list of strings to a dict mapping column
  names to expected data types — enables type validation in the
  analysis layer without requiring a separate config key
- Config structure section updated to reflect the new format

---

# Future Improvements (Planned)

- Validate additional pipeline config keys as the project grows
  (e.g. thresholds in Month 3, cloud config in Month 5)
- Support environment variable override for config file path —
  useful for Docker and cloud deployments
- Full type validation for all data types (Month 3) — currently
  only `int` columns are validated
