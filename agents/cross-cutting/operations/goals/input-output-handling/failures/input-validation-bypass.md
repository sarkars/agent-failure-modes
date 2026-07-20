# Input Validation Bypass

## Issue
An agent's input validation rule checks the input's surface form (a regex, a length check, an allowlist match) but the check can be satisfied by an encoding, formatting, or representation variant that is semantically equivalent to a blocked value while syntactically different enough to slip past the check. Unicode homoglyphs, alternate encodings, case variations, whitespace insertion, or double-encoding let disallowed content — a blocked word, a malicious path, an injection payload — pass a validator that was written to catch only the literal, canonical form.

**Frequency**: Occasional

**Symptoms**
- Content that is clearly a variant of a blocked pattern (different case, extra whitespace, homoglyph substitution) passes validation and reaches downstream systems
- Security or content-moderation review finds bypass content that "should have" been caught by an existing filter
- Validation logs show the rule firing correctly on the literal test cases used to build it, but production data reveals it missing near-identical variants
- The same semantic value is normalized differently depending on which code path processed it, so the validator's behavior appears inconsistent
- A previously effective validation rule appears to "stop working" after an unrelated encoding or library change elsewhere in the pipeline

## Root Cause
Most validation rules are written against a single canonical representation of the disallowed pattern — a specific string, a specific character set, a specific case — without first normalizing the input to that canonical form. But many formats support multiple representations of the same logical value: Unicode allows visually identical characters from different code points (homoglyphs), URL and HTML encoding allow the same character to be expressed multiple ways (`%2e%2e%2f` vs `../`), and case-insensitive systems still get validated with case-sensitive rules. When the input isn't normalized (decoded, case-folded, Unicode-normalized) *before* the validation check runs, the validator is only checking one of many equivalent surface forms, and any of the others sails through unexamined — the input didn't defeat the validation logic, it simply never entered the space the logic was checking.

## Example
```
A document-management agent blocks file uploads with paths attempting
directory traversal, using the check:

    if "../" in filepath:
        reject("path traversal attempt")

This correctly blocks a literal "../../etc/passwd". But the upload
endpoint decodes URL-encoded paths *after* this check runs, not before.
A request submits the path as "..%2f..%2fetc%2fpasswd" -- the literal
string the validator inspects contains no "../" substring, so it passes.

Downstream, the file-serving layer URL-decodes the path before opening
the file, turning "..%2f..%2fetc%2fpasswd" back into "../../etc/passwd"
and successfully traversing outside the intended upload directory. The
validation rule was logically correct for the case it was written
against, but because normalization (URL-decoding) happened after
validation instead of before, an encoded variant bypassed it entirely.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of input-validation-bypass security findings stem from validation occurring before normalization/decoding rather than after | Common pattern in application-security review findings, not agent-specific |
| Unicode homoglyph and encoding-variant bypasses are a well-established category in content-moderation and security-filter evasion | Established pattern in security and trust-and-safety literature |
| Reordering pipelines to normalize-then-validate closes the large majority of bypass techniques in a given class without new rules | Estimated from the structural nature of the fix relative to the vulnerability |

## Mitigations
1. **Normalize before validating, always**: Fully decode (URL-decode, HTML-entity-decode) and Unicode-normalize (NFC/NFKC) input to its canonical form *before* any validation check runs, so the validator only ever inspects one representation per logical value.
2. **Validate on the decoded/executed form, not the transport form**: Ensure the exact string that will ultimately be used (opened as a path, executed as a query) is the same string that was validated — validating an intermediate encoded representation that differs from what's later decoded is the core of this bug class.
3. **Prefer allowlists over denylists**: Where feasible, validate that input matches an allowed set of characters/patterns rather than checking for the absence of disallowed ones — allowlists are far more resistant to representation-variant bypasses than denylists.
4. **Canonicalize case and whitespace explicitly**: For text-based content filters, case-fold and collapse whitespace as part of normalization, since case and spacing variants are among the simplest bypass techniques.
5. **Adversarial validation testing**: Test validation rules specifically against known encoding-variant, homoglyph, and double-encoding bypass techniques, not just against the literal blocked pattern, as part of routine security review.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_normalization_validation_delta | Rate of inputs that pass validation pre-normalization but would fail if re-checked post-normalization | Alert if > 0 |
| encoding_variant_rejection_rate | Rate of inputs rejected specifically for containing encoded/homoglyph variants of blocked patterns | Informational; track for trend |
| downstream_traversal_or_injection_attempt_count | Count of downstream systems detecting a pattern that upstream validation should have blocked | Alert on any occurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Bypass pattern detected downstream | A downstream system blocks or flags content that passed upstream validation | High | Treat as a validation-bypass incident, patch normalization order, audit for exploitation |
| Validation/normalization order drift | A code change reorders validation relative to decoding/normalization steps | High | Require security review on any change to input-handling pipeline ordering |

## Related Patterns
- [Input Null Bytes Injection](./input-null-bytes-injection.md) - a specific technique for bypassing validation via a byte-level representation mismatch
- [Input Encoding Mismatch](./input-encoding-mismatch.md) - encoding confusion is one concrete mechanism that enables validation bypass
- [Output Sanitization Bypass](./output-sanitization-bypass.md) - the mirror-image failure on the output side, where a sanitizer is defeated by a representation variant rather than a validator
