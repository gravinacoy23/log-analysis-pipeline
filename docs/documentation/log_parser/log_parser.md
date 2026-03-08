# Log Parser — Implementation (v1)

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
- `_parse_line(metrics, line_number)` — parses a single line's fields (private)

This separation allows `parse_logs` to handle skip logic cleanly based
on the return value of `_parse_line`.

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

## Type Conversion

Numeric fields are cast to `int` automatically using a try/except pattern.
Fields that cannot be converted to `int` are stored as strings.

```python
try:
    log_dict[key] = int(value)
except ValueError:
    log_dict[key] = value
```

This avoids hardcoding which fields are numeric and handles the format
in a generic way.

## Message Cleanup

The `msg` value is stored with surrounding quotes stripped using `.strip('"')`.

```python
log_dict["msg"] = message.strip('"')
```

## Line Numbering

`enumerate(log_list, start=1)` is used to track the human-readable line
number. This is passed to `_parse_line` so that warning messages
reference the correct line.

---

# Error Handling

## Malformed Lines

A line is considered malformed if any field cannot be split into a
`key=value` pair — specifically when `splitted_log[1]` raises an
`IndexError`.

When a malformed line is detected:
- A `WARNING` is logged identifying the line number
- `_parse_line` returns `None`
- `parse_logs` skips the line and continues processing

```python
except IndexError:
    logger.warning(f"Malformed line skipped at line {line_number}")
    return None
```

## Implicit Handling of Malformed `msg` Field

A malformed `msg` field — for example `msg"Seat booked"` instead of
`msg="Seat booked"` — is handled implicitly without extra logic.

`str.partition(" msg=")` does not find the separator and returns the
full line as the first element unchanged. The malformed `msg"Seat booked"`
token then reaches `_parse_line` as a field without a valid `=` separator,
triggering the same `IndexError` path as any other malformed field.

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

## `None` as sentinel value
`_parse_line` returns `None` for malformed lines. This allows `parse_logs`
to use a simple `if log_dict is not None` check to decide whether to
append the result — clean and idiomatic Python.

## Private function convention
`_parse_line` is prefixed with `_` to signal it is an internal
implementation detail, not part of the public interface of the module.

## No hardcoded field names
Type conversion uses try/except rather than an explicit list of numeric
fields. This makes the parser more resilient to minor format changes
without requiring updates to a field registry.

## Logging over print
`logger.warning()` is used instead of `print()` for malformed line
reporting. This follows Python best practices — functions should not
have console side effects, and logging gives the application control
over how and where messages are handled.

---

# Future Improvements (Planned)

- Parse `timestamp` field into a proper `datetime` object
- Validate that all expected fields are present before accepting a line
- Support configurable field type mappings from `config.yaml`
- Return parsing statistics (lines processed, lines skipped)
- Support for additional log formats
