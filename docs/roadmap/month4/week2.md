# Month 4 — Week 2 (Sprint 8)

## Sprint Goal

Understand the conceptual foundations that determine whether an ML
model is working well or poorly. By the end of this week you should
be able to explain bias vs variance, know when accuracy is
misleading, and compute precision, recall, and F1 score from a
confusion matrix.

This sprint is primarily **conceptual**. The code is minimal —
the goal is to build intuition for evaluating ML models before
you train one in Phase 3.

---

## Context

Week 1 closed with:

- Distribution analysis of cpu, mem, response_time
- Cross-service comparison confirming uniform generator behavior
- Correlation verification (CPU→RT, MEM→RT)
- Train/test split with stratification on `is_error`
- `statistical_analysis.py` and `run_statistical_pipeline.py` in place

The train/test split exists but there is no model yet. This week
focuses on understanding **how** you will evaluate a model once
you have one.

---

## Sprint Focus

### Day 1 — Bias vs Variance

**Goal:** Understand underfitting and overfitting conceptually,
and connect them to your dataset.

**Concepts:**

1. **Underfitting (high bias)** — the model is too simple to
   capture patterns in the data. It performs poorly on both
   training and test data.

2. **Overfitting (high variance)** — the model memorizes the
   training data including noise. It performs well on training
   data but poorly on test data.

3. **The tradeoff** — increasing model complexity reduces bias
   but increases variance. The goal is to find the balance
   where the model generalizes well to unseen data.

**Analysis work (no code):**

4. Think about your `is_error` feature. If a model simply
   predicted `is_error = False` for every row, would it
   underfit or overfit? What would its accuracy be given
   your class distribution?

5. Document your understanding of bias vs variance in
   `docs/statistical_analysis.md`

---

### Day 2 — Accuracy and Why It Can Be Misleading

**Goal:** Understand why accuracy alone is not enough to evaluate
a classifier.

**Concepts:**

1. **Accuracy** = correct predictions / total predictions.
   Simple, intuitive, but dangerous with imbalanced data.

2. **The accuracy trap** — if your dataset has 85% `is_error =
   False` and 15% `is_error = True`, a model that always
   predicts `False` gets 85% accuracy without learning anything.

**Analysis work:**

3. Using your training dataset, calculate what percentage of
   rows have `is_error = True` vs `False`. This is your class
   distribution.

4. Calculate what accuracy a "dumb model" (always predicts
   `False`) would achieve. Write this in your report — it
   becomes the **baseline** that any real model must beat.

5. If a model is supposed to detect errors in your airline
   backend, what matters more — catching all real errors
   (even if some false alarms), or only flagging rows you
   are sure are errors (even if you miss some)?

**Deliverable:** Class distribution calculated. Baseline accuracy
documented. Question 5 answered in your report — this sets up
precision vs recall.

---

### Day 3 — Precision, Recall, and F1 Score

**Goal:** Understand the metrics that handle imbalanced
classification.

**Concepts:**

1. **Confusion matrix** — a 2x2 table for binary classification:
   - True Positive (TP): predicted error, was error
   - True Negative (TN): predicted not error, was not error
   - False Positive (FP): predicted error, was not error
   - False Negative (FN): predicted not error, was error

2. **Precision** = TP / (TP + FP) — "of all the rows I flagged
   as errors, how many were actually errors?"

3. **Recall** = TP / (TP + FN) — "of all the real errors, how
   many did I catch?"

4. **F1 score** = harmonic mean of precision and recall — balances
   both when you cannot afford to sacrifice either

**Analysis work:**

5. Create a function in `statistical_analysis.py` that receives
   a list of actual values and predicted values, and computes
   TP, TN, FP, FN. Do this manually — do not use sklearn yet.
   This is about understanding the math, not calling a library.

6. Using synthetic predictions (hardcode a small example), verify
   your function produces correct counts. Then compute precision,
   recall, and F1 manually from those counts.

7. Answer: for your airline backend error detection system, would
   you prioritize precision or recall? Why?

**Deliverable:** Confusion matrix function in
`statistical_analysis.py`. Manual computation of precision, recall,
F1 documented in report.

---

### Day 4 — Connecting Everything

**Goal:** Tie all concepts together using your dataset.

**Analysis work:**

1. Using your training set, simulate a "dumb model" that predicts
   `is_error = False` for every row. Compute its confusion matrix,
   precision, recall, and F1 using your function.

2. Simulate a slightly smarter model: predict `is_error = True`
   whenever `is_slow = True`. Compute the same metrics.

3. Compare the two. Which one has better accuracy? Which one has
   better recall? Which one would you deploy in a real system
   and why?

4. Document findings in `docs/statistical_analysis.md`

**Deliverable:** Two simulated models compared with metrics.
Interpretation documented.

---

### Day 5–7 (Buffer)

- Complete `docs/statistical_analysis.md` with all Month 4 findings
- Update `session_context.md`
- Review: does `statistical_analysis.py` need any cleanup?
- Check for tech debt items
- Sprint review and checkpoint

---

## Sprint Deliverables

At the end of Week 2 you must have:

- Bias vs variance explanation documented
- Class distribution and baseline accuracy calculated
- Confusion matrix function in `statistical_analysis.py`
- Precision, recall, F1 computed for two simulated models
- Comparison of dumb model vs is_slow-based model
- `docs/statistical_analysis.md` complete with all Month 4 findings
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs
- Concepts are explained in your own words, not just definitions
- Analysis includes interpretation connected to your project
- Findings are documented in `docs/statistical_analysis.md`
- Commit pushed
- Results reproducible
