# Log Statistical Analysis — Design (v1)

## Objective

Provide the statistical analysis layer of the pipeline.
Receives a feature dataset and performs statistical operations
required for ML preparation: descriptive statistics and
train/test splitting. Each function has a single responsibility
and returns its result to the caller.

---

## System Context

The statistical analysis module sits between the feature dataset
and the ML preparation outputs. It receives a DataFrame and
produces statistical summaries and split datasets.

```
features.csv → run_statistical_pipeline.py → log_statistical_analysis.py → train/test DataFrames
```

---

## Module Location

```
src/analysis/log_statistical_analysis.py
```

---

## Dependencies

- `pandas` — DataFrame operations and descriptive statistics
- `scikit-learn` — `train_test_split` for dataset splitting

---

## Function: orchestrate_statistics()

### Parameters

- `dataset` — pandas DataFrame with feature engineering data

### Returns

- `tuple[pd.DataFrame, pd.DataFrame]` — train and test DataFrames

### Implementation Details

- Calls `_split_dataset()` to perform the train/test split
- Returns the two DataFrames as a tuple
- Does not modify the input DataFrame

### Design Decisions

- **Orchestrator pattern.** Same pattern used in
  `orchestrate_features()` — a single entry point that
  coordinates the module's functions. As new statistical
  operations are added, they are called from the orchestrator
  without changing the pipeline.

- **Returns tuple, does not persist.** The orchestrator returns
  data to the pipeline. Persistence (saving to CSV) is the
  pipeline's responsibility — same separation used across
  the project.

---

## Function: general_statistics()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns

- `pd.DataFrame` — descriptive statistics including count, mean,
  std, min, max, and percentiles (25th, 50th, 75th) for all
  numeric columns

### Implementation Details

- Wraps `df.describe()` which automatically selects numeric
  columns
- The 50th percentile is the median

### Design Decisions

- **Not called by the orchestrator.** This function is used for
  exploratory analysis during development, not as part of the
  automated pipeline. It is available for future integration
  when a statistical report pipeline is implemented.

- **Accepts any DataFrame.** The function works on both the raw
  DataFrame and the feature dataset. The caller decides which
  DataFrame to analyze.

---

## Function: _split_dataset()

### Parameters

- `dataset` — pandas DataFrame with feature engineering data

### Returns

- `tuple[pd.DataFrame, pd.DataFrame]` — train and test DataFrames

### Implementation Details

- Uses `train_test_split` from `sklearn.model_selection`
- Split ratio: 80% train, 20% test via `test_size=0.2`
- Stratified on `is_error` column to preserve class distribution
  in both sets
- `pyright: ignore` comment on the return — sklearn's type stubs
  declare the return type as `list`, but the actual return values
  are DataFrames when a DataFrame is passed as input. This is a
  known limitation of sklearn's type annotations.

### Design Decisions

- **Stratified on `is_error`.** The `is_error` column has
  imbalanced distribution — ERROR is the least common log level.
  Without stratification, a random split could produce a test set
  with a significantly different error rate than the training set.
  `stratify` ensures both sets reflect the original distribution.

- **`is_error` as the stratification target.** Although the
  feature dataset does not have a formal ML target column yet,
  `is_error` is the most likely candidate for classification
  in Phase 3. Stratifying on it now ensures the splits are
  already prepared for that use case.

- **80/20 split ratio.** Standard ratio for datasets of this
  size. The training set needs to be large enough to learn
  patterns; the test set needs to be large enough to evaluate
  reliably.

- **Private function.** The split is called by the orchestrator,
  not directly by the pipeline. This keeps the module's public
  interface clean — the pipeline interacts only with
  `orchestrate_statistics()`.

---

## Changes from v0

- Initial implementation

---

## Future Improvements (Planned)

- Add `random_state` parameter for reproducible splits
- Statistical report generation with distribution summaries
- Cross-service comparison functions
- Integration of `general_statistics()` into the orchestrator
  when a report pipeline is implemented
