# Run Reporting Pipeline — Design (v4)

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
2. _count_report(df, "method")                  → {filename: Figure}
3. _count_report(df, "http_response")           → {filename: Figure}
4. _corr_report(df)                             → {filename: Figure}
5. _dist_report(df, "response_size")            → {filename: Figure}
6. for each figure → figure.savefig(path)       → output/plots/
```

### Design Decisions

- **Dict as collector pattern.** Each report function returns a
  `{filename: Figure}` dict. The orchestrator merges them all and
  saves in a single loop. This separates report generation from
  file persistence — the report functions do not need to know about
  paths or directories.

- **Runs all reports every time.** The orchestrator calls all report
  functions unconditionally. Selective report execution is deferred
  to future work — the current set of 4 reports is small enough
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
  multiple times with different metrics. A hardcoded filename would
  cause the second call to overwrite the first.

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

## Changes from v3

- Report calls updated for CLF migration: synthetic column names
  replaced with real log columns
- `_count_report(df, "level")` → `_count_report(df, "method")` —
  HTTP method is the new categorical column worth counting
  (GET/POST/HEAD distribution)
- `_count_report(df, "service")` → `_count_report(df, "http_response")`
  — status code distribution replaces service distribution
- `_dist_report(df, "response_time")` → `_dist_report(df, "response_size")`
  — response size is the new continuous numeric column
- `_dist_report(df, "cpu")` and `_dist_report(df, "mem")` removed —
  these columns do not exist in CLF data
- Pipeline flow reduced from 6 reports to 4

---

# Future Improvements (Planned)

- Selective report execution — allow the caller to specify which
  reports to generate instead of running all unconditionally
- Accept output path as a parameter for flexibility
- Add a summary or metadata file alongside the plots (report date,
  dataset analyzed, record count)
