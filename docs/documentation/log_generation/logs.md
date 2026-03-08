Log Format Specification

Each log line must follow this structure:

timestamp=<timestamp>service=<service_name>user=<id> cpu=<value> mem=<value> response_time=<ms> level=<LEVEL> msg="<message>"

timestamp=2026-03-02T18:23:11Z service=pricing-service user=42 cpu=73 mem=68 response=842 level=INFO msg="Price calculation completed"
