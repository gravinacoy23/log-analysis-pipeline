# Log Visualizer Module — Design (v2)

## Objective

Provide the visualization layer of the pipeline.
Receives data from the analysis layer and produces matplotlib/seaborn
figures ready to be saved or displayed by the caller. Supports
categorical count plots, numeric distribution histograms, and
correlation heatmaps.

---

## System Context

The visualizer sits at the end of the analysis chain. It receives
data and produces visual output. It does not know where the data
came from or what will be done with the figure — that is the
responsibility of the layers above.

```
log_analysis.py → DataFrame / correlation matrix → log_visualizer.py → matplotlib Figure
```

---

## Module Location

```
src/analysis/log_visualizer.py
```

---

## Dependencies

- `matplotlib` — figure and axes management, saving figures
- `seaborn` — statistical plots (countplot, histplot, heatmap)

---

## Function: plot_count_metric()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `metric` — string identifying the categorical column to count
  (e.g. `"level"`, `"service"`)

### Returns

- `matplotlib.figure.Figure` — the complete figure object, ready to
  be saved to disk or displayed

### Implementation Details

- Uses `plt.subplots()` to create `fig` and `ax` explicitly
- Calls `sns.countplot()` with `x=metric`, `data=logs_dataframe`,
  and `ax=ax` to draw on the explicit axes
- Seaborn handles tick positioning and labeling automatically —
  no manual `set_xticks()` or `set_xticklabels()` needed
- Title and axis labels are derived from `metric`

### Design Decisions

- **Receives a DataFrame, not a dict.** Unlike the previous
  `plot_metric()` which received pre-processed dicts to stay
  decoupled from pandas, seaborn functions need the raw DataFrame
  to perform their own counting internally. Passing pre-counted
  data would defeat the purpose of using seaborn. Since the
  visualizer now uses seaborn for all plots, pandas is already
  a dependency of the module — maintaining dict-based decoupling
  for individual functions would be inconsistent.

- **Replaces `plot_metric()`.** The previous function required the
  caller to pre-compute counts and convert to dict before calling.
  `plot_count_metric()` produces the same result with less work
  from the caller. With seaborn as a module dependency, keeping
  both functions would be redundant.

- **Generic across categorical columns.** The `metric` parameter
  accepts any categorical column name, making the function reusable
  for level counts, service counts, or any future categorical field.

---

## Function: plot_distribution()

### Parameters

- `logs_dataframe` — pandas DataFrame with parsed log data
- `column_name` — string identifying the numeric column to plot
  (e.g. `"response_time"`)

### Returns

- `matplotlib.figure.Figure` — the complete figure object

### Implementation Details

- Uses `plt.subplots()` to create `fig` and `ax` explicitly
- Calls `sns.histplot()` with `x=column_name`, `data=logs_dataframe`,
  and `ax=ax`
- Seaborn automatically bins the numeric data and displays the
  distribution as a histogram
- Title and axis labels are derived from `column_name`

### Design Decisions

- **Separate function from `plot_count_metric()`.** Both produce
  bar-like visuals, but they answer different questions.
  `countplot` counts occurrences of discrete categories.
  `histplot` shows the distribution of continuous numeric data
  by binning values into ranges. The distinction matters
  conceptually even if the visual output looks similar.

- **Caller is responsible for passing a numeric column.** The
  function does not validate that `column_name` refers to a
  numeric column. The pipeline orchestrator selects the column,
  so validation at this level would be redundant.

---

## Function: plot_correlation()

### Parameters

- `corr_matrix` — pandas DataFrame containing a correlation matrix
  as produced by `convert_corr_matrix()` in `log_analysis.py`

### Returns

- `matplotlib.figure.Figure` — the complete figure object

### Implementation Details

- Uses `plt.subplots()` to create `fig` and `ax` explicitly
- Calls `sns.heatmap()` with the correlation matrix and `ax=ax`
- Seaborn renders column names on both axes automatically
- Title is set on the axes; axis labels are omitted because the
  heatmap axes already display the column names

### Design Decisions

- **Receives the correlation matrix, not the raw DataFrame.** The
  computation of `select_dtypes()` and `.corr()` is an analytical
  operation that belongs in the analysis layer. The visualizer only
  draws the result. This follows the same separation used across
  the pipeline: analysis calculates, visualizer draws.

- **No axis labels.** The heatmap inherits row and column names
  from the correlation matrix DataFrame. Adding explicit axis labels
  would duplicate information already visible on the plot.

---

## Shared Design Decisions

- **Returns a Figure, does not save or display.** Every function's
  responsibility is to create the visualization, not to decide where
  it goes. Saving to disk or calling `plt.show()` is the caller's
  decision — following the same single-responsibility pattern used
  across the pipeline.

- **Explicit `fig, ax` over implicit `plt` calls.** Using
  `plt.subplots()` gives explicit control over the figure and axes
  objects. This allows the function to return the figure, pass `ax`
  to seaborn, and avoids relying on matplotlib's implicit global
  state.

- **Seaborn draws on explicit axes via `ax=ax`.** Seaborn functions
  accept an `ax` parameter that specifies which axes object to draw
  on. This integrates cleanly with the `fig, ax` pattern and keeps
  all drawing within the explicitly managed figure.

---

## Changes from v1

- Removed `plot_metric()` — replaced by `plot_count_metric()` which
  uses seaborn and receives a DataFrame directly
- Added `plot_count_metric()` — seaborn countplot for categorical
  columns (level, service)
- Added `plot_distribution()` — seaborn histplot for numeric column
  distributions (response_time)
- Added `plot_correlation()` — seaborn heatmap for correlation matrices
- Module now depends on seaborn in addition to matplotlib
- Visualizer now accepts DataFrames instead of dicts — seaborn requires
  raw data to perform its own statistical computations
- "Support additional plot types" removed from Future Improvements —
  resolved with the three new functions

---

## Future Improvements (Planned)

- Color customization per category (e.g. red for ERROR, yellow
  for WARNING)
- Annotation support for heatmap cells (display correlation values)
- Support for saving figures directly if a path is provided
  (optional parameter, not mandatory)
