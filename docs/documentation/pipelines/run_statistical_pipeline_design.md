# Run Statistical Pipeline — Design (v1)

## Objective

Orchestrate the statistical analysis workflow for the log analysis
pipeline. Loads the feature dataset from disk, delegates statistical
operations to the analysis module, and persists the resulting
train/test splits to disk as CSV.

---

## System Context

The statistical pipeline sits between the feature dataset on disk
and the statistical analysis module. It handles loading, delegates
analysis, and persists outputs.

```
main.py → run_statistical_pipeline.py → log_statistical_analysis.py → output/datasets/
```

---

## File Location

```
pipelines/run_statistical_pipeline.py
```

---

## Function: run_statistical_pipeline()

### Parameters

- None

### Returns

- None — output is saved to disk

### Implementation Details

- Calls `_get_directory()` to resolve the datasets path
- Calls `_load_features_dataset()` to load `features.csv`
- Calls `orchestrate_statistics()` which returns train and test
  DataFrames as a tuple
- Persists both DataFrames to CSV using `.to_csv()` with
  `index=False`
- Output files: `training_data.csv` and `test_data.csv`

### Pipeline Flow

```
1. _get_directory()                              → Path
2. _load_features_dataset(path)                  → DataFrame
3. orchestrate_statistics(dataset)               → (train_df, test_df)
4. train_df.to_csv(path / "training_data.csv")   → output/datasets/
5. test_df.to_csv(path / "test_data.csv")         → output/datasets/
```

### Design Decisions

- **No parameters.** Unlike `run_pipeline` and
  `run_features_pipeline` which receive config and DataFrames
  from `main.py`, this pipeline is self-contained. It loads its
  own input from disk because the feature dataset is already
  persisted by a previous pipeline stage. This avoids coupling
  the statistical pipeline to the features pipeline's return
  value.

- **Reuses the same output directory.** Train and test sets are
  saved alongside `features.csv` in `output/datasets/`. They
  are derived from the feature dataset and belong in the same
  location. No new directory creation is needed.

- **`index=False` on CSV persistence.** Same rationale as
  `run_features_pipeline` — the pandas index has no relationship
  to the data.

- **Called by `main.py` after `run_features_pipeline`.** The
  execution order matters: the feature dataset must exist on disk
  before this pipeline runs. `main.py` ensures the sequence:
  data pipeline → reporting pipeline → features pipeline →
  statistical pipeline.

---

## Function: _get_directory()

### Parameters

- None

### Returns

- `Path` — path to the datasets output directory

### Implementation Details

- Resolves `output/datasets/` relative to the project root
  using `pathlib` and `__file__`
- Validates that the directory exists using `is_dir()`
- Raises `ValueError` if the directory does not exist

### Design Decisions

- **Validates existence instead of creating.** Unlike
  `_make_output_directory()` in other pipelines which create
  directories with `mkdir()`, this function expects the directory
  to already exist — it was created by `run_features_pipeline`.
  If the directory is missing, it means the features pipeline did
  not run, which is a pipeline ordering error that should surface
  immediately.

- **Single function for path resolution.** The same path is used
  to load the input dataset and to save the output splits. Having
  one function that returns the path avoids resolving it twice
  and ensures consistency.

---

## Function: _load_features_dataset()

### Parameters

- `directory` — `Path` to the datasets directory

### Returns

- `pd.DataFrame` — the feature dataset loaded from CSV

### Implementation Details

- Constructs the full path as `directory / "features.csv"`
- Reads the CSV using `pd.read_csv()`

### Design Decisions

- **Receives directory as parameter.** The directory is resolved
  once by `_get_directory()` and passed to both the loader and
  the persistence step. This keeps path resolution in one place.

- **Loading is the pipeline's responsibility.** The statistical
  analysis module receives a DataFrame — it does not know where
  the data came from. Same decoupling pattern used across the
  project.

---

## Changes from v0

- Initial implementation

---

## Future Improvements (Planned)

- Accept output path as parameter for flexibility
- Log summary of persisted datasets (row count per split)
- Configurable split parameters (test_size, random_state) via
  config.yaml
