# Input Schema Evolution

## Issue
An upstream system that feeds an agent changes its data schema — renaming a field, changing a type, adding a required field, deprecating an enum value — without a coordinated update to the agent's input parser, so the agent either silently misreads the new shape (treating a renamed field as missing and falling back to a default) or crashes on fields it no longer recognizes. Because the agent's own code didn't change, the failure looks like a regression with no corresponding commit, making it unusually hard to diagnose.

**Frequency**: Common

**Symptoms**
- Fields that were reliably populated suddenly start showing as missing/null in agent output, with no change in the agent's own code
- Parsing errors or type-mismatch exceptions appear that correlate exactly with an upstream deployment, not an agent deployment
- New enum values from an upstream system fall through the agent's `switch`/`match` logic into an unhandled default branch
- Agent behavior changes silently in production with no corresponding pull request in the agent's own repository
- Postmortem timeline shows the actual root-cause commit lives in a different team's/service's repository

## Root Cause
Agents that consume structured input from another system are implicitly coupled to that system's schema, but the coupling is rarely enforced by any contract that both sides are obligated to honor together. Upstream teams version and deploy their own services independently, and unless there's a shared schema registry, consumer-driven contract tests, or a deprecation/notification process, a schema change ships the moment it passes the upstream team's own tests — which say nothing about downstream consumers they don't know exist. The agent's parser, written against a snapshot of the schema at integration time, has no mechanism to detect that the contract underneath it has shifted, so it either silently misinterprets the new shape (if the change is structurally compatible but semantically different) or throws an unhandled error (if it isn't).

## Example
```
A claims-processing agent parses claim submissions from an insurance
partner's API, reading a field "claim_status" with expected values
"open", "closed", "pending".

The partner deploys a schema update adding a new status, "under_review",
to better reflect a new internal workflow stage. From the partner's
perspective this is a backward-compatible additive change -- existing
consumers should just ignore values they don't recognize.

The agent's status-handling logic is:

    if status == "open": route_to_adjuster()
    elif status == "closed": archive()
    elif status == "pending": queue_for_review()
    else: raise UnhandledStatusError(status)

Every claim newly submitted with "under_review" now throws an unhandled
exception, and because the agent's retry logic re-queues failed claims,
these claims pile up in a dead-letter queue. Nobody notices for four days
because the agent's own error rate dashboard groups all exceptions under
one generic "processing_error" bucket, and the actual cause -- a schema
change in a partner system three teams away -- isn't discovered until
someone manually inspects the dead-letter payloads.
```

## Statistics
| Finding | Context |
|---------|---------|
| A substantial share of "no code change" production incidents in agents consuming external APIs trace back to an upstream schema change | Typical range observed in cross-team incident postmortems |
| Additive/backward-compatible-by-the-producer's-definition changes (new enum values, new optional fields) account for the majority of these incidents, not breaking removals | Common pattern in schema-evolution incident analysis |
| Consumer-driven contract testing catches a large majority of schema-evolution incidents before they reach production | Reported range across teams using contract-testing frameworks |

## Mitigations
1. **Consumer-driven contract testing**: Maintain automated contract tests that assert the agent's expectations about the upstream schema, run against the upstream service's actual staging/CI environment, so a breaking or semantically significant change fails a test before it ships.
2. **Explicit unknown-value handling**: Treat unrecognized enum values, unexpected new fields, and type mismatches as a distinct "unknown, needs review" branch rather than either crashing or silently falling into a default — surfacing new schema shapes instead of hiding or breaking on them.
3. **Schema version pinning and negotiation**: Where the upstream system supports it, pin to and request a specific schema version, and treat a version bump as a signal requiring explicit agent-side review rather than silent pass-through.
4. **Shared schema registry**: Use a shared schema registry (e.g. for event/message-based integrations) so schema changes are visible and diffable across producer and consumer teams before deployment.
5. **Upstream change notification process**: Establish a lightweight process (changelog, deprecation window, notification channel) so upstream teams know downstream agent consumers exist and are expected to flag schema changes before shipping them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unrecognized_field_value_rate | Share of parsed records containing a field value not in the agent's known set | Alert if > 0.5% sustained |
| dead_letter_queue_growth_rate | Rate of records failing processing and landing in a dead-letter/retry queue | Alert on sustained upward trend |
| schema_drift_detection_count | Count of contract-test failures against upstream staging/CI | Alert on any failure |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unhandled schema value in production | An unrecognized enum value or unexpected field shape reaches production parsing logic | High | Route to unknown-value queue instead of failing, notify upstream team, patch handling |
| Contract test failure against upstream | A consumer-driven contract test fails against the upstream service's current staging build | High | Block upstream deployment or coordinate a synchronized release with the agent's parser update |

## Related Patterns
- [Input Default Value Assumption](./input-default-value-assumption.md) - a renamed or restructured field is a common trigger for the agent falling back to an incorrect default
- [Input Validation Bypass](./input-validation-bypass.md) - a schema change can inadvertently open a gap that a previously-enforced validation rule no longer covers
- [Output Format Not Validated](./output-format-not-validated.md) - the mirror-image failure, where the agent's own output schema drifts without downstream consumers being updated
