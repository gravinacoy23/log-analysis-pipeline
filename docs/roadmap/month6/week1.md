# Month 6 — Week 1 (Sprint 11)

## Sprint Goal

Adapt the reporting and visualization layers to CLF columns,
clean up deprecated config, re-enable pipelines in main.py,
define metric thresholds for new data, and merge the migration
branch to main. By the end of this sprint the pipeline should
run end-to-end producing a DataFrame and visualization reports
from real NASA log data.

---

## Context

Sprint 10 delivered the core migration: reader, parser, config,
and analysis layer all running on real data. The analysis layer
validation was already updated (range validation for status code,
protocol None handling, dtype checks). What remains for the
analysis and visualization layer is adapting the reporting
pipeline's column arguments, defining metric thresholds for new
numeric columns, and running correlation/distribution analysis
on the new data.

The reporting pipeline requires only column name changes — the
functions are generic. `get_metric_thresholds()` is generic and
already in the codebase — it needs new threshold definitions in
config for CLF-relevant metrics. Features and statistical
pipelines are deferred to Weeks 2–3.

---

## Sprint Focus

### Day 1 — Reporting Pipeline Adaptation

**Goal:** Update `run_reporting_pipeline.py` to use CLF columns.

1. Replace old column arguments with new ones:
   - `_count_report(df, "level")` → what categorical column
     is worth counting? Candidates: `method`, `http_response`,
     `protocol_version`
   - `_count_report(df, "service")` → no direct replacement,
     remove or replace with a relevant categorical column
   - `_dist_report(df, "response_time")` → `_dist_report(df, "response_size")`
   - `_dist_report(df, "cpu")` → remove (column doesn't exist)
   - `_dist_report(df, "mem")` → remove (column doesn't exist)

2. Decide which reports are meaningful for CLF data:
   - Count by HTTP method (GET/POST/HEAD distribution)
   - Count by status code (200/304/302/404 distribution)
   - Distribution of response size
   - Correlation heatmap (http_response vs response_size)

3. The visualizer functions (`plot_count_metric`,
   `plot_distribution`, `plot_correlation`) are generic — no
   code changes needed in `log_visualizer.py`.

4. Run the reporting pipeline and verify plots are generated
   in `output/plots/`.

**Deliverable:** Reporting pipeline producing plots from real data.

---

### Day 2 — Config Cleanup and Main Re-enable

**Goal:** Clean deprecated config keys, re-enable reporting
pipeline in main.py, and run end-to-end.

1. Remove deprecated keys from `config.yaml`:
   - `metric_thresholds` (cpu/mem — will be replaced with
     new thresholds on Day 3)
   - `feature_thresholds` (features being redesigned in Week 2)
   - `hour_of_day_weights` (generator deprecated)

2. Update `main.py`:
   - Uncomment `run_report_pipeline(logs_dataframe)`
   - Keep features and statistical pipelines commented
     (deferred to Weeks 2–3)
   - Remove unused imports if any

3. Run `main.py` end-to-end and verify:
   - DataFrame created with correct row count
   - Plots generated in `output/plots/`
   - No crashes or unexpected warnings

**Deliverable:** `main.py` runs with data pipeline + reporting
pipeline active.

---

### Day 3 — Analysis, Thresholds, and Distribution Exploration

**Goal:** Run analytical exploration on real data, define metric
thresholds for new columns, and document findings.

1. Run `convert_corr_matrix()` on the new DataFrame — what
   correlates in real data? Compare with the designed
   correlations in synthetic data (CPU→RT, MEM→RT).

2. Run `general_statistics()` — examine describe() output for
   response_size and http_response. What do the distributions
   look like?

3. Define metric thresholds for `response_size` using
   `get_metric_thresholds()`:
   - Examine the distribution of response_size from describe()
     output (min, 25th, 50th, 75th, max)
   - Define meaningful buckets in config (e.g. small, medium,
     large based on percentile boundaries)
   - Add new `metric_thresholds` to config with response_size
     boundaries
   - Call `get_metric_thresholds()` from `run_pipeline` and
     verify the `response_size_bucket` column is added

4. Document findings:
   - What patterns exist in real data?
   - What surprised you vs synthetic data?
   - What columns have enough variance to be useful for ML?
   - What columns have almost no variance (e.g. method is
     99.7% GET)?
   - What threshold boundaries did you choose and why?

**Deliverable:** Analysis findings documented. Metric thresholds
defined and working for response_size.

---

### Day 4–5 — Documentation, Cleanup, and Merge

**Goal:** Close documentation, update __main__ blocks, and
merge to main.

1. Update `__main__` blocks in modified modules with real
   data examples (CLF format).

2. Update design documents:
   - `main_design.md` — v7
   - `run_reporting_pipeline_design.md` — v4
   - `run_pipeline_design.md` — v9 (if get_metric_thresholds
     call added back)

3. Update `README.md`:
   - New log format description
   - Updated setup instructions (NASA dataset)
   - Remove references to synthetic logs and service names

4. Final verification on complete dataset (~1.57M lines).

5. Create Pull Request on GitHub from `migration/real-logs`
   to `main`:
   - Review the diff
   - Merge
   - `git checkout main`, `git pull`, verify clean

**Deliverable:** Migration complete. Branch merged. Main branch
running on real data with metric thresholds.

---

## Sprint Deliverables

At the end of Week 1 you must have:

- Reporting pipeline producing plots from real CLF data
- Deprecated config keys removed
- `get_metric_thresholds()` working with response_size buckets
- New metric thresholds defined in config
- `main.py` running end-to-end (data + reporting pipelines)
- Correlation and distribution analysis documented
- `__main__` blocks updated with real data examples
- All design documents current
- README updated
- Branch merged to main
- Clean git history

---

## Definition of Done

A task is complete when:

- Code runs on real log data
- Plots are generated correctly
- Metric thresholds produce correct bucket column
- Pipeline runs end-to-end without errors
- Documentation updated
- Commit pushed
- Branch merged to main (end of sprint)
