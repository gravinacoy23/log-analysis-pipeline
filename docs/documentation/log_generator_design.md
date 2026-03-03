# Log Generator – Initial Implementation

## Objective

Implement the initial version of a synthetic log generator for the airline booking backend simulation.

The goal of this phase is to:

- Define a consistent and parseable log format
- Build a modular log generation structure
- Generate valid log lines for multiple services
- Prepare the foundation for future behavior simulation

---

## System Context

The simulated system represents an airline booking platform composed of three services:

- shopping
- pricing
- booking

Each generated log represents a single backend request event.

---

## Log Format

Each log entry follows this structure:

<timestamp> service=<service> user=<id> cpu=<value> mem=<value> response=<ms> level=<LEVEL> msg="<message>"

Example:

2026-03-02T18:23:11Z service=pricing user=42 cpu=73 mem=68 response=842 level=INFO msg="Price calculation completed"

---

## Implementation Details

### Modular Functions

The generator is structured using small, focused functions:

- `generate_timestamp()`  
- `generate_service()`  
- `generate_message(service)`  
- `build_log_line()`

This modular approach ensures:

- Clear separation of responsibilities
- Future extensibility
- Easier refactoring

---

## Randomization Strategy

For the initial implementation:

- Services are selected randomly
- Users are generated between 1–100
- CPU usage between 30–70
- Memory usage between 40–75
- Response time between 200–900 ms
- Log level randomly selected from INFO/WARNING/ERROR
- Message selected based on service

At this stage, no conditional probability logic has been introduced.

---

## Execution Behavior

The script includes a proper execution guard:

if __name__ == "__main__":

This ensures that log generation runs only when the script is executed directly, not when imported as a module.

---

## Directory Management

### `make_directory()`

Creates the `data/raw` directory dynamically if it does not exist.

This function ensures that the log generator is environment-independent and does not rely on pre-created folders.

### Design Decisions

- Uses `pathlib` for OS-independent path handling.
- Resolves the script location using `__file__` to ensure portability.
- Navigates to the project root dynamically.
- Creates directories using:

    dynamic_dir.mkdir(parents=True, exist_ok=True)

This guarantees:

- No failure if the directory already exists.
- No dependency on the current working directory.
- Consistent behavior across operating systems.
- Compatibility with future Docker execution.

### Why This Matters

In production-oriented systems, scripts must be self-sufficient and should not depend on manual environment setup.  
This function ensures reproducibility and portability of the log generation process.

## Future Improvements (Planned)

- Conditional error probability based on CPU and response time
- Peak vs off-peak hour simulation
- Service-specific instability modeling
- Writing logs to service-specific files
- Temporal correlation between events
