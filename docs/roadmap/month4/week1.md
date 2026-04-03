# Month 4 — Week 1 (Sprint 7)

## Sprint Goal

Begin building statistical intuition by analyzing the data your
pipeline produces. By the end of this week you should understand
the distributions in your data, verify the correlations you designed
into the generator, and perform your first train/test split.

This sprint is about **analysis, not engineering**. You are not
building new pipeline infrastructure — you are using what you
built in Months 1–3 to understand your data before modeling it.

---

## Context

Month 3 closed with:

- Feature dataset with 5 derived features + 3 context columns
- Generator with CPU+memory→RT correlation and peak/off-peak hours
- Automated pipeline via bash script + cron
- Config-driven thresholds across generator and features

This sprint uses two data sources:

- **Raw DataFrame** (from `run_pipeline`): contains cpu, mem,
  response_time, level, service — used for distribution analysis
  and correlation verification
- **Feature dataset** (`output/datasets/features.csv`): contains
  derived features — used for train/test splitting

---

## New Module This Sprint

```
src/analysis/statistical_analysis.py
```

This module contains functions for statistical analysis: descriptive
statistics, cross-service comparison, and train/test splitting.
During development, functions are tested via a `__main__` block —
same pattern used across the project. Pipeline integration is
deferred until the module is stable and the scope is clear.

---

## Sprint Focus

### Day 1 — Distribution Analysis

**Goal:** Plot and interpret the distributions of the three numeric
metrics in the raw DataFrame.

**Operational improvement:** Add cpu and mem distribution plots to
the existing reporting pipeline. This is a small change — two
additional calls to `_dist_report()` in `run_reporting_pipeline.py`.

**Analysis work:**

1. Run the pipeline and examine the three distribution plots
   (response_time, cpu, mem)
2. For each distribution, identify:
   - Shape: uniform, normal, or skewed?
   - Center: where do most values concentrate?
   - Spread: how wide is the range?
3. Explain **why** each distribution looks the way it does —
   connect back to how the generator produces the data
   - cpu: `random.randint(30, 70)` — what shape does this produce?
   - mem: `random.randint(40, 75)` — same question
   - response_time: depends on cpu AND mem thresholds — how does
     this affect the shape?

**Deliverable:** Three distribution plots saved to `output/plots/`.
Written interpretation of each distribution in
`docs/statistical_analysis.md`.

---

### Day 2 — Descriptive Statistics and Cross-Service Comparison

**Goal:** Compute summary statistics and verify that the generator
produces uniform behavior across services.

**New code in `statistical_analysis.py`:**

1. **Descriptive statistics function** — given a DataFrame, compute
   mean, median, std, min, max, and percentiles (25th, 50th, 75th)
   for numeric columns
2. **Cross-service comparison** — run the pipeline for each service
   individually, compute descriptive statistics for each, and
   compare. Since the generator does not differentiate between
   services, the statistics should be similar across all three.

**Analysis work:**

3. Run descriptive statistics on the raw DataFrame
4. Identify if any values fall outside the generator's configured
   ranges (cpu 30–70, mem 40–75, response_time 200–1200)
5. Compare statistics across services — are they similar?
   Document why or why not

**Deliverable:** Descriptive statistics output. Cross-service
comparison documented in `docs/statistical_analysis.md`.

---

### Day 3 — Correlation Analysis

**Goal:** Verify the correlations designed into the generator and
interpret the feature dataset correlations.

**Using existing tools** (`convert_corr_matrix()` and
`plot_correlation()`):

1. Run the correlation matrix on the **raw DataFrame** — verify:
   - Is cpu correlated with response_time?
   - Is mem correlated with response_time?
   - The generator was designed to produce these — confirm
     they exist
2. Run the correlation matrix on the **feature dataset** —
   interpret:
   - Which derived features are correlated?
   - Do the correlations make sense given how the features
     were constructed?

**Conceptual exercise (no code):**

3. **Correlation vs causation** — document at least one example
   from your data where correlation exists but causation is the
   generator's design, not a real-world relationship

**Deliverable:** Correlation heatmaps for both datasets.
Interpretation and correlation vs causation discussion documented
in `docs/statistical_analysis.md`.

---

### Day 4 — Train / Test Split

**Goal:** Split the feature dataset for future ML consumption.

**New code in `statistical_analysis.py`:**

1. Install scikit-learn in your conda environment
2. Write a function that uses `train_test_split` on the feature
   dataset
3. Choose a split ratio (80/20 is standard)
4. Save train and test sets to `output/datasets/`

**Verification:**

5. Check that class distribution is preserved in both sets —
   the feature dataset does not have a `level` column directly,
   so think about what column can serve as a proxy, or whether
   you need to bring `level` into the feature dataset for
   stratification
6. If the split is not balanced, learn about the `stratify`
   parameter

**Deliverable:** `train.csv` and `test.csv` saved to
`output/datasets/`. Split verification documented.

---

### Day 5–7 (Buffer)

- Complete `docs/statistical_analysis.md` with all findings
- Update `session_context.md`
- Check if any tech debt items emerged during the sprint
- Sprint review and checkpoint

---

## Tech Debt Mapped to This Sprint

| Item | Module | Connection |
|------|--------|------------|
| Expand metric combinations | log_analysis | Resolved by adding cpu/mem dist to reporting |

No major tech debt items are required. The focus is analytical
work using existing tools.

---

## Sprint Deliverables

At the end of Week 1 you must have:

- Distribution plots for response_time, cpu, and mem
- Descriptive statistics for the raw DataFrame
- Cross-service comparison with interpretation
- Correlation matrices for raw DataFrame and feature dataset
- Correlation vs causation documented
- Train/test split saved to output/datasets/
- `docs/statistical_analysis.md` with all findings and
  interpretations
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs
- Analysis includes interpretation, not just plots or numbers
- Findings are documented in `docs/statistical_analysis.md`
- Commit pushed
- Results reproducible
