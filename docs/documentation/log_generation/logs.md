# Log Format Specification

Each log line follows the Common Log Format (CLF):

```
host identity user [timestamp] "request" status size
```

Example:

```
ppptky455.asahi-net.or.jp - - [01/Aug/1995:06:10:01 -0400] "GET /images/WORLD-logosmall.gif HTTP/1.0" 200 669
```

Field details documented in `docs/migration_plan/format_analysis.md`.
