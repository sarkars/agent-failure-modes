# PII Field Leakage In Responses

## Issue
PII is correctly scrubbed or redacted from a tool's primary, well-tested response path, but leaks through a secondary channel the same tool call touches — an error message that echoes back invalid input, a stack trace surfaced when a downstream call fails, a nested or joined object included for context that wasn't covered by the redaction filter, or a debug/verbose field left enabled in production. The agent then reads that secondary channel as part of its normal error-handling or context-gathering behavior and surfaces the leaked PII to the user, having no way to know it wasn't supposed to be there.

**Frequency**: Common

**Symptoms**
- Redaction works correctly on the "happy path" response but not on error/exception responses from the same tool
- PII surfaces in the agent's answer only when a lookup partially fails or returns an unexpected shape, not on normal successful calls
- Nested objects returned as part of a join (e.g., an "order" response that embeds a full unredacted "customer" object for internal reference) bypass the top-level redaction filter, which only inspects top-level fields
- Debug or verbose-logging fields, meant to be stripped before reaching production, appear intermittently when a feature flag or environment config drifts
- Security review of the "clean" response path passes, but a fuzzing/error-injection test reveals PII in edge-case responses

## Root Cause
Redaction and scrubbing logic is typically written and tested against the tool's expected, successful response shape, because that's the path exercised by normal QA and integration tests. Error paths, nested/joined objects, and debug output are structurally different response shapes that the same redaction filter either doesn't run against at all (if it's applied only to the primary payload) or doesn't recurse into (if it only inspects top-level fields), so PII embedded in those secondary shapes passes through unfiltered even though the primary path is fully compliant.

## Example
```
A billing tool redacts customer email and phone from its standard
"get invoice" response before returning it to a customer-support agent.
The redaction filter is implemented as a top-level field stripper: it
removes `customer.email` and `customer.phone` from the JSON response's
top-level `customer` object.

When an invoice lookup fails because the invoice was voided, the
billing service returns an error object that includes a `context` field
for debugging, containing the full original request payload — which
includes the customer's email and phone number as submitted, embedded
one level deeper than the redaction filter inspects. The support agent,
handling the failure gracefully, includes the error context in its
explanation to the user ("I see there was an issue processing invoice
INV-4471 for jane.doe@example.com..."), surfacing the customer's email
even though the exact same tool, on a successful call, would never have
revealed it.
```

## Statistics
| Finding | Context |
|---------|---------|
| Error-path and exception-response PII leaks are a recurring category in application security audits, distinct from and often missed by tests focused on the primary success path | Common in penetration test findings across API-backed services |
| Redaction filters that only inspect top-level response fields miss a meaningful share of PII embedded in nested or joined objects | Typical limitation of naive field-stripping implementations |
| Debug/verbose output left enabled due to configuration drift is a recurring root cause of PII appearing in production responses that passed initial security review | Common in configuration-drift incident postmortems |

## Mitigations
1. **Recursive, schema-agnostic redaction**: Implement PII scrubbing as a recursive pass over the entire response object — including nested, joined, and error payloads — rather than a shallow filter over expected top-level fields.
2. **Error-path redaction parity testing**: Explicitly test error and exception response paths for PII leakage with the same rigor as the success path, including fuzzed and malformed inputs designed to trigger unusual error shapes.
3. **Pattern-based secondary scrubbing**: Layer a pattern-matching redaction pass (regex or classifier-based detection of email, phone, SSN patterns) over all outbound tool responses as a backstop, independent of the field-based redaction logic, to catch PII in shapes the field-based filter wasn't designed for.
4. **Debug output hard-disabled in production**: Gate verbose/debug fields behind a build-time flag rather than a runtime config flag, so configuration drift can't accidentally re-enable them in a live environment.
5. **Agent-side leak detection before surfacing**: Have the agent runtime scan tool-call outputs for PII patterns before including them in a user-facing response, flagging or stripping matches even if the upstream tool failed to redact them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `error_path_pii_leak_count` | Count of error/exception responses containing an unredacted PII pattern | Alert threshold: > 0 (any occurrence) |
| `nested_object_pii_leak_count` | Count of responses where PII is found in a nested/joined object not covered by the top-level redaction filter | Alert threshold: > 0 (any occurrence) |
| `agent_surfaced_leaked_pii_count` | Count of confirmed cases where a tool-level PII leak was subsequently surfaced in an agent's user-facing response | Alert threshold: > 0 (any occurrence) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| PII in Error Response | Pattern-based scan detects PII in a tool's error/exception output | P1 | Patch the redaction filter to cover the error path, review recent logs for exposure |
| Agent Surfaced Leaked PII | Agent-side leak detection confirms unredacted PII reached a user-facing response | P1 | Notify security/privacy immediately, assess notification obligations, patch the leak source |

## Related Patterns
- [PII Field Exposure](./pii-field-exposure.md) - a related but distinct failure where PII is present in the primary response by design rather than leaking through a secondary channel
- [Masked Field Unmasking](./masked-field-unmasking.md) - both involve a control that works on the primary path but fails on an alternate access pattern
- [Sensitive Field Access Not Restricted](./sensitive-field-access-not-restricted.md) - overlaps when the leaked secondary-channel data is also a flagged sensitive field
