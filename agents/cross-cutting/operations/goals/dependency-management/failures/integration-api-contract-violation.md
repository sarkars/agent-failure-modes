# Integration API Contract Violation

## Issue
An agent integrates with a third-party or internal service whose documented API contract specifies a particular response shape, status code semantics, or guaranteed behavior, but the service itself violates that contract in practice — returning a documented-as-required field as null, using a success status code for a partial failure, or exceeding its documented rate limits without the promised 429 response. The agent's integration code, written to trust the documented contract, mishandles the actual response because it never anticipated the provider's own inconsistency.

**Frequency**: Common

**Symptoms**
- Parsing code crashes or produces wrong results on a field the API documentation guarantees is always present, but which is empirically absent under certain conditions
- A response has a 200 OK status code but the response body indicates a failure, and code that only checks status codes treats it as success
- The provider's actual behavior differs between its documentation and its real implementation, discovered only through production traffic hitting the undocumented edge case
- Provider support tickets confirm "yes, that's a known inconsistency" for behavior the documentation states differently
- Retrying a call that failed due to a contract violation doesn't help, because the violation is deterministic given the same input, not a transient issue

## Root Cause
API documentation describes the intended contract, but the actual server-side implementation is a separate artifact that can drift from that description through bugs, incomplete edge-case handling, or the documentation simply never being updated after a behavior change — and there is no automated mechanism forcing the two to stay in sync from the consumer's side. Integration code is typically written and tested against the documented contract and against a set of manually observed example responses, both of which represent the "happy path" the documentation describes; the actual violation usually surfaces only for input combinations or account states the integration developer didn't test against, meaning the mismatch is discovered by production traffic rather than integration testing.

## Example
```
An expense-processing agent integrates with a third-party OCR API whose
documentation guarantees every successful response includes a
"confidence_score" field (float, 0.0-1.0) for the extracted text, which the
agent's logic uses to decide whether to auto-approve an expense or route it
to human review (confidence_score < 0.85 triggers review).

The agent's code assumes confidence_score is always present on a 200 OK
response, per the documented contract, and defaults to auto-approve when it
parses successfully with no null check.

For receipts processed via the API's "batch" endpoint (a less-used, less
thoroughly maintained code path on the provider's side), confidence_score is
actually omitted from the response for roughly 3% of documents, a known
inconsistency the provider's own support team later confirms exists only in
the batch endpoint and has existed for over a year without a documentation
update. The agent's null-unsafe comparison (undefined < 0.85 evaluates to
false in the runtime's coercion rules) causes these documents to be treated
as high-confidence and auto-approved without review, silently approving a
small but steady stream of poorly-extracted expense data for months before
a finance audit catches a pattern of malformed line items.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of third-party API integrations encounter at least one documented-contract violation in production within their first year of use | Typical range observed in integration incident reviews |
| Contract violations affecting a minority of traffic (specific endpoints, specific input types) take an estimated 3-6x longer to detect than violations affecting all traffic | Estimated from time-to-detection comparisons by violation scope |
| Integrations with runtime response-shape validation (schema checks on every response, not just at integration-test time) catch an estimated 60-80% of contract violations before they propagate into business logic errors | Reported range across teams using runtime contract validation |

## Mitigations
1. **Runtime response schema validation**: Validate every API response against an explicit schema (required fields, types) at runtime, not just during integration testing, and fail loudly or route to a safe default when the actual response violates the documented contract.
2. **Defensive handling of "guaranteed" fields**: Treat documentation-guaranteed fields as probabilistically present rather than certain, with explicit null/missing-value handling and a conservative default (route to human review, not auto-approve) when a critical field is unexpectedly absent.
3. **Contract-violation monitoring and provider escalation**: Track and alert on schema validation failures against a specific provider, and maintain a paper trail to escalate confirmed contract violations to the provider's support/API team.
4. **Broad, production-representative integration test data**: Test integrations against the full range of real-world input variety (multiple endpoints, edge-case account states, batch vs. single-item paths) rather than only the documentation's example requests.
5. **Fail-safe default direction under uncertainty**: When a contract violation makes an outcome ambiguous, default to the safer/more conservative business action (route to review rather than auto-approve) rather than defaulting to whatever a permissive parser happens to coerce.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| response_schema_validation_failure_rate | Rate of API responses failing schema validation against the documented contract | Alert if > 0.5% for any single provider/endpoint |
| missing_guaranteed_field_rate | Rate at which a documentation-guaranteed field is absent from actual responses | Alert if > 0% |
| status_body_mismatch_rate | Rate of responses where the status code and response body semantics disagree (e.g., 200 with an error body) | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Documented field missing in production | A field the API documentation guarantees is absent in a live response | High | Route affected records to safe-default handling, file provider ticket, add defensive null handling |
| Contract violation concentrated in one endpoint/path | Schema validation failures cluster around a specific endpoint or input type | Medium | Investigate whether the endpoint is less well-maintained by the provider, consider avoiding it |

## Related Patterns
- [Integration Error Handling Mismatch](./integration-error-handling-mismatch.md) - a status/body mismatch is one specific form of the broader inconsistency in how integrated systems signal errors
- [Data Pipeline Schema Drift](./data-pipeline-schema-drift.md) - both involve a producer's actual output diverging from what the consumer was built to expect, one through unannounced change and one through undocumented inconsistency
- [Integration Impedance Mismatch](./integration-impedance-mismatch.md) - a contract violation is a special case of impedance mismatch where the divergence is a provider bug rather than an inherent modeling difference
