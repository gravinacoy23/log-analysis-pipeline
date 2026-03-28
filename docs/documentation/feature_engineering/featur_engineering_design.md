# Feature Engineering Module — Design (v2)

## Objective

Provide the feature engineering layer of the pipeline.
Receives a validated DataFrame and produces derived features
suitable for ML model consumption. Each feature function returns
an independent Series; the orchestrator assembles them into a
single DataFrame.

---

## System Context

The feature engineering module sits between the analysis layer
and the persistence layer. It receives a validated DataFrame
and produces a new DataFrame containing context columns and
derived features.

```
log_analysis.py → DataFrame → feature_engineering.py → Feature DataFrame → pipeline persists to CSV
```

---

## Module Location

```
src/features/feature_engineering.py
```

---

## Dependencies

- `pandas` — Series creation and DataFrame assembly

---

## Function: orchestrate_features()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data
- `thresholds` — dict mapping threshold names to int values,
  loaded from `config.yaml` under `feature_thresholds`
- `services` — list of service names from `config.yaml`, used
  to derive the numeric encoding for `service_encoded`

### Returns

- `pd.DataFrame` — new DataFrame containing context columns
  and all derived feature columns

### Implementation Details

- Defines context columns (timestamp, service, user) and
  delegates extraction to `_context_cols()`
- Calls each feature function independently
- Collects all results (context DataFrame and feature Series)
  into a list
- Assembles the final DataFrame using `pd.concat(features_list, axis=1)`
- Does not modify the input DataFrame

### Design Decisions

- **Returns a new DataFrame, does not mutate the original.**
  The feature dataset is a distinct artifact from the validated
  log DataFrame. Keeping them separate ensures the analysis
  pipeline and the feature pipeline do not interfere with each
  other.

- **Orchestrator assembles, feature functions produce.** Each
  feature function returns a single Series. The orchestrator
  decides how to combine them. Adding a new feature requires
  writing one function and appending one line in the
  orchestrator — the pipeline does not change.

- **List collector pattern with pd.concat.** Same conceptual
  pattern as the dict collector in `report_pipeline()` — collect
  results from individual functions, combine in a single step
  at the end.

---

## Function: _context_cols()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data
- `cols` — list of column names to extract as context

### Returns

- `pd.DataFrame` — subset of the original DataFrame containing
  only the specified context columns

### Implementation Details

- Uses list-based column indexing on the DataFrame
- Returns a DataFrame, not a Series — list indexing always
  returns a DataFrame regardless of the number of columns

### Design Decisions

- **Context columns defined in the orchestrator, not hardcoded
  in the function.** The function receives the column list as a
  parameter, keeping it reusable. The orchestrator owns the
  decision of which columns provide context.

- **Separate function instead of inline extraction.** Extracting
  context columns is a distinct responsibility from deriving
  features. A dedicated function keeps the orchestrator readable
  and follows the same pattern as the feature functions.

---

## Function: _is_error()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data

### Returns

- `pd.Series` — boolean Series named `"is_error"`, `True` where
  `level == "ERROR"`

### Implementation Details

- Uses boolean comparison on the `level` column
- Renames the resulting Series using `.rename()` to avoid
  inheriting the source column name

### Design Decisions

- **No threshold needed.** ERROR is a fixed categorical value,
  not a configurable boundary. The condition is deterministic.

---

## Function: _is_slow()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data
- `rt_threshold` — integer threshold from config defining what
  constitutes a slow response time

### Returns

- `pd.Series` — boolean Series named `"is_slow"`, `True` where
  `response_time >= rt_threshold`

### Implementation Details

- Uses boolean comparison with a config-driven threshold
- Threshold is passed as a parameter, not read from config
  directly — the orchestrator extracts and passes it

### Design Decisions

- **Config-driven threshold.** What counts as "slow" is a
  business decision that may change. Externalizing it to
  `config.yaml` under `feature_thresholds.high_rt` makes
  the transformation reproducible and adjustable without
  code changes.

- **Receives threshold as parameter, not config dict.** The
  function does not need to know the config structure — it
  receives a single int. The orchestrator handles extraction
  from the config. Same decoupling pattern used across the
  pipeline.

---

## Function: _hour_of_day()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data

### Returns

- `pd.Series` — integer Series named `"hour_of_day"`, values
  0–23 representing the hour extracted from the timestamp

### Implementation Details

- Uses the `.dt.hour` accessor on the timestamp column
- Renames the resulting Series using `.rename()`

### Design Decisions

- **Hour only, no minutes or seconds.** The purpose of this
  feature is to detect load patterns by time of day (peak vs
  off-peak). Minutes and seconds add noise without signal —
  both 14:37:22 and 14:12:45 belong to the same hourly
  pattern. The 0–23 range gives 24 distinct buckets.

---

## Function: _service_encoded()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data
- `services` — list of service names from config

### Returns

- `pd.Series` — integer Series named `"service_encoded"`,
  mapping each service name to a numeric value starting at 1

### Implementation Details

- Builds a mapping dict from the services list using
  `enumerate(services, start=1)`
- Applies the mapping to the `service` column using
  `.map(services_map)`
- Renames the resulting Series using `.rename()`

### Design Decisions

- **Mapping derived from config list, not hardcoded.** The
  services list already exists in `config.yaml`. Using
  `enumerate` on that list produces the mapping automatically.
  If a service is added or removed, the encoding updates
  without code changes.

- **Starts at 1, not 0.** Avoids ambiguity — 0 could be
  confused with a missing or default value in downstream
  analysis.

- **Receives the services list, not the full config.** Same
  decoupling pattern as `_is_slow` — the function does not
  know the config structure. The orchestrator extracts and
  passes only what is needed.

---

## Function: _cpu_mem_ratio()

### Parameters

- `logs_dataframe` — pandas DataFrame with validated log data

### Returns

- `pd.Series` — float Series named `"cpu_mem_ratio"`,
  representing the ratio of CPU usage to memory usage

### Implementation Details

- Divides the `cpu` column by the `mem` column element-wise
- Renames the resulting Series using `.rename()`

### Design Decisions

- **Ratio as a derived feature.** CPU and memory individually
  tell part of the story. Their ratio captures the relationship
  between the two — a high CPU with low memory is a different
  signal than high CPU with high memory. This gives ML models
  an additional dimension without adding new raw data.

- **No threshold or config needed.** The ratio is a pure
  mathematical derivation with no configurable boundary.

---

## Config Structure

```yaml
feature_thresholds:
  high_rt: 800
  high_cpu: 70
```

The orchestrator reads `feature_thresholds` from the config
and extracts individual values for each feature function.

---

## Changes from v1

- Added `services` parameter to `orchestrate_features()` —
  needed for `_service_encoded()` mapping
- Added `_hour_of_day()` — extracts hour from timestamp
- Added `_service_encoded()` — numeric encoding derived from
  config service list using `enumerate`
- Added `_cpu_mem_ratio()` — CPU / memory ratio as derived
  numeric feature
- All 5 planned features now implemented
- "Context columns in final dataset" removed from Future
  Improvements — resolved in v1 with `_context_cols()`

---

## Future Improvements (Planned)

- Pipeline integration and CSV persistence
- Feature documentation describing ML relevance per feature
