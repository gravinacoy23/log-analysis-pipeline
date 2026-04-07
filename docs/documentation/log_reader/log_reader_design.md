# Log Reader — Design (v4)

## Objective

Provide the ingestion layer for the log analysis pipeline.
Reads log files from a configurable directory path and yields
raw lines to the parser. Handles encoding issues gracefully
and validates the directory before reading.

---

## System Context

The log reader is the first stage of the ingestion layer. It
sits between the raw log files on disk and the parser. Its only
responsibility is to access the file system and deliver raw
content. It does not know anything about the log format or
structure — that is the parser's responsibility.

```
data/raw/access_logs/ → log_reader.py → log_parser.py
```

---

## Module Location

```
src/ingestion/log_reader.py
```

---

## Function: load_all_logs()

### Parameters

- `path` — string with the relative path to the log directory,
  loaded from `config.yaml` under `paths.log_dir`

### Returns

- `Iterator[str]` — yields one string per log line across all
  files in the directory

### Implementation Details

- Calls `_load_path()` to construct and validate the full path
- Calls `_load_all_files()` to collect and sort all files
- Opens each file with `errors="ignore"` to handle non-UTF-8
  bytes without crashing
- Yields one line at a time using the generator pattern

### Design Decisions

- **Single public function.** The previous reader had two public
  functions: `load_service_logs(service)` for single-service
  reads and `load_all_logs(services)` for multi-service reads.
  The migration to real logs eliminates the per-service directory
  structure — all logs live in a single directory. One function
  is sufficient.

- **Path received as parameter from config.** The directory path
  is defined in `config.yaml` and passed by the pipeline
  orchestrator. The reader does not load config directly — same
  decoupling pattern used across the project. The path is a
  relative string (e.g. `data/raw/access_logs`); the reader
  constructs the absolute path using `__file__` for the project
  root and `pathlib` for portability.

- **`errors="ignore"` on file open.** The NASA dataset contains
  bytes that are not valid UTF-8. Rather than crashing, the
  reader silently drops invalid bytes. If this corrupts a line,
  the parser's regex will fail to match it and skip it via guard
  clause — each layer handles its own validation.

- **Generator pattern preserved.** Lines are yielded one at a
  time, avoiding loading the full dataset into memory. With
  ~1.57M lines, this is important for memory efficiency. The
  parser receives the generator and processes each line
  independently.

---

## Function: _load_path()

### Parameters

- `path` — string with the relative path from config

### Returns

- `Path` — resolved absolute path to the log directory

### Raises

- `ValueError` — if the resolved path is not a valid directory

### Implementation Details

- Resolves the project root using `Path(__file__).parents[2]`
- Constructs the full path by joining root with the config path
- Calls `.resolve()` for absolute path resolution
- Validates the directory exists using `.is_dir()` before
  returning — fail fast principle

### Design Decisions

- **Combines root resolution with config path.** `__file__`
  provides machine-independent root resolution. The config
  provides the relative path. Together they produce a portable
  absolute path without hardcoding any directory name.

- **Validates immediately.** If the path does not exist, the
  reader raises before attempting to iterate files. The error
  message identifies the source (config file) to help debugging.

---

## Function: _load_all_files()

### Parameters

- `path` — `Path` object pointing to the log directory

### Returns

- `list[Path]` — sorted list of all files in the directory

### Raises

- `ValueError` — if the directory contains no files

### Implementation Details

- Iterates over the directory using `path.iterdir()`
- Skips non-file entries (subdirectories) using guard clause
- Validates the result is not empty — fail fast
- Sorts alphabetically for deterministic processing order

### Design Decisions

- **Fail fast on empty directory.** An empty directory means no
  data to process. Raising immediately with a clear message is
  preferable to letting the pipeline fail downstream in the
  parser or analysis layer with a less descriptive error.

- **Guard clause for non-files.** Uses `if not file.is_file():
  continue` instead of `if file.is_file(): append`. Consistent
  with the guard clause pattern used across the project.

- **Sorted for determinism.** File processing order is
  alphabetical, ensuring reproducible results across runs and
  operating systems.

---

## Deprecated (removed in v4)

| Function | Reason |
|---|---|
| `load_service_logs(service)` | Per-service directory structure no longer exists |
| `load_all_logs(services)` | Replaced by new `load_all_logs(path)` with different interface |
| `_load_all_path_names(services)` | Service path building no longer needed |

All deprecated code is preserved in git history on the `main`
branch.

---

## Changes from v3

- Complete rewrite for real log migration (Month 5, Sprint 10)
- Single public function `load_all_logs(path)` replaces both
  previous public functions
- Log directory path received from config instead of constructed
  from service names
- Added `errors="ignore"` on file open for non-UTF-8 byte
  handling
- Added guard clause for empty directory in `_load_all_files()`
- Added directory existence validation in `_load_path()`
- Removed all service-specific logic and helper functions

---

## Future Improvements (Planned)

- Support reading logs within a specific time range
