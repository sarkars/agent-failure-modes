# Error Code Semantic Drift

## Issue
A tool vendor changes what an existing error code means — repurposing a generic `400 Bad Request` to also signal a new condition like "rate limited by a downstream partner" or reusing `409 Conflict` for a newly introduced idempotency-key collision case — without incrementing the API version or announcing a breaking change. The agent's error-handling logic, written against the old, narrower meaning of that code, applies the wrong recovery strategy (e.g. retrying a request that will never succeed, or treating a transient condition as permanent), and because the HTTP status and error code string are unchanged, nothing about the failure looks abnormal at the transport level.

**Frequency**: Occasional

**Symptoms**
- A specific error code's observed cause changes over time even though the agent's handling logic for that code hasn't changed
- Retry logic keeps retrying an error that used to be transient but is now permanent (or vice versa), producing either wasted retries or premature give-ups
- Error handling that was correct for months suddenly starts producing wrong outcomes with no corresponding change on the agent's side
- The vendor's changelog, if it exists, doesn't list the error-code reinterpretation as a breaking change, or the change shipped without a changelog entry at all
- Support tickets to the vendor reveal the error code is now documented differently than when the integration was built, but no version or endpoint change accompanied it

## Root Cause
HTTP status codes and generic error identifiers (`400`, `409`, `invalid_request`) are coarse-grained by design, and vendors often expand what condition maps to an existing code rather than minting a new one, because adding a new code is a more visible, deliberate API change that goes through review, while reusing an existing code for a new internal condition can ship as an implementation detail on the vendor's side. Agent error-handling logic that pattern-matches on the code alone (rather than on more specific fields like an error subtype or message content) has no way to distinguish the old meaning from the new one, since the code itself hasn't changed.

## Example
```
An agent integrates "PaymentsGatewayAPI" and treats HTTP 409 Conflict as
"duplicate transaction — safe to treat as already-succeeded and stop
retrying," which matches the documented behavior at integration time.

Eight months later, PaymentsGatewayAPI's team adds a new fraud-hold
feature and, rather than introducing a new status code, repurposes 409
to also cover "transaction held for manual fraud review — retry later
once cleared." This ships as a minor backend change with no version bump
and a one-line mention in an internal vendor release note the integrating
team never sees.

The agent now receives 409 responses for both duplicate transactions and
fraud holds, indistinguishable at the status-code level. Its existing
logic treats every 409 as "already succeeded, stop retrying," so
transactions that are actually held for fraud review are marked complete
and the customer never receives the retry that would have cleared the
hold — until a customer complaint traces the missing charge back to a
transaction the agent had silently marked done.
```

## Statistics
| Finding | Context |
|---------|---------|
| Vendor API changes that repurpose or expand the meaning of an existing error/status code without a version bump are a common source of silent breaking changes in third-party integrations | Frequently cited pattern in API-integration incident reviews |
| Error-handling logic keyed only on HTTP status code (rather than a more specific error subtype field) is common in agent tool wrappers built for rapid integration | Common implementation pattern |
| Detection of semantic drift in error codes typically happens via a downstream business-outcome anomaly (wrong customer-facing result) rather than via the error-handling code itself flagging anything unusual | Typical detection pattern |

## Mitigations
1. **Key on the most specific error field available**: Parse and branch on structured error subtype/reason fields (e.g. `error.type`, `error.code` in the JSON body) rather than the HTTP status code alone, since vendors are less likely to repurpose a specific documented subtype than a generic status code.
2. **Vendor changelog and API-version monitoring**: Subscribe to the vendor's changelog, status page, or API version announcements, and route any error-handling-relevant change through a review before it can silently affect production behavior.
3. **Outcome-based sanity checks**: Add downstream assertions that validate the *business* outcome implied by an error-handling decision (e.g. confirm a transaction marked "duplicate, already succeeded" actually appears as succeeded in a reconciliation feed) rather than trusting the classification alone.
4. **Contract/schema testing against the live vendor sandbox**: Periodically run integration tests against the vendor's sandbox or staging environment that specifically probe known error conditions, to catch cases where the returned code or its associated payload has changed shape or meaning.
5. **Fail toward manual review on ambiguous codes**: For error codes whose meaning materially changes agent behavior (stop vs. retry vs. escalate), default to routing to human review when confidence in the classification is uncertain, rather than assuming the historical meaning still holds indefinitely.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| error_code_outcome_distribution_shift | Change in the distribution of downstream outcomes following a given error code, compared to historical baseline | Alert if distribution shifts > 20% week-over-week |
| unhandled_error_subtype_rate | Rate of responses containing an error subtype/reason value not recognized by current handling logic | Alert if > 0.5% of error responses |
| retry_success_rate_by_code | Success rate of retries following a specific error code | Alert on a sudden drop for a code previously considered reliably transient |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Outcome distribution shift for known code | error_code_outcome_distribution_shift exceeds threshold for a code with established handling logic | High | Freeze automated handling for that code, route to manual review, contact vendor support |
| Unrecognized error subtype observed | An error response contains a subtype/reason value not in the agent's known mapping | Medium | Log full payload for review, do not silently default to prior behavior |

## Related Patterns
- [Error Response Format Inconsistency](./error-response-format-inconsistency.md) - both involve the agent's error parser making assumptions about vendor error shape that silently stop holding
