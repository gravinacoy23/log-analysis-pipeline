# NASA HTTP Access Logs — Format Analysis

## Dataset Source

NASA Kennedy Space Center WWW server access logs.
Source: https://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html

**File used:** August 1995 (Aug 04 to Aug 31)
~1.5 million log entries.

Note: No data exists between 01/Aug/1995:14:52:01 and
03/Aug/1995:04:36:13 — the server was shut down due to
Hurricane Erin. This is a real-world edge case the pipeline
must handle gracefully (gap in data, not malformed data).

---

## Sample Log Line

```
ppptky455.asahi-net.or.jp - - [01/Aug/1995:06:10:01 -0400] "GET /images/WORLD-logosmall.gif HTTP/1.0" 200 669
```

---

## Field-by-Field Analysis

### Field 1 — Host

- **Example:** `ppptky455.asahi-net.or.jp` or `199.72.81.55`
- **Contains:** The source of the request — either a resolved
  hostname or an IP address when DNS lookup failed
- **Data type:** Always string. Even when the value is an IP
  address, it should be treated as string — there is no
  mathematical operation to perform on an IP
- **Delimiter:** First field in the line, followed by a space
- **Presence:** Always present

---

### Field 2 — RFC 1413 Identity

- **Example:** `-`
- **Contains:** Client identity as defined by RFC 1413. In
  practice, this field is almost always empty (represented
  as `-`)
- **Data type:** String
- **Delimiter:** Space on both sides
- **Presence:** Always present positionally, almost always `-`
- **Note:** This field can be ignored for analysis but must be
  accounted for in parsing to avoid misaligning subsequent
  fields

---

### Field 3 — Authenticated User

- **Example:** `-` or `frank`
- **Contains:** The username if HTTP authentication was used.
  Empty (represented as `-`) when no authentication occurred
- **Data type:** String
- **Delimiter:** Space on both sides
- **Presence:** Always present positionally, rarely has a value
  in this dataset (first 7000+ lines all show `-`)
- **Note:** Same as Field 2 — must be parsed to maintain field
  alignment, even if discarded for analysis

---

### Field 4 — Timestamp

- **Example:** `[01/Aug/1995:06:08:37 -0400]`
- **Contains:** Date and time of the request with timezone offset
- **Data type:** Datetime
- **Format:** `[DD/Mon/YYYY:HH:MM:SS -0400]`
- **Delimiter:** Enclosed in square brackets `[]`. Space separates
  it from adjacent fields
- **Presence:** Always present
- **Timezone:** All entries use `-0400` (Eastern Daylight Time)
- **Note:** The format is different from the synthetic logs which
  used ISO 8601 (`2026-03-09T22:15:52Z`). The parser will need
  a different datetime parsing strategy

---

### Field 5 — Request Line

- **Example:** `"GET /images/WORLD-logosmall.gif HTTP/1.0"`
- **Contains:** Three sub-fields inside double quotes:
  1. **HTTP method** — `GET`, `POST`, `HEAD`, etc.
  2. **Endpoint** — the requested URL path
  3. **HTTP version** — protocol version (`HTTP/1.0`)
- **Data type:** String (composite — may be split into three
  separate columns during parsing)
- **Delimiter:** Enclosed in double quotes `""`. Sub-fields
  separated by spaces within the quotes
- **Presence:** Always present, though the content may be
  malformed in some entries
- **Note:** This is effectively three fields packed into one.
  The parser should extract method, endpoint, and HTTP version
  as separate columns for meaningful analysis

---

### Field 6 — HTTP Status Code

- **Example:** `200`, `404`, `500`, `302`
- **Contains:** The HTTP response status code from the server
- **Data type:** Integer by format, but behaves as a **category**.
  Status codes are not continuous values — `200` is not "double"
  `100`. Analysis should count occurrences per code (like
  `count_by_level` in the current pipeline), not compute averages
- **Delimiter:** Space on both sides
- **Presence:** Always present
- **Common values:** 200 (OK), 302 (redirect), 304 (not modified),
  404 (not found), 500 (server error)
- **Note:** This field is the most likely candidate for defining
  `is_error` in the new feature engineering — e.g.
  `status_code >= 400` or `status_code >= 500`

---

### Field 7 — Response Size (bytes)

- **Example:** `669`, `44877`, `0`
- **Contains:** The number of bytes in the server's response body
- **Data type:** Integer
- **Delimiter:** Last field in the line, preceded by space
- **Presence:** Always present. A value of `0` means the server
  sent no response body — typical for redirects (301, 302) and
  some error responses
- **Note:** This is a numeric field suitable for distribution
  analysis, thresholds, and feature engineering (e.g. response
  size buckets)

---

## Delimiter Summary

| Delimiter | Fields |
|-----------|--------|
| Space | Separates most fields |
| `[ ]` | Encloses timestamp |
| `" "` | Encloses request line |
| `-` | Represents empty value (identity, user) |

The mixed delimiters mean `str.split(" ")` alone cannot parse
this format. A **regex approach** is the standard and most
maintainable strategy for Common Log Format — one pattern
captures all fields regardless of delimiter type.

---

## Parsing Strategy Decision

**Chosen approach: Regular expressions.**

**Rationale:**
- The CLF has mixed delimiters (spaces, brackets, quotes) that
  make chained `str.split()` calls fragile and hard to read
- A single regex pattern captures all fields in one match
- Regex is the standard approach for parsing CLF in the industry
- More maintainable than multiple splits — one pattern to update
  vs multiple string operations scattered across functions
- The original `key=value` parser used `split()` because every
  field had the same `key=value` structure. CLF does not have
  that uniformity — regex is the right tool for this format

---

## Comparison with Synthetic Format

Full field mapping is documented in `docs/migration_plan.md`.

Key differences:
- **No service concept** — synthetic logs had shopping/pricing/booking,
  access logs have endpoints instead
- **No CPU/memory/response_time** — synthetic metrics do not exist
  in web server logs. Response size and status code are the new
  numeric fields
- **No level (INFO/WARNING/ERROR)** — status codes serve a similar
  purpose: 2xx = healthy, 4xx = client error, 5xx = server error
- **New fields** — IP address, HTTP method, endpoint, HTTP version,
  referer, user agent (the last two in Combined format only, not
  present in this dataset)
- **Timestamp format** — completely different, requires new parsing
