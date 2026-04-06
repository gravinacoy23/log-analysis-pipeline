# Month 5 — Week 2 (Sprint 10)

## Sprint Goal

Migrate the reader and parser to handle NASA HTTP access logs.
By the end of this week the pipeline should produce a raw
DataFrame from real log data. This is the core engineering
sprint of the migration.

---

## Context

Sprint 9 delivered:

- NASA HTTP dataset (Aug 1995, ~1.57M lines)
- Format analysis with field-by-field documentation
- Data quality findings (10 malformed lines, `-` in response size)
- Regex pattern verified against good and bad lines
- Migration decisions: deprecate synthetic, regex for parsing,
  config updated layer by layer

The regex pattern from the experiment:
```python
r"(\S+) (\S+) (\S+) \[(.+?)\] \"(.+?)\" (\d+) (\S+)"
```

---

## Sprint Focus

### Day 1 — Reader Migration

**Goal:** Adapt `log_reader.py` to load access logs from the new
directory structure.

1. The current reader assumes per-service directories
   (`data/raw/booking/`, `data/raw/shopping/`, etc.). The NASA
   dataset is a single file (or files) in one directory.

2. Decide the new directory structure. Options:
   - `data/raw/access/` — single directory with log files
   - `data/raw/` — files directly in raw

3. Simplify the reader — the concepts of "service" directories
   and `load_service_logs(service)` no longer apply. You need
   a function that reads all log files from a single directory.

4. Keep the generator pattern (`yield` per line) — that
   principle is correct regardless of format.

5. Update error handling for the new structure.

**Deliverable:** Reader loads real log files and yields lines.
Test with `__main__` block or by printing first 10 lines.

---

### Day 2 — Parser Migration (regex + field extraction)

**Goal:** Rewrite `parse_logs()` and `_parse_fields()` to use
regex for Common Log Format.

1. Replace the `key=value` logic with the regex pattern from
   the experiment.

2. Handle the guard clause: if `re.match` returns `None`, the
   line is malformed — skip it and increment the counter. This
   replaces the current guards for missing `msg=` and empty
   fields.

3. Extract the request line (group 5) into sub-fields: HTTP
   method, endpoint, and HTTP version. This can be a simple
   `str.split(" ", 2)` since the request is already captured
   cleanly by the regex.

4. Handle the `-` in response size — decide: convert to `0`,
   convert to `None`, or skip the line.

5. `_verify_columns()` and `_skip_report()` should not need
   changes — they are generic. Verify this.

**Deliverable:** Parser produces a list of dicts from real log
lines. Test with `__main__` block.

---

### Day 3 — Config and Analysis Layer

**Goal:** Update config.yaml and verify the analysis layer works
with the new columns.

1. Update `config.yaml`:
   - New `columns` dict with the fields from the access log
     and their data types
   - New `expected_values` — HTTP methods (GET, POST, HEAD),
     status code ranges or categories
   - Remove synthetic-specific keys (`messages`,
     `hour_of_day_weights`) or mark them as deprecated
   - Keep `metric_thresholds` structure but adapt for new
     metrics if needed

2. Update `config_loader.py` — adjust `required_keys` list
   if keys changed.

3. Update `run_pipeline.py`:
   - Use the new reader function
   - Build `expected_values` from new config keys
   - Remove or update `get_metric_thresholds` calls for new
     metrics

4. Run the pipeline end-to-end for the first time with real
   data. Fix whatever breaks.

**Deliverable:** `run_pipeline` produces a valid DataFrame from
real NASA logs.

---

### Day 4 — End-to-End Verification and Cleanup

**Goal:** Verify the full pipeline works and clean up deprecated
code.

1. Run `main.py` and verify:
   - Reader loads the file
   - Parser produces correct dicts
   - Analysis layer validates and creates DataFrame
   - No crashes on the 10 malformed lines

2. Remove or update `main.py` argparse — the `--service`
   argument no longer applies.

3. Deprecate synthetic-specific code:
   - Remove `log_generator.py` from active use (keep in git)
   - Remove `load_service_logs()` and `load_all_logs()` from
     the reader
   - Remove synthetic-specific analysis functions from
     `log_analysis.py` (or leave for Month 6 cleanup)

4. Run `_skip_report()` and verify it correctly reports the
   10 malformed lines.

5. Print `df.describe()` on the resulting DataFrame — verify
   the numbers make sense (status codes, response sizes).

**Deliverable:** Pipeline runs end-to-end on real data.
`describe()` output documented.

---

### Day 5–7 (Buffer)

- Handle edge cases that surfaced during testing
- Update design documents for reader and parser
- Update `__main__` blocks with real data examples
- Commit with clear messages
- Sprint review

---

## Deprecated Code This Sprint

| Module | What | Action |
|--------|------|--------|
| `log_generator.py` | Entire module | Remove from active pipeline |
| `log_reader.py` | `load_service_logs()`, `load_all_logs()`, helpers | Replace with new reader function |
| `log_parser.py` | `parse_logs()` inner logic, `_parse_fields()` | Rewrite with regex |
| `main.py` | `--service` argument | Remove |
| `run_pipeline.py` | Service parameter, synthetic expected_values | Update |
| `config.yaml` | `messages`, `hour_of_day_weights` | Remove |

---

## Sprint Deliverables

At the end of Week 2 you must have:

- Reader loading real NASA access log files
- Parser extracting all fields with regex
- Config updated for new column definitions
- Pipeline producing a valid DataFrame from real logs
- Malformed lines skipped and reported correctly
- `describe()` output verifying data makes sense
- Deprecated synthetic code removed
- Commits with clear messages pushed to GitHub

---

## Definition of Done

A task is complete when:

- Code runs on real log data
- Parser handles all 10 malformed lines gracefully
- Pipeline produces a valid DataFrame
- Changes are documented
- Commit pushed
