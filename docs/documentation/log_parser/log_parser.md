# Log Parser — Implementation (v2)

## Objective

Implement a log parser module for the airline booking backend pipeline.

The goal of this phase is to:

- Transform raw log strings into structured Python dictionaries
- Extract all fields from each log line
- Apply correct data types to numeric fields
- Handle malformed lines gracefully without crashing the pipeline
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

## `parse_logs(log_list)`

Parses a list of raw log strings into a list of dictionaries.

**Parameters:**
- `log_list` (list[str]) — list of raw log lines as returned by `log_reader.py`

**Returns:**
- List of dicts — one dictionary per valid log line

**Behavior:**
- Malformed lines are skipped and logged as warnings
- Valid lines are always included regardless of field values

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

## Two-Function Design

The parser is split into two functions with distinct responsibilities:

- `parse_logs(log_list)` — orchestrates iteration over all lines
- `_parse_fields(fields, line_number)` — parses a single line's
  key=value fields (private)

This separation allows `parse_logs` to handle skip logic cleanly based
on the return value of `_parse_fields`.

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

## Field Parsing

After isolating the message, the remaining fields are split by space.
Each `key=value` pair is then split by `=` to extract the key and value.

## Type Detection and Conversion

Type detection uses a guard clause followed by explicit checks instead
of relying on exceptions for control flow.

For each field, the logic follows this order:

1. **Guard clause** — if `split_log` has fewer than 2 elements, the line
   is malformed. Log a warning and return `None` immediately.
2. **Numeric check** — if the value is numeric (`str.isdigit()`), convert
   to `int`.
3. **Timestamp check** — if the key is `"timestamp"`, parse with
   `datetime.fromisoformat()`.
4. **Default** — store as string.

```python
if len(split_log) < 2:
    logger.warning(f"Malformed line skipped at line {line_number}")
    return None

if split_log[1].isdigit():
    log_dict[split_log[0]] = int(split_log[1])
elif split_log[0] == "timestamp":
    log_dict[split_log[0]] = datetime.fromisoformat(split_log[1])
else:
    log_dict[split_log[0]] = split_log[1]
```

The guard clause is a separate `if` from the type detection chain
because they represent different concerns — validation vs assignment.

## Message Cleanup

The `msg` value is stripped of surrounding quotes and trailing newline
characters using `.strip('"\n')`.

```python
log_dict["msg"] = message.strip('"\n')
```

Both characters are stripped together because log lines read from disk
via `readlines()` include a trailing `\n`. A naive `.strip('"')` would
leave the newline after the closing quote, producing `'Booking confirmed"\n'`
instead of `'Booking confirmed'`.

## Line Numbering

`enumerate(log_list, start=1)` is used to track the human-readable line
number. This is passed to `_parse_fields` so that warning messages
reference the correct line.

---

# Error Handling

## Malformed Lines

A line is considered malformed if any field cannot be split into a
`key=value` pair — detected by checking `len(split_log) < 2`.

When a malformed line is detected:
- A `WARNING` is logged identifying the line number
- `_parse_fields` returns `None`
- `parse_logs` skips the line and continues processing

This uses a guard clause pattern (early return) instead of exception
handling, which is cleaner for expected validation logic.

## Implicit Handling of Malformed `msg` Field

A malformed `msg` field — for example `msg"Seat booked"` instead of
`msg="Seat booked"` — is handled implicitly without extra logic.

`str.partition(" msg=")` does not find the separator and returns the
full line as the first element unchanged. The malformed `msg"Seat booked"`
token then reaches `_parse_fields` as a field without a valid `=`
separator, triggering the same guard clause as any other malformed field.

This is an example of implicit error coverage — the general malformation
logic handles a specific edge case without requiring dedicated code.

## Logging

Uses Python's standard `logging` module. A module-level logger is
created once using `logging.getLogger(__name__)`.

```python
logger = logging.getLogger(__name__)
```

Logger configuration (handlers, format, level) is the responsibility
of the entry point (`main.py`), not this module. This follows the
standard Python logging pattern for library and module code.

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
The guard clause (`if len < 2`) is a separate `if` statement from the
type detection chain (`if isdigit / elif timestamp / else`). The guard
handles validation and exits early. The chain handles assignment logic.
Mixing them in a single `if/elif` would conflate two different concerns.

## `None` as sentinel value
`_parse_fields` returns `None` for malformed lines. This allows
`parse_logs` to use a simple `if log_dict is not None` check to decide
whether to append the result — clean and idiomatic Python.

## Private function convention
`_parse_fields` is prefixed with `_` to signal it is an internal
implementation detail, not part of the public interface of the module.

## No hardcoded field names
Type detection does not rely on a list of numeric field names. Instead,
`isdigit()` detects numeric values generically. This makes the parser
resilient to minor format changes without requiring updates to a field
registry.

## Logging over print
`logger.warning()` is used instead of `print()` for malformed line
reporting. This follows Python best practices — functions should not
have console side effects, and logging gives the application control
over how and where messages are handled.

---

# Changes from v1

- `_parse_logs_without_message()` renamed to `_parse_fields()` — reflects
  what the function actually does (parse key=value fields)
- `splitted_log` renamed to `split_log` — corrected English grammar
- Malformed line detection changed from `IndexError` exception to
  `len()` guard clause
- Numeric detection changed from `try int() / except ValueError` to
  `str.isdigit()` check
- Guard clause separated from type detection logic into its own `if` block

---

# Future Improvements (Planned)

- ~~Parse `timestamp` field into a proper `datetime` object~~ — resolved
  in `_parse_fields()` using `datetime.fromisoformat()` from Python's
  standard library. The parser is responsible for delivering correctly
  typed data, not just raw strings. Using the standard library keeps
  this conversion free of external dependencies like pandas.
- Validate that all expected fields are present before accepting a line
- Support configurable field type mappings from `config.yaml`
- Return parsing statistics (lines processed, lines skipped)
- Support for additional log formats
