# Log Parser — Design (v5)

## Objective

Provide the processing layer for the log analysis pipeline.
Receives raw log lines from the reader and parses them into
structured dictionaries ready for DataFrame creation. Validates
line structure using regex, extracts and converts fields, and
reports parsing statistics.

---

## System Context

The parser sits between the reader and the analysis layer. It
receives raw strings and produces structured data. It validates
format — the analysis layer validates content.

```
log_reader.py → raw lines → log_parser.py → list[dict] + stats → log_analysis.py
```

---

## Module Location

```
src/processing/log_parser.py
```

---

## Dependencies

- `re` — compiled regex pattern for Common Log Format matching
- `datetime` — `strptime` for timestamp conversion
- `logging` — warning and info messages for skipped lines and
  statistics

---

## Function: parse_logs()

### Parameters

- `logs` — `Iterator[str]` of raw log lines from the reader
- `expected_cols` — `list[str]` of column names from config,
  used for field mapping and column verification

### Returns

- `tuple[list[dict[str, Any]], dict[str, int | float]]` — parsed
  log dicts and a stats dict with lines_processed, skipped_lines,
  and skip_rate

### Implementation Details

- Compiles the regex pattern once before the loop using
  `re.compile()` — avoids recompiling on every iteration across
  ~1.57M lines
- Iterates over the log lines with `enumerate(start=1)` for
  line number tracking
- Guard clause: if `pattern.match()` returns `None`, the line
  is completely malformed — skip, log warning, increment counter
- Calls `_parse_fields()` to extract and convert field values
- Calls `_verify_columns()` to confirm all expected columns
  are present in the resulting dict
- Calls `_skip_report()` at the end to build and log statistics

### Regex Pattern

```python
r"(\S+) (\S+) (\S+) \[(.+?)\] \"(.+?)\" (\d+) (\S+)"
```

Captures 7 groups from Common Log Format:
1. Host (IP or hostname)
2. Identity (RFC 1413, almost always `-`)
3. User (authenticated user, almost always `-`)
4. Timestamp (inside `[]`)
5. Request line (inside `""` — contains method, endpoint,
   and optionally HTTP version)
6. Status code
7. Response size (may be `-`)

### Guard Clause Flow

```
1. re.match returns None         → skip (malformed line)
2. _parse_fields returns None    → skip (field-level issue)
3. _verify_columns returns False → skip (missing column)
4. All pass                      → append to result list
```

### Design Decisions

- **`re.compile()` outside the loop.** The regex pattern is
  constant. Compiling once and reusing the pattern object
  avoids redundant compilation on every line. Standard practice
  for large-file parsing.

- **Orchestration structure preserved from v4.** The flow
  (iterate → validate → skip or collect → report) is identical
  to the previous parser. What changed is the parsing logic
  inside, not the orchestration around it.

- **Stats tuple return preserved.** The parser returns both
  the parsed data and parsing statistics as a tuple — same
  interface as v4. The pipeline unpacks both; the caller
  decides what to do with the stats.

---

## Function: _parse_fields()

### Parameters

- `split_log_line` — `tuple[str | Any, ...]` of captured groups
  from the regex match
- `line_number` — current line number for warning messages
- `expected_columns` — `list[str]` of column names for field
  mapping

### Returns

- `dict[str, Any] | None` — parsed dict mapping column names
  to values, or `None` if the line should be skipped

### Implementation Details

- Calls `_parse_request_line()` to expand the request group
  into method, endpoint, and protocol_version — producing a flat
  tuple of 9 values from the original 7
- Uses `zip(values, column_names)` to map each value to its
  corresponding column name in a single pass
- Field-specific processing:
  - **`response_size`:** converts to `int` if digit, converts
    `-` to `0`, rejects anything else as malformed
  - **`http_response`:** converts to `int` if digit, rejects
    anything else as malformed
  - **`timestamp`:** converts to `datetime` using `strptime`
    with format `%d/%b/%Y:%H:%M:%S %z`
  - **`protocol_version`:** allowed to be `None` (some request lines
    lack HTTP version) — skipped by the empty-value guard
  - **All other fields:** stored as strings
- Guard clause: if a value is empty and the field is not
  `protocol_version`, the line is skipped with a warning

### Design Decisions

- **`zip()` for field mapping.** The regex produces values in
  a fixed positional order. The config provides column names
  in the same order. `zip()` pairs them naturally without
  index management.

- **`response_size` as `-` maps to `0`.** In CLF, `-` means
  no response body was sent — common for redirects (302) and
  some error responses. `0` represents the same meaning as a
  numeric value suitable for DataFrame operations. This is a
  representation of reality, not fabricated data.

- **`http_response` converted to `int`.** Status codes are
  numeric values needed for range comparisons (e.g. filtering
  `>= 400`, defining `is_error`). Converting in the parser
  keeps the analysis layer clean — it receives the correct
  type directly.

- **`protocol_version` allowed as `None`.** Some request lines in the
  NASA dataset contain only method and endpoint without an
  HTTP version. The method and endpoint are still valuable for
  analysis. `None` becomes `NaN` in the DataFrame, which pandas
  handles natively.

- **`timestamp` parsed with timezone.** The `%z` directive
  handles the `-0400` offset in the CLF timestamp format.
  The resulting `datetime` object is timezone-aware.

---

## Function: _parse_request_line()

### Parameters

- `split_log_line` — `tuple[str | Any, ...]` of captured groups
  from the regex match

### Returns

- `tuple[str]` — flat tuple with the request line expanded
  into method, endpoint, and protocol_version, replacing the original
  single request group

### Implementation Details

- Splits the request group (index 4) by spaces
- Filters empty strings from the split result
- Handles two cases:
  - **< 3 parts:** appends `None` for missing protocol_version
  - **>= 3 parts:** checks if the last element starts with
    `HTTP/` to determine if it is a protocol_version or part of the
    endpoint:
    - If last element starts with `HTTP/`: treats it as
      protocol_version, joins middle elements as endpoint
    - If last element does not start with `HTTP/`: joins all
      elements after method as endpoint, sets protocol_version to `None`
- Reassembles the full tuple: fields 0–3 + expanded request
  + fields 5–6

### Design Decisions

- **`HTTP/` prefix check for protocol_version detection.** The NASA
  dataset contains request lines where spaces in the endpoint
  produce 3+ parts but no protocol_version is present. Simply taking
  the last element as protocol_version would assign endpoint fragments
  as the protocol_version value. Checking for the `HTTP/` prefix
  distinguishes real protocol_versions from endpoint fragments without
  requiring config or external data.

- **`>= 3` instead of separate `== 3` and `> 3` branches.**
  Originally `== 3` was treated as the "normal" case requiring
  no adjustment, and `> 3` handled spaces in endpoints. However,
  some lines have exactly 3 parts where the last part is not a
  protocol_version (e.g. `"GET /path/page.html>Link</a>, a"` splits
  into 3 parts but `a` is not a protocol_version). Using `>= 3` with
  the `HTTP/` check handles both cases uniformly. For the normal
  case `["GET", "/path", "HTTP/1.0"]`, the check passes and
  `join` of a single-element list produces the element unchanged
  — no performance or correctness impact.

- **Handles spaces in endpoints.** Some NASA log entries have
  spaces within the URL path. Rather than skipping these lines,
  the first element is treated as method, and everything between
  method and protocol_version (or everything after method if no protocol_version)
  is joined as the endpoint.

- **`None` for missing protocol_version.** When the request line lacks
  a valid HTTP protocol_version, `None` is appended. The method and
  endpoint are still valid and useful for analysis.

- **Produces a flat tuple.** The caller (`_parse_fields`)
  expects a flat sequence of values matching the column name
  list. Expanding the request line in place keeps the mapping
  clean.

---

## Function: _verify_columns()

### Parameters

- `logs_dict` — `dict[str, Any]` containing one parsed log line
- `expected_cols` — `list[str]` of required column names
- `line_number` — current line number for warning messages

### Returns

- `bool` — `True` if all expected columns are present

### Implementation Details

- Iterates over expected column names and checks presence in
  the dict
- Returns `False` on first missing column
- Logs a warning identifying the missing column and line number

### Design Decisions

- **Unchanged from v4.** This function is generic — it checks
  column presence against a config-driven list. The migration
  to CLF does not affect its logic.

---

## Function: _skip_report()

### Parameters

- `skipped_lines` — counter of skipped lines
- `lines_processed` — counter of successfully parsed lines

### Returns

- `dict[str, int | float]` — stats dict with lines_processed,
  skipped_lines, and skip_rate (percentage)

### Implementation Details

- Handles the edge case of both counters being 0 (empty file)
  with a warning and returns without computing skip_rate
- Computes skip_rate as a percentage of total lines
- Logs all stats at INFO level

### Design Decisions

- **Unchanged from v4.** Generic reporting function — works
  regardless of log format.

---

## Data Quality Handling

| Case | Lines | Handling |
|---|---|---|
| Completely malformed (no regex match) | ~2 | Skipped by `parse_logs` guard clause |
| Missing endpoint (request line has < 2 parts) | 6 | Skipped by `_parse_fields` empty-value guard |
| Missing protocol_version (request line has < 3 parts) | ~1400 | `None` appended, becomes `NaN` in DataFrame |
| Missing protocol_version (request line has >= 3 parts, last element is not `HTTP/`) | ~few | Last element joined into endpoint, protocol_version set to `None` |
| Spaces in endpoint with protocol_version present | ~11 | Middle elements joined as single endpoint |
| Spaces in endpoint without protocol_version | ~few | All elements after method joined as endpoint, protocol_version `None` |
| Response size is `-` | ~10 | Converted to `0` |
| Binary/garbled request data with valid structure | 2 | Passes parser — content validation deferred to analysis layer (method not in expected values) |
| Non-UTF-8 bytes | ~few | Dropped by reader (`errors="ignore"`), parser sees cleaned line |
| **Total skipped** | **8** | **0.0005% skip rate** |

---

## Deprecated (removed in v5)

| Element | Reason |
|---|---|
| `str.partition(" msg=")` | Synthetic `key=value` format no longer used |
| `str.split("=")` field parsing | Replaced by regex capture groups |
| `isdigit()` for generic type detection | Replaced by field-specific conversion |
| `msg` field handling | Messages do not exist in CLF |

All deprecated code is preserved in git history on the `main`
branch.

---

## Changes from v4

- Complete rewrite of parsing logic for Common Log Format
  (Month 5, Sprint 10)
- Regex-based parsing replaces `key=value` string splitting
- `re.compile()` used for pattern compilation before the loop
- Added `_parse_request_line()` — splits request group into
  method, endpoint, and protocol_version with `HTTP/` prefix detection
  for distinguishing protocol_version from endpoint fragments
- `_parse_request_line()` uses `>= 3` branch with `HTTP/` check
  instead of separate `== 3` and `> 3` branches — handles
  edge case where exactly 3 parts are present but last part
  is not a protocol_version
- `_parse_fields()` rewritten — uses `zip()` for field-to-column
  mapping, field-specific conversion for timestamp, response
  size, http_response, and protocol_version
- `http_response` converted to `int` in parser — enables
  numeric range validation in analysis layer
- Guard clause added in `parse_logs()` for `None` regex match
- `_verify_columns()` and `_skip_report()` unchanged — generic
  functions that work across formats

---

## Future Improvements (Planned)

- Support additional log formats beyond CLF
