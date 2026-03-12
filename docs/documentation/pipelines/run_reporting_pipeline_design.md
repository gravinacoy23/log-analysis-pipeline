# Run Reporting Pipeline — Design (v1)

## Objective

Orchestrate the reporting workflow for the log analysis pipeline.
Receives a DataFrame, runs analysis, generates visualizations, and
persists output to disk.

---

# System Context

The reporting pipeline sits between the analysis layer and the file
system. It connects analytical functions with the visualizer and
handles output persistence.

```
main.py → run_reporting_pipeline.py → log_analysis.py → log_visualizer.py → output/plots/
```

---

# File Location

```
pipelines/run_reporting_pipeline.py
```

---

## Function: make_output_directory()

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

## Function: report_level_pipeline()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data

### Returns

- None — output is saved to disk

### Implementation Details

- Calls `count_by_level_all()` from `log_analysis.py` to get level counts
- Converts the resulting `pd.Series` to a `dict` using `.to_dict()`
- Passes the dict and the metric name to `plot_metric()` from `log_visualizer.py`
- Saves the returned figure to `output/plots/level_plot.png` using `figure.savefig()`

### Pipeline Flow

```
1. count_by_level_all(df)   → pd.Series
2. .to_dict()               → dict
3. plot_metric(dict, name)  → matplotlib Figure
4. figure.savefig(path)     → output/plots/level_plot.png
```

### Design Decisions

- **Series to dict conversion happens here, not in the analysis layer.**
  The reporting pipeline is the orchestrator — it adapts the output format
  of one module to the input format of another. The analysis layer should
  not need to know that the visualizer expects a dict. The visualizer should
  not need to know that the data comes from pandas.

- **Function is specific to level counts, not generic.** The function is
  named `report_level_pipeline()` and hardcodes the call to
  `count_by_level_all()` and the metric name `"level"`. This is intentional
  — generalizing the reporting pipeline before having multiple report types
  would be designing with incomplete information. When Month 2 introduces
  additional reports, the pattern will emerge and refactoring can happen
  with confidence.

- **Saves output to disk directly.** Unlike `plot_metric()` which returns
  a figure without deciding what to do with it, the reporting pipeline's
  job is to produce a deliverable. Saving to disk is part of that
  responsibility.

---

# Future Improvements (Planned)

- Generalize to support additional report types (by service, response
  time distribution, etc.) when Month 2 introduces more analysis work
- Accept output path as a parameter for flexibility
- Add a summary or metadata file alongside the plot (report date,
  service analyzed, record count)
