# Month 6 — Week 2 (Sprint 12)

## Sprint Goal

Redesign and implement the feature engineering module for CLF
log data. By the end of this sprint, the pipeline should produce
a new feature dataset with domain-relevant features derived from
real web server access logs, persisted to CSV.

---

## Context

Sprint 11 delivered the reporting pipeline, metric thresholds,
and analysis findings on real data. The data pipeline and
reporting pipeline are fully functional on main branch.

The current `feature_engineering.py` references synthetic columns
that no longer exist (level, service, cpu, mem, response_time).
The module needs a complete redesign, but the orchestration
pattern survives: each function returns a Series, the orchestrator
assembles with `pd.concat()`.

Key findings from Sprint 11 that inform feature design:
- response_size is heavily right-skewed (median 3.1K, max 3.4M)
- http_response has almost no variance (89% are 200)
- HTTP method has almost no variance (99.7% GET)
- Pearson correlation between status and size is ~0 due to
  class imbalance and categorical nature of status codes
- Features need to surface relationships that raw columns hide

---

## Sprint Focus

### Day 1 — Feature Design

**Goal:** Define which features to build and why each is
relevant for future ML.

1. Review the CLF columns available in the DataFrame:
   host, identity, user, timestamp, method, endpoint,
   protocol_version, http_response, response_size,
   response_size_bucket

2. For each candidate feature, answer:
   - What does it measure?
   - What pattern does it surface that raw columns hide?
   - Is there enough variance to be useful for ML?

3. Candidate features to evaluate:
   - **status_category:** Map status codes to categories
     (2xx, 3xx, 4xx, 5xx) — surfaces error patterns hidden
     by the dominance of 200
   - **is_error:** Boolean flag for status >= 400 (or >= 500)
     — the target variable for ML
   - **hour_of_day:** Extract hour from timestamp — surfaces
     temporal traffic patterns
   - **response_size_bucket:** Already exists from
     get_metric_thresholds() — evaluate if it should also
     live in features
   - **endpoint_frequency:** How often each endpoint is
     requested — surfaces popular vs rare endpoints
   - **is_large_response:** Boolean flag for response_size
     above a threshold — simpler binary signal than buckets

4. Decide which features to implement. Not all candidates
   may be worth building — justify each decision.

**Deliverable:** Feature list with rationale documented.

---

### Day 2 — Core Feature Implementation

**Goal:** Implement the straightforward features that derive
directly from existing columns.

1. Update `orchestrate_features()`:
   - New context columns (host, timestamp, endpoint)
   - Remove synthetic references (service, level, cpu, mem)

2. Implement features that transform single columns:
   - `_status_category()` — map http_response to 2xx/3xx/4xx/5xx
   - `_is_error()` — boolean from http_response >= threshold
   - `_hour_of_day()` — extract hour from timestamp

3. Each function follows the established pattern:
   - Receives the DataFrame
   - Returns a named Series
   - No side effects

4. Update config with any new thresholds needed (e.g. error
   threshold: 400 vs 500).

**Deliverable:** Core features implemented and verified.

---

### Day 3 — Advanced Features

**Goal:** Implement features that require aggregation or
cross-row logic.

1. Evaluate and implement:
   - `_endpoint_frequency()` — count of requests per endpoint,
     mapped back to each row. This requires a groupby +
     transform or a value_counts + map pattern.
   - `_is_large_response()` — boolean from response_size
     above a config-driven threshold

2. Think about: does `response_size_bucket` from
   get_metric_thresholds() belong in the feature dataset?
   If yes, how do you include it without duplicating the
   bucketing logic?

3. Verify all features produce correct output on a small
   sample before running on the full dataset.

**Deliverable:** All features implemented and verified.

---

### Day 4 — Pipeline Integration and Persistence

**Goal:** Re-enable the features pipeline in main.py and
persist the feature dataset.

1. Update `run_features_pipeline.py`:
   - Update the call to `orchestrate_features()` with new
     parameters
   - Verify config keys match what the pipeline extracts

2. Update `main.py`:
   - Uncomment `run_features_pipeline()` call
   - Verify import is still correct

3. Run end-to-end and verify:
   - Feature dataset saved to `output/datasets/features.csv`
   - Correct number of rows (should match DataFrame row count)
   - All feature columns present
   - No NaN values in unexpected places

**Deliverable:** Features pipeline producing CSV from real data.

---

### Day 5 — Documentation and Cleanup

**Goal:** Update all documentation for the new feature
engineering module.

1. Update design documents:
   - `feature_engineering_design.md` — v3
   - `run_features_pipeline_design.md` — v2
   - `main_design.md` — v8 (features re-enabled)

2. Document feature rationale:
   - Why each feature was chosen
   - What ML relevance each feature has
   - What features were considered but rejected (and why)

3. Update `tech_debt.md` if new items arise.

4. Commit and push.

**Deliverable:** Documentation current. Feature module complete.

---

## Sprint Deliverables

At the end of Week 2 you must have:

- New `feature_engineering.py` with CLF-relevant features
- Feature design rationale documented
- `orchestrate_features()` updated with new feature list
- Features pipeline re-enabled in main.py
- Feature dataset persisted to `output/datasets/features.csv`
- Config updated with feature-related thresholds
- All design documents current
- Clean git history with atomic commits

---

## Key Concepts to Learn

- **Feature engineering for categorical data:** Transforming
  status codes into categories and binary flags
- **Aggregation-based features:** Using groupby/transform to
  create per-group statistics mapped back to individual rows
- **Feature relevance assessment:** Not every column or
  transformation produces a useful feature — variance, signal,
  and ML utility matter
- **Class imbalance awareness:** With ~0.65% error rate, feature
  design must consider how to surface the minority class signal

---

## Definition of Done

A task is complete when:

- Feature functions follow the established pattern (Series return)
- Features are verified on real data
- Pipeline runs end-to-end without errors
- Feature dataset persisted correctly
- Documentation updated
- Commit pushed
