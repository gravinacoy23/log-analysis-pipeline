# Log Parser — Implementation (v4)

## Objective

Implement a log parser module for the airline booking backend pipeline.

The goal of this phase is to:

- Transform raw log strings into structured Python dictionaries
- Extract all fields from each log line
- Apply correct data types to numeric fields
- Validate that all expected fields are present per line
- Reject lines with empty values
- Handle malformed lines gracefully without crashing the pipeline
- Track and report parsing statistics (lines processed, skipped, skip rate)
- Prepare structured data for the pandas layer

---

# System Context

The log parser is the first stage of the processing layer.

It sits between the reader and the analysis layer. Its only responsibility
is to transform raw strings into structured data. It does not know where
the logs came from or what will be done with the data — that is the
responsibility of the layers above and below.

```
log_reader.py → log_parser.py → pandas DataFrame
```

---

# Module Location

```
src/processing/log_parser.py
```

---

# Interface

## `parse_logs(logs, expected_cols)`

Parses a list of raw log strings into a list of dictionaries and
returns parsing statistics alongside the result.

**Parameters:**
- `logs` (Iterator[str]) — iterator of raw log lines as returned by `log_reader.py`
- `expected_cols` (list[str]) — list of required column names loaded from config

**Returns:**
- `tuple[list[dict[str, Any]], dict[str, int | float] | dict[str, int]]`
  — a tuple containing:
  - List of dicts — one dictionary per valid log line
  - Dict of parsing statistics — lines_processed, skipped_lines,
    and skip_rate (skip_rate omitted when input is empty)

**Behavior:**
- Malformed lines are skipped and logged as warnings
- Lines with empty field values are skipped and logged as warnings
- Lines with empty messages are skipped and logged as warnings
- Lines missing expected columns are skipped and logged as warnings
- Valid lines with all expected fields are always included
- Parsing statistics are logged at INFO level at the end of parsing
- Empty input (0 lines processed, 0 skipped) is logged as a WARNING

---

# Log Format

Each log line follows this structure:

```
timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time=561 level=INFO msg="Seat booked"
```

All fields follow the `key=value` pattern. The `msg` field is the only
field that may contain spaces inside quoted values.

---

# Implementation Details

## Four-Function Design

The parser is split into four functions with distinct responsibilities:

- `parse_logs(logs, expected_cols)` — orchestrates iteration over all
  lines, validates messages, validates column completeness, tracks
  skipped lines, and delegates statistics reporting
- `_parse_fields(fields, line_number)` — parses a single line's
  key=value fields, rejects malformed or empty values (private)
- `_verify_columns(logs_dict, expected_cols, line_number)` — validates
  that all expected columns are present in a parsed dict (private)
- `_skip_report(skipped_lines, lines_processed)` — builds and logs
  parsing statistics (private)

This separation keeps each function focused on one concern: parsing,
field validation, column completeness, and statistics reporting.

## Skipped Line Tracking

A `skipped_lines` counter is incremented at each point where a line
is rejected in `parse_logs`:

- Missing or empty message → `skipped_lines += 1`
- `_parse_fields` returns `None` → `skipped_lines += 1`
- `_verify_columns` returns `False` → `skipped_lines += 1`

All three rejection points live in `parse_logs`, so the counter is
maintained in a single function without needing auxiliary functions
to modify an external variable.

The number of successfully processed lines is derived from
`len(log_dict_list)` after the loop — O(1) operation on a Python
list, no counter needed.

## Message Field Isolation

The `msg` field is handled separately because it can contain spaces,
which would break a naive `.split()` approach.

`str.partition(" msg=")` splits the line into three parts:
- Everything before `msg`
- The separator itself (discarded with `_`)
- The message value

```python
before_message, _, message = log.partition(" msg=")
```

The message is stripped of quotes and newlines immediately after
partition. If the result is empty, the line is skipped with a warning
before any further processing occurs.

## Field Parsing

After isolating the message, the remaining fields are split by space.
Each `key=value` pair is then split by `=` to extract the key and value.

## Type Detection and Conversion

Type detection uses guard clauses followed by explicit checks instead
of relying on exceptions for control flow.

For each field, the logic follows this order:

1. **Malformation guard** — if `split_log` has fewer than 2 elements,
   the line is malformed. Log a warning and return `None` immediately.
2. **Empty value guard** — if `split_log[1]` is an empty string
   (e.g. `cpu=`), the field has no value. Log a warning identifying
   the field name and return `None` immediately.
3. **Numeric check** — if the value is numeric (`str.isdigit()`),
   convert to `int`.
4. **Timestamp check** — if the key is `"timestamp"`, parse with
   `datetime.fromisoformat()`.
5. **Default** — store as string.

```python
if len(split_log) < 2:
    logger.warning(f"Malformed line skipped at line {line_number}")
    return None
elif not split_log[1]:
    logger.warning(
        f"Missing {split_log[0]} at line {line_number}, line skipped"
    )
    return None

if split_log[1].isdigit():
    log_dict[split_log[0]] = int(split_log[1])
elif split_log[0] == "timestamp":
    log_dict[split_log[0]] = datetime.fromisoformat(split_log[1])
else:
    log_dict[split_log[0]] = split_log[1]
```

The guard clauses are separate from the type detection chain because
they represent different concerns — validation vs assignment.

## Column Completeness Validation

After a line is successfully parsed by `_parse_fields` and the message
is attached, `_verify_columns` checks that every expected column from
the config is present in the resulting dictionary.

```python
if not _verify_columns(log_dict, expected_cols, line_number):
    skipped_lines += 1
    continue
```

This catches lines where the `key=value` syntax is valid but a field
is entirely missing — for example a line without `mem=` at all. The
empty value guard in `_parse_fields` catches `mem=` with no value;
`_verify_columns` catches the absence of `mem` entirely.

## Message Cleanup

The `msg` value is stripped of surrounding quotes and trailing newline
characters using `.strip('"\n')`.

```python
parsed_message = message.strip('"\n')
```

Both characters are stripped together because log lines read from disk
include a trailing `\n`. A naive `.strip('"')` would leave the newline
after the closing quote.

## Line Numbering

`enumerate(logs, start=1)` is used to track the human-readable line
number. This is passed to `_parse_fields` and `_verify_columns` so
that warning messages reference the correct line.

---

# Validation Flow

Each line goes through three levels of validation before being accepted:

```
1. Message present?          → No  → skip, log warning, increment counter
2. Fields parseable?         → No  → skip, log warning, increment counter
3. All expected cols present? → No  → skip, log warning, increment counter
4. All passed               → append to result list
```

After the loop completes:

```
5. _skip_report(skipped_lines, len(log_dict_list)) → log stats, return stats dict
```

Each level catches a different class of problem:
- Level 1: missing or malformed `msg` field
- Level 2: fields that cannot be split (`key=value`) or have empty values (`key=`)
- Level 3: syntactically valid lines with missing fields

---

# Function: _skip_report()

## Parameters

- `skipped_lines` — integer count of lines rejected during parsing
- `lines_processed` — integer count of lines successfully parsed

## Returns

- `dict[str, int | float] | dict[str, int]` — dict containing
  `lines_processed`, `skipped_lines`, and `skip_rate` (percentage).
  When both values are 0 (empty input), `skip_rate` is omitted to
  avoid division by zero.

## Implementation Details

- Builds the stats dict with lines_processed and skipped_lines
- If both are 0, logs a WARNING about empty input and returns
  the dict without skip_rate
- Otherwise calculates skip_rate as a percentage:
  `(skipped / (skipped + processed)) * 100`
- Iterates over the stats dict and logs each metric at INFO level

## Design Decisions

- **Separate function for statistics.** The main parsing loop tracks
  the raw counter. Building the report, calculating the rate, and
  logging are a distinct responsibility — delegated to `_skip_report`.

- **Logs at INFO level, not WARNING.** Parsing statistics are
  informational — they report what happened, not what went wrong.
  Individual skipped lines are already logged as warnings. The
  empty input case is logged as WARNING because it signals a
  potential problem upstream.

- **Skip rate calculated in the parser, not downstream.** The skip
  rate is a direct metric of parsing quality. The parser has the
  raw data to compute it, and it is logged alongside the other
  stats for immediate visibility.

- **Division by zero handled via early return.** When both counters
  are 0, the function returns early with only the two counters.
  This avoids a conditional inside the calculation and keeps the
  happy path clean.

---

# Error Handling

## Malformed Lines

A line is considered malformed if any field cannot be split into a
`key=value` pair — detected by checking `len(split_log) < 2`.

When a malformed line is detected:
- A `WARNING` is logged identifying the line number
- `_parse_fields` returns `None`
- `parse_logs` increments the skip counter and continues processing

## Empty Values

A field with a key but no value (e.g. `cpu=`) produces
`split_log = ['cpu', '']`. The empty string passes the length check
but is caught by the `not split_log[1]` guard clause. The warning
message includes the field name for clarity.

Without this check, an empty value would be stored as an empty string
in the dict. This is worse than `NaN` in a DataFrame because `.isna()`
does not detect empty strings — the bad data would be invisible to
downstream quality checks.

## Missing Fields

A line missing a field entirely (e.g. no `mem=` token at all) produces
a valid dict with fewer keys than expected. `_verify_columns` detects
this by comparing the dict keys against the expected columns list.

## Empty Messages

A missing or empty message is detected in `parse_logs` before any
field parsing occurs. If `message.strip('"\n')` produces an empty
string, the line is skipped immediately.

## Implicit Handling of Malformed `msg` Field

A malformed `msg` field — for example `msg"Seat booked"` instead of
`msg="Seat booked"` — is handled implicitly without extra logic.

`str.partition(" msg=")` does not find the separator and returns the
full line as the first element unchanged. The malformed `msg"Seat booked"`
token then reaches `_parse_fields` as a field without a valid `=`
separator, triggering the same guard clause as any other malformed field.

## Empty Input

When the iterator produces no lines (empty log file), both counters
remain at 0. `_skip_report` detects this and logs a warning. The
empty list is returned to the caller, where the analysis layer's
`_verify_columns` will raise a `ValueError` for an empty list.

## Logging

Uses Python's standard `logging` module. A module-level logger is
created once using `logging.getLogger(__name__)`.

```python
logger = logging.getLogger(__name__)
```

Logger configuration (handlers, format, level) is the responsibility
of the entry point (`main.py`), not this module. The logging level
in `main.py` is set to `INFO` to surface parsing statistics.

---

# Design Decisions

## Guard clause over exception handling for validation
Malformed fields are detected using `len()` instead of catching
`IndexError`. Exceptions should signal unexpected conditions, not serve
as the primary branching mechanism. The guard clause makes the validation
explicit and readable.

## `isdigit()` over try/except for type detection
Numeric detection uses `str.isdigit()` instead of attempting `int()`
and catching `ValueError`. This keeps exceptions for truly unexpected
situations and uses normal control flow for expected branching.

## Separate concerns in conditional blocks
The guard clauses (`if len < 2` and `elif not split_log[1]`) are
separate from the type detection chain (`if isdigit / elif timestamp /
else`). Guards handle validation and exit early. The chain handles
assignment logic. Mixing them would conflate two different concerns.

## `None` as sentinel value
`_parse_fields` returns `None` for malformed lines. This allows
`parse_logs` to use a simple `if log_dict is None` check to decide
whether to proceed with column validation.

## `_verify_columns` returns bool, not None
Unlike `_parse_fields` which returns `None` as a sentinel,
`_verify_columns` returns `True` or `False`. This is because the
check happens inside `parse_logs` where `continue` is used directly —
a boolean is clearer than checking for `None` in this context.

## Expected columns come from the caller
`parse_logs` receives the expected columns list as a parameter from
the pipeline orchestrator. The parser does not load config — it
receives what it needs. This is the same decoupling pattern used in
`_verify_columns()` in the analysis layer.

## Two layers of column validation are not redundant
The parser's `_verify_columns` validates each dict individually as it
is built. The analysis layer's `_verify_columns` validates the
complete list before DataFrame creation — catching the case where all
lines are rejected and the list arrives empty. Each layer validates
at its own level.

## Private function convention
`_parse_fields`, `_verify_columns`, and `_skip_report` are prefixed
with `_` to signal they are internal implementation details, not part
of the public interface of the module.

## No hardcoded field names in type detection
Type detection does not rely on a list of numeric field names. Instead,
`isdigit()` detects numeric values generically. This makes the parser
resilient to minor format changes without requiring updates to a field
registry.

## Logging over print
`logger.warning()` and `logger.info()` are used instead of `print()`
for all validation and statistics reporting. Functions should not have
console side effects, and logging gives the application control over
how and where messages are handled.

## Tuple return for data + metadata
`parse_logs` returns a tuple of `(parsed_logs, stats_dict)`. This is
appropriate because the function always returns exactly two things of
different nature — the data and metadata about the data. The stats
dict can grow internally (new metrics) without changing the tuple
structure. This avoids the fragility of positional tuples with many
elements (as seen in the generator's original config return).

---

# Changes from v3

- `parse_logs` now returns a tuple: `(list[dict], stats_dict)` —
  parsed logs and parsing statistics returned together
- Added `skipped_lines` counter in `parse_logs` — incremented at
  each rejection point (missing message, failed parse, missing columns)
- Lines processed count derived from `len(log_dict_list)` after
  the loop — O(1) on Python lists
- Added `_skip_report()` — builds stats dict, calculates skip rate,
  logs statistics at INFO level
- Empty input handled: when both counters are 0, logs WARNING and
  returns stats without skip_rate to avoid division by zero
- Logging level in `main.py` changed from WARNING to INFO to surface
  parsing statistics
- "Return parsing statistics" removed from Future Improvements —
  resolved

---

# Future Improvements (Planned)

- ~~Parse `timestamp` field into a proper `datetime` object~~ — resolved
  in `_parse_fields()` using `datetime.fromisoformat()` from Python's
  standard library.
- ~~Validate that all expected fields are present before accepting a
  line~~ — resolved with `_verify_columns()` and empty value guard.
- ~~Return parsing statistics (lines processed, lines skipped)~~ —
  resolved with tuple return and `_skip_report()`.
- Support configurable field type mappings from `config.yaml`
- Support for additional log formats
