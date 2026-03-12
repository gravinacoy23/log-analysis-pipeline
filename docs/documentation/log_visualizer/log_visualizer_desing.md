# Log Visualizer Module — Design (v1)

## Objective

Provide the visualization layer of the pipeline.
Receives structured metric data as a dictionary and produces
matplotlib figures ready to be saved or displayed by the caller.

---

## System Context

The visualizer sits at the end of the analysis chain. It receives
processed data and produces visual output. It does not know where
the data came from or what will be done with the figure — that is
the responsibility of the layers above.

```
log_analysis.py → dict → log_visualizer.py → matplotlib Figure
```

---

## Module Location

```
src/analysis/log_visualizer.py
```

---

## Function: plot_metric()

### Parameters

- `metric_dict` — dictionary with category names as keys and numeric
  values as values (e.g. `{"INFO": 150, "WARNING": 30, "ERROR": 12}`)
- `metric_name` — string identifying the metric being plotted (e.g.
  `"level"`, `"service"`)

### Returns

- `matplotlib.figure.Figure` — the complete figure object, ready to
  be saved to disk or displayed

### Implementation Details

- Uses `plt.subplots()` to create `fig` and `ax` explicitly
- Bar plot is drawn on `ax` using `ax.bar()`
- X-axis tick positions set with `ax.set_xticks()`
- X-axis labels set with `ax.set_xticklabels()` using the dict keys
- Title and axis labels are derived from `metric_name`

### Design Decisions

- **Receives a dict, not a pd.Series.** This decouples the visualizer
  from pandas. The module depends only on Python standard library and
  matplotlib. Any source that can produce a dict can use this function
  — pandas, a JSON file, a database query, or an API response.

- **Returns a Figure, does not save or display.** The function's
  responsibility is to create the visualization, not to decide where
  it goes. Saving to disk or calling `plt.show()` is the caller's
  decision — following the same single-responsibility pattern used
  across the pipeline.

- **Explicit `fig, ax` over implicit `plt` calls.** Using
  `plt.subplots()` gives explicit control over the figure and axes
  objects. This allows the function to return the figure and avoids
  relying on matplotlib's implicit global state.

- **Generic function instead of metric-specific functions.** The
  function accepts any metric name instead of being hardcoded to a
  specific metric like log level. This avoids duplicating nearly
  identical functions for different metrics (level, service, etc.)
  as the project grows in Month 2. The metric name parameter is
  configuration, not behavior — it changes what text is displayed,
  not what the function does.

---

## Future Improvements (Planned)

- Support additional plot types (histogram, line plot) as the
  analysis layer expands in Month 2
- Color customization per category (e.g. red for ERROR, yellow
  for WARNING)
- Support for saving figures directly if a path is provided
  (optional parameter, not mandatory)
