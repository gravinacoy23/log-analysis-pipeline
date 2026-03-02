# Month 1 -- Week 1 (Sprint 1)

## Sprint Goal

Build the foundation of the log pipeline:

-   Create project structure
-   Implement log generator
-   Implement log reader
-   Implement basic parser

No pandas yet. No visualization yet. No Docker yet.

------------------------------------------------------------------------

# Day-by-Day Breakdown

## Day 1

-   Create repository structure
-   Initialize Git
-   Create README
-   First commit

------------------------------------------------------------------------

## Day 2

-   Create `log_generator.py`
-   Generate 50--100 synthetic log entries
-   Save to `data/raw/app.log`

Commit changes.

------------------------------------------------------------------------

## Day 3

-   Implement `reader.py`
-   Read log file safely
-   Handle file-not-found exception

Commit changes.

------------------------------------------------------------------------

## Day 4

-   Implement `parser.py`
-   Parse one log line into dictionary
-   Handle malformed lines gracefully

Commit changes.

------------------------------------------------------------------------

## Day 5

-   Integrate reader + parser in `main.py`
-   Print structured logs

Commit changes.

------------------------------------------------------------------------

## Day 6

-   Refactor if needed
-   Improve naming
-   Improve error handling

Commit changes.

------------------------------------------------------------------------

## Day 7 (Sprint Review)

-   Document what was learned
-   Document difficulties
-   Push final version
-   Reflect on improvements

------------------------------------------------------------------------

# Sprint Deliverable

At the end of Week 1 you must have:

-   Synthetic logs generated automatically
-   Logs read from file
-   Logs parsed into dictionaries
-   At least 5--7 commits
-   Documentation updated

