# Input Null Bytes Injection

## Issue
An agent accepts input containing embedded null bytes (`\x00`) — whether from malicious crafting, corrupted upstream data, or binary content misrouted into a text field — and passes it to a downstream layer (a C-based library, a filesystem call, a database driver, or a validation regex) whose string handling treats the null byte as a terminator. The agent's own validation logic sees the full string and approves it, but the consuming layer only sees the truncated prefix, creating a gap between what was validated and what was actually acted on.

**Frequency**: Rare

**Symptoms**
- A filename or path passed validation but the file operation acts on an unexpectedly short/different path
- Validation logic (e.g. "must end in .pdf") passes on a string like `"report.pdf\x00.exe"` because the check saw the full string while the OS or library only processed up to the null byte
- Log entries and application-layer records show the full string, but filesystem/database state reflects only the truncated portion
- Intermittent, hard-to-reproduce failures that correlate with specific upstream systems known to pass through binary or corrupted data
- Security scanners flag null-byte sequences in fields that are supposed to be pure text

## Root Cause
Many validation and business-logic layers are written in null-byte-safe languages (Python, Java, Go, JavaScript) where strings carry an explicit length and a null byte is just another character, so the agent's own checks run correctly against the entire string. But the string frequently gets handed off to a lower layer — a C library, a shell command, a legacy filesystem API, certain database drivers — that represents strings as null-terminated buffers, where processing silently stops at the first `\x00`. The mismatch between "length-prefixed string semantics" at the validation layer and "null-terminated string semantics" at the execution layer creates a gap an attacker or corrupted input can exploit: craft a string that passes the length-aware check but is truncated differently by the terminator-aware consumer.

## Example
```
A document-processing agent validates uploaded filenames against an
allowlist of extensions before saving them:

    if filename.endswith((".pdf", ".docx", ".txt")):
        save_to_storage(filename, contents)

A malformed upload (from a fuzzer or a corrupted client) submits the
filename "invoice.pdf\x00.sh". The Python-level check sees the full
string and confirms it ends in ".pdf" -- wait, it doesn't, it ends in
".sh", so this particular check fails; but a laxer check using
`".pdf" in filename` would pass.

Assume the laxer substring check is in place: it passes because
".pdf" appears in the string. save_to_storage then calls into an
underlying C-based storage library via ctypes, which treats the
filename as a null-terminated buffer and writes the file as
"invoice.pdf" instead -- but a still more dangerous variant occurs
when the reverse happens: the file is actually written using the
full null-containing path by one layer while a permissions check
earlier only evaluated "invoice.pdf", approving an operation that a
policy would have blocked had it seen the true, differently-typed
target path.
```

## Statistics
| Finding | Context |
|---------|---------|
| Null-byte injection is a long-documented class of poison-null-byte vulnerability, historically most common in file-path and filename validation | Well-established pattern in application security literature, not agent-specific |
| A small but nonzero share of malformed-input security findings in agent pipelines that shell out or call native libraries involve null-byte truncation | Typical range observed in security review findings |
| Rejecting any input containing `\x00` at the ingestion boundary eliminates the class of bug entirely with negligible false-positive cost for legitimate text fields | Estimated from the rarity of legitimate null bytes in user-facing text fields |

## Mitigations
1. **Reject null bytes at ingestion**: Scan and reject any text-field input containing `\x00` at the earliest possible validation point, since legitimate user-facing text essentially never contains one.
2. **Match string semantics across layers**: When passing strings to native/C-based libraries, shell commands, or legacy APIs, be explicit about null-terminated vs. length-prefixed semantics, and never assume the validating layer and the executing layer interpret the string the same way.
3. **Avoid shelling out with unsanitized strings**: Prefer library calls with structured parameters over constructing shell commands or native buffer calls from raw validated strings, removing the class of terminator-mismatch entirely.
4. **Defense-in-depth path validation**: For filesystem operations specifically, re-validate the resolved/canonical path immediately before the write or read, not just the originally submitted filename string.
5. **Fuzz validation logic with control characters**: Include null bytes and other control characters in routine fuzz/security testing of any input validation path that feeds a native or shell-based consumer.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| null_byte_input_rate | Share of ingested text fields containing a `\x00` byte | Alert if > 0 (should be near-zero) |
| validation_execution_path_mismatch_count | Count of cases where the string passed to validation differs from the string that reached the executing layer | Alert on any occurrence |
| native_call_reject_rate | Rate of native/shell calls rejected by control-character pre-filters | Informational, track for trend anomalies |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Null byte detected in text input | Any ingested field contains `\x00` | High | Reject the input, log source system, flag for security review if pattern recurs |
| Suspicious filename/path pattern | Filename or path contains control characters combined with a trusted-looking extension | High | Block the file operation, quarantine the upload, alert security team |

## Related Patterns
- [Input Special Character Handling](./input-special-character-handling.md) - null bytes are a specific, especially dangerous instance of the broader special-character handling problem
- [Input Validation Bypass](./input-validation-bypass.md) - null-byte truncation is one concrete technique for bypassing a validation rule via an encoding edge case
- [Output Injection Vulnerability](./output-injection-vulnerability.md) - both stem from mismatched string-handling assumptions between the validating and executing layers
