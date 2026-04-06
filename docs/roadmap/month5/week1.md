# Month 5 — Week 1 (Sprint 9)

## Sprint Goal

Research and select a real log source, understand its format in
depth, and plan the migration strategy. By the end of this week
you should have a real log dataset on disk, a clear understanding
of every field in the format, and a documented plan for how the
parser needs to change.

No code changes to the pipeline this week — this is research and
planning. The migration starts in Week 2.

---

## Context

The pipeline currently processes synthetic logs in `key=value`
format designed for the airline booking simulation. The goal of
Month 5 is to transition to real web server access logs in
Common/Combined Log Format.

The recommended source is Nginx/Apache access logs. These are
the standard format for web server traffic logging and are
directly relevant to infrastructure and data engineering roles.

---

## Sprint Focus

### Day 1 — Obtain a Real Log Dataset

1. **Search for a public dataset.** Look for:
   - "NASA HTTP access logs dataset" — a classic dataset used
     in research, freely available
   - "web server access logs dataset" on Kaggle
   - Any publicly available Apache/Nginx access log dataset

2. **Alternatively, generate your own.** If you prefer:
   - Install Nginx on WSL (`sudo apt install nginx`)
   - Start the server and generate traffic manually or with
     a tool like `curl` or `ab` (Apache Bench)
   - Collect the access logs from `/var/log/nginx/access.log`

3. **Download or collect the dataset** and place it in
   `data/raw/` in your project. Examine the first 20-30 lines
   manually.

**Deliverable:** A real log file in your project directory.

---

### Day 2 — Understand the Log Format

1. **Identify the format.** Is it Common Log Format (CLF) or
   Combined Log Format? The difference:

   **CLF:**
   ```
   127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
   ```

   **Combined:**
   ```
   127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08"
   ```

2. **Map every field.** For each field, document:
   - What it represents
   - Its data type (string, int, datetime)
   - Whether it is always present or can be missing
   - The delimiter that separates it from adjacent fields

3. **Compare with your current format.** Create a table:

   | Current (synthetic) | New (access log) | Notes |
   |---------------------|------------------|-------|
   | timestamp | timestamp | Different format |
   | service | — | Does not exist |
   | user | remote user | May be empty (`-`) |
   | cpu | — | Does not exist |
   | mem | — | Does not exist |
   | response_time | — | Not in standard CLF |
   | level | — | Does not exist |
   | msg | — | Does not exist |
   | — | IP address | New |
   | — | HTTP method | New |
   | — | endpoint | New |
   | — | HTTP version | New |
   | — | status code | New |
   | — | response size | New |
   | — | referer | New (Combined only) |
   | — | user agent | New (Combined only) |

4. **Identify the parsing challenge.** Your current parser uses
   `str.split(" ")` and `str.partition()`. Look at the new
   format — which fields are space-separated? Which are inside
   brackets or quotes? What makes this harder than `key=value`?

**Deliverable:** Format documentation with field mapping and
comparison table.

---

### Day 3 — Data Quality Exploration

1. **Look for messy data.** In your real log file, find:
   - Lines with missing fields (e.g. `-` for user or referer)
   - Unusual status codes
   - Malformed lines (if any)
   - Different request methods (GET, POST, HEAD, etc.)
   - Unusual endpoints or query strings

2. **Count the lines.** How many log entries does your dataset
   have? Is it enough for meaningful analysis and ML?

3. **Identify edge cases** your parser will need to handle:
   - What does `-` mean in the user field?
   - What happens if the request line is malformed?
   - Are there lines that do not match the expected format?
   - Are there any encoding issues?

**Deliverable:** List of edge cases and data quality observations
documented.

---

### Day 4 — Migration Strategy

1. **Decide on the parsing approach.** Research two options:
   - **String splitting:** use delimiters like `[`, `]`, `"` to
     extract fields positionally
   - **Regular expressions:** write a regex pattern that captures
     all fields in one match

   For each, consider: readability, maintainability, error
   handling. Which aligns better with the project's philosophy
   of readable, understandable code?

2. **Decide on synthetic log support.** Options:
   - Keep both parsers (synthetic and real) selectable via config
   - Deprecate synthetic — the old code lives in git history
   - Document your decision and reasoning

3. **Plan the config changes.** What needs to change in
   `config.yaml`? New columns, new expected values, new
   thresholds? Draft the new config structure.

4. **List all modules that need changes.** For each module,
   note what specifically changes:
   - `log_reader.py` — file structure (single file vs dirs?)
   - `log_parser.py` — complete rewrite of parsing logic
   - `log_analysis.py` — new columns, new validation
   - `config.yaml` — new fields, new values
   - Others?

**Deliverable:** Migration plan documented with decisions and
module impact list.

---

### Day 5–7 (Buffer)

- Document all findings in `docs/migration_plan.md`
- If time allows, start experimenting with parsing approaches
  in a scratch file (not in the pipeline yet)
- Commit research and documentation
- Sprint review

---

## Sprint Deliverables

At the end of Week 1 you must have:

- A real log dataset in `data/raw/`
- Format documentation with field-by-field analysis
- Comparison table: synthetic vs real format
- Data quality observations and edge cases listed
- Parsing approach decision documented
- Synthetic log support decision documented
- Config change plan drafted
- Module impact list
- All findings in `docs/migration_plan.md`
- Commits pushed

---

## Definition of Done

A task is complete when:

- Research is documented, not just read
- Decisions include reasoning, not just choices
- Findings are in `docs/migration_plan.md`
- Commit pushed
