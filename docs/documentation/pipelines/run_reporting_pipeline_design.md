# Run Reporting Pipeline — Design (v3)

## Objective

Orchestrate the reporting workflow for the log analysis pipeline.
Receives a DataFrame, delegates to report-specific functions that
prepare data and generate visualizations, and persists all output
to disk.

---

# System Context

The reporting pipeline sits between the analysis layer and the file
system. It connects analytical functions with the visualizer and
handles output persistence.

```
main.py → run_report_pipeline.py → log_analysis.py → log_visualizer.py → output/plots/
```

---

# File Location

```
pipelines/run_reporting_pipeline.py
```

---

## Function: _make_output_directory()

### Parameters

- None

### Returns

- `Path` — path to the output directory for plots

### Implementation Details

- Uses `pathlib` for OS-independent path resolution
- Resolves the project root using `__file__`
- Creates `output/plots/` if it does not exist using `mkdir(parents=True, exist_ok=True)`

### Design Decisions

- Directory creation is handled inside the pipeline because the pipeline
  is responsible for persistence — it needs to guarantee the output
  location exists before saving

---

## Function: run_report_pipeline()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns

- None — output is saved to disk

### Implementation Details

- Calls `_make_output_directory()` once to get the output path
- Collects all report results into a single dict mapping filenames
  to Figure objects
- Calls each report function (`_count_report`, `_corr_report`,
  `_dist_report`) which return `{filename: Figure}` dicts
- Merges results using `dict.update()`
- Iterates over the collected dict and saves each figure to disk
  using `figure.savefig()`

### Pipeline Flow

```
1. _make_output_directory()                     → Path
2. _count_report(df, "level")                   → {filename: Figure}
3. _count_report(df, "service")                 → {filename: Figure}
4. _corr_report(df)                             → {filename: Figure}
5. _dist_report(df, "response_time")            → {filename: Figure}
6. _dist_report(df, "cpu")                      → {filename: Figure}
7. _dist_report(df, "mem")                      → {filename: Figure}
8. for each figure → figure.savefig(path)       → output/plots/
```

### Design Decisions

- **Dict as collector pattern.** Each report function returns a
  `{filename: Figure}` dict. The orchestrator merges them all and
  saves in a single loop. This separates report generation from
  file persistence — the report functions do not need to know about
  paths or directories.

- **Runs all reports every time.** The orchestrator calls all report
  functions unconditionally. Selective report execution is deferred
  to future work — the current set of 6 reports is small enough
  that running all of them is acceptable.

- **One save loop instead of saving in each function.** Persistence
  is the orchestrator's responsibility. Report functions focus on
  preparing data and generating figures. This is the same separation
  of concerns used across the pipeline.

---

## Function: _count_report()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `metric_name` — string identifying the categorical column to count

### Returns

- `dict[str, Figure]` — single-entry dict mapping the filename to
  the generated Figure

### Implementation Details

- Generates a dynamic filename using the metric name:
  `f"{metric_name}_count_plot.png"`
- Calls `plot_count_metric()` from the visualizer with the DataFrame
  and metric name
- Returns the filename-figure pair as a dict

### Design Decisions

- **Dynamic filename from metric name.** The function is called
  multiple times with different metrics (level, service). A hardcoded
  filename would cause the second call to overwrite the first.

---

## Function: _corr_report()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns

- `dict[str, Figure]` — single-entry dict mapping the filename to
  the generated Figure

### Implementation Details

- Calls `convert_corr_matrix()` from the analysis layer to compute
  the Pearson correlation matrix
- Passes the matrix to `plot_correlation()` from the visualizer
- Returns the filename-figure pair as a dict

### Design Decisions

- **Correlation computation happens in the analysis layer.** The
  report function orchestrates the call to `convert_corr_matrix()`
  and passes the result to the visualizer. This maintains the
  separation: analysis computes, visualizer draws, pipeline connects.

---

## Function: _dist_report()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `metric_name` — string identifying the numeric column to plot

### Returns

- `dict[str, Figure]` — single-entry dict mapping the filename to
  the generated Figure

### Implementation Details

- Calls `plot_distribution()` from the visualizer with the DataFrame
  and column name
- Returns the filename-figure pair as a dict

---

## Changes from v2

- Function renamed from `report_pipeline()` to
  `run_report_pipeline()` — consistent naming with other pipeline
  functions (`run_pipeline`, `run_features_pipeline`,
  `run_statistical_pipeline`)
- Added distribution reports for `cpu` and `mem` — two additional
  calls to `_dist_report()`, reusing the existing function with
  different column names
- Pipeline flow updated to reflect 6 reports instead of 4
- "Expand metric combinations" tech debt item resolved by adding
  cpu and mem distribution plots

---

# Future Improvements (Planned)

- Selective report execution — allow the caller to specify which
  reports to generate instead of running all unconditionally
- Accept output path as a parameter for flexibility
- Add a summary or metadata file alongside the plots (report date,
  service analyzed, record count)
