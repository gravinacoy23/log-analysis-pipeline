# Log Statistical Analysis — Design (v2)

## Objective

Provide the statistical analysis layer of the pipeline.
Receives a feature dataset and performs statistical operations
required for ML preparation: descriptive statistics, train/test
splitting, and model evaluation via confusion matrix. Each
function has a single responsibility and returns its result
to the caller.

---

## System Context

The statistical analysis module sits between the feature dataset
and the ML preparation outputs. It receives a DataFrame and
produces statistical summaries, split datasets, and evaluation
metrics.

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

## Function: create_confusion_matrix()

### Parameters

- `results` — `list[bool]` of actual values (ground truth)
- `predictions` — `list[bool]` of predicted values from a model

### Returns

- `tuple[int, int, int, int]` — counts of True Positives,
  True Negatives, False Positives, and False Negatives in
  that order

### Implementation Details

- Iterates over both lists in parallel using `zip()`
- Guard clause skips any pair where either value is not a
  boolean — silent `continue`, no logging, since input comes
  from internal code not external data
- Classifies each pair into one of four categories:
  - **True Positive:** prediction is True, result is True
  - **True Negative:** prediction is False, result is False
  - **False Positive:** prediction is True, result is False
  - **False Negative:** prediction is False, result is True
- Uses idiomatic boolean checks (`if prediction` instead of
  `if prediction == True`)

### Design Decisions

- **Manual implementation instead of sklearn.** The function
  exists to build understanding of how a confusion matrix works.
  `sklearn.metrics.confusion_matrix` provides the same
  functionality but using it without understanding the mechanics
  would be vibe coding. The manual implementation stays as a
  learning artifact and is used for simulated model evaluation.

- **Returns a tuple, not a dict.** Four values in a fixed,
  documented order. The caller knows the order from the
  docstring and type hint. A dict would add overhead for a
  return value that is always the same four counters.

- **Guard clause over strict validation.** Invalid values are
  skipped silently rather than raising an error. The function
  processes internal data (boolean Series converted to lists),
  not external input. A guard clause is sufficient; a logger
  would be over-engineering for this context.

- **Not called by the orchestrator.** This function is used for
  manual model evaluation during development and analysis. It
  will be integrated into the pipeline when ML training begins
  in Phase 3.

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
- `random_state=42` for reproducible splits
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

- **`random_state=42` for determinism.** Ensures every execution
  produces the same split. Required by the project's Definition
  of Done (results reproducible). The value is hardcoded in the
  function — this is the only split in the project, so config
  externalization is unnecessary.

- **Private function.** The split is called by the orchestrator,
  not directly by the pipeline. This keeps the module's public
  interface clean — the pipeline interacts only with
  `orchestrate_statistics()`.

---

## Changes from v1

- Added `create_confusion_matrix()` — manual implementation of
  confusion matrix computation for model evaluation
- Added guard clause in confusion matrix for non-boolean values
- Updated `_split_dataset()` to include `random_state=42` for
  reproducibility (resolved bug #27)
- "Add `random_state` parameter" removed from Future Improvements
  — resolved

---

## Future Improvements (Planned)

- Statistical report generation with distribution summaries
- Cross-service comparison functions
- Integration of `general_statistics()` into the orchestrator
  when a report pipeline is implemented
- Precision, recall, and F1 score computation functions
