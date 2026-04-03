# Month 4 — Week 1 (Sprint 7)

## Sprint Goal

Begin building statistical intuition using the feature dataset
produced in Month 3. By the end of this week you should understand
the distributions in your data, verify the correlations you designed
into the generator, and perform your first train/test split.

---

## Context

Month 3 closed with:

- Feature dataset with 5 derived features + 3 context columns
- Generator with CPU+memory→RT correlation and peak/off-peak hours
- Automated pipeline via bash script + cron
- Config-driven thresholds across generator and features

The feature dataset at `output/datasets/features.csv` is the
starting point for all Month 4 work. This month is about
understanding the data before modeling it in Phase 3.

---

## Sprint Focus

### Probability and Distributions

Using the feature dataset and the raw DataFrame:

1. **Plot distributions** of response_time, cpu, and mem
   - Use histplot from seaborn (already in the project)
   - Identify whether each is uniform, normal, or skewed
   - Explain *why* each distribution looks the way it does —
     connect back to how the generator produces the data

2. **Compare distributions across services**
   - Does shopping have different CPU patterns than booking?
   - This verifies whether the generator produces uniform
     behavior across services (it should, since service-specific
     instability is not yet implemented)

3. **Outlier detection**
   - Use descriptive statistics: mean, median, std, percentiles
   - Identify if any values fall outside expected ranges
   - Connect findings to the generator's configured ranges

### Correlation Analysis

4. **Correlation matrix of the feature dataset**
   - You already have `convert_corr_matrix()` and the heatmap
   - Run it on the feature dataset and interpret results
   - Verify: is CPU correlated with response_time? Is memory?
   - The generator was designed to produce these correlations —
     confirm they exist in the data

5. **Correlation vs causation**
   - Document at least one example from your data where
     correlation exists but causation is the generator's design,
     not a real-world relationship
   - This is a conceptual exercise, not a coding task

### Train / Test Split

6. **First split with sklearn**
   - Install scikit-learn if not already in your environment
   - Use `train_test_split` on the feature dataset
   - Choose an appropriate split ratio (80/20 or 70/30)
   - Save train and test sets to `output/datasets/`

7. **Verify the split**
   - Check that class balance (INFO/WARNING/ERROR distribution)
     is preserved in both sets
   - If not balanced, learn about `stratify` parameter
   - Document the split ratio and verification

---

## Tech Debt Mapped to This Sprint

| Item | Module | Connection |
|------|--------|------------|
| Expand metric combinations | log_analysis | Distribution analysis needs more metric views |

No major tech debt items are required for this sprint. The focus
is analytical work using existing tools.

---

## Day-by-Day Suggestion

### Day 1
- Load the feature dataset from CSV
- Plot distributions of response_time, cpu, mem
- Describe each distribution (shape, center, spread)

### Day 2
- Compare distributions across services
- Descriptive statistics: mean, median, std, percentiles
- Outlier identification

### Day 3
- Correlation matrix on feature dataset
- Interpret: which features are correlated and why
- Document correlation vs causation distinction

### Day 4
- Install scikit-learn
- First train/test split
- Verify class balance in both sets
- Save splits to output/datasets/

### Day 5–7 (Buffer)
- Begin statistical analysis report in docs/
- Documentation updated
- Sprint review and checkpoint

---

## Sprint Deliverable

At the end of Week 1 you must have:

- Distribution plots for numeric features
- Cross-service distribution comparison
- Correlation matrix with interpretation
- Train/test split saved to output/datasets/
- Split verification documented
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs
- Analysis includes interpretation, not just plots
- Findings are documented
- Commit pushed
- Results reproducible
