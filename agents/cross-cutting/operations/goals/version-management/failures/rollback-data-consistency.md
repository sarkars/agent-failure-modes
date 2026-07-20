# Rollback Data Consistency

## Issue
An agent platform rolls back its application code to a prior version after a bad release, but the data the new version wrote during the time it was live — new conversation-state fields, a changed tool-call log schema, session records referencing a memory format the old code doesn't understand — is not rolled back along with it. The old code comes back up and immediately encounters data shapes it was never written to handle, either crashing on deserialization, silently dropping fields it doesn't recognize, or misinterpreting a repurposed field, producing corrupted or nonsensical agent behavior that looks like a new bug rather than the direct consequence of the rollback itself.

**Frequency**: Common

**Symptoms**
- Immediately after a rollback, error rates spike again but with different error signatures than the original incident being rolled back from
- Deserialization or schema-validation errors referencing fields the rolled-back code doesn't recognize
- Conversation or session state appears truncated, defaulted, or corrupted specifically for sessions that were active during the rolled-forward version's window
- The rollback is declared successful based on code-level health checks while data-level anomalies keep surfacing for hours afterward
- Session records written by the newer version silently lose the fields only that version understood, once the old code re-saves them

## Root Cause
Code rollbacks are fast and mechanically simple — redeploy the previous artifact — which creates an illusion that the whole system has returned to its prior state. But persistent data (databases, caches, session stores, message queues) is not versioned alongside code and does not roll back with it; any writes made by the newer version stay in place unless a separate, explicit data-remediation step is taken. When the newer version's schema change was forward-only (additive fields the old code ignores are usually safe, but renamed/removed/repurposed fields or new required invariants are not), the old code re-encountering that data behaves however its un-updated logic happens to handle unfamiliar input — which is rarely "gracefully," because it was never designed to. The team doing the rollback is usually reacting to an active incident and focused on restoring code health, and data-shape backward-compatibility is easy to overlook under that pressure, especially because it doesn't fail immediately or visibly the way a crash-on-startup error would.

## Example
```
"MemoryAgent" v18 introduces a change to how long-term memory
summaries are stored: the old "summary_text" string field is
replaced with a structured "summary_blocks" array (list of
{topic, content} objects), written by a migration-on-write pattern -
whenever v18 touches a session, it converts and saves the record in
the new shape rather than a bulk migration up front.

v18 ships, runs for 5 hours, converts roughly 40% of active sessions'
memory records to the new summary_blocks format as those sessions
get touched.

An unrelated regression in v18 (a tool-call timeout bug) triggers an
incident. On-call rolls back to v17 to stop the timeout errors.
v17's code only knows how to read summary_text and has no handling
for summary_blocks - it either treats the field as absent (memory
appears empty for those 40% of sessions) or, in a few code paths,
throws a deserialization error that surfaces as a 500 on session
load.

Users whose sessions were touched during the v18 window suddenly
"forget" earlier conversation context after the rollback, and this
gets reported as a fresh, unrelated bug rather than recognized as a
direct consequence of rolling back code without rolling back (or
migrating forward) the data it had already written.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of rollback incidents are followed by a second, distinct incident traced to data written by the rolled-back-from version | Typical pattern reported in post-incident reviews covering rollback events |
| Additive-only schema changes are substantially less likely to cause post-rollback data issues than renamed, removed, or repurposed fields | Estimated from comparing incident rates across schema-change types |
| Testing rollback against realistic data written by the newer version (not just testing the rollback deploy mechanics) catches most of these issues before production | Reported range across teams that added rollback-compatibility testing to their release checklist |

## Mitigations
1. **Backward-compatible-by-default schema changes**: Default to additive, non-destructive schema changes (new optional fields, dual-write during a transition period) so that a code rollback naturally leaves data the old version can still read, even if it ignores the newer fields.
2. **Rollback compatibility testing**: As part of release testing, explicitly test the rollback path against data written by the new version, not just the forward deployment, to catch backward-incompatibility before it happens under incident pressure.
3. **Data versioning alongside code versioning**: Tag persisted records with a schema version, and have both old and new code paths explicitly branch on that version rather than assuming a single implicit shape, so old code degrades predictably instead of failing on unfamiliar structure.
4. **Rollback runbook includes data remediation step**: Make data-compatibility assessment an explicit, named step in every rollback runbook — not an afterthought — including a decision on whether a remediation script is needed before or immediately after the code rollback.
5. **Post-rollback data anomaly monitoring**: After any rollback, specifically watch for schema-validation errors, unexpected null/default fields, and deserialization failures in the following hours, since these often appear later and look unrelated to the rollback itself.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_rollback_deserialization_error_rate | Rate of schema/deserialization errors in the hours following a rollback | Alert if > 0.1% of session loads within 6 hours post-rollback |
| unexpected_field_default_rate | Rate at which fields load as null/default when they should have data, correlated with post-rollback windows | Alert if elevated versus pre-incident baseline |
| affected_session_count_post_rollback | Count of sessions touched by the rolled-back-from version, tracked as an at-risk population | Informational, surfaced automatically on every rollback |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Post-rollback data errors detected | post_rollback_deserialization_error_rate exceeds threshold following a rollback | High | Identify affected sessions, assess need for a forward-fix or data remediation script, do not assume rollback alone resolved the incident |
| Silent data loss suspected | unexpected_field_default_rate spikes for sessions touched during the rolled-back-from version's active window | High | Audit a sample of affected records, determine scope, communicate to affected users if data loss is confirmed |

## Related Patterns
- [Rollback Partial Failure](./rollback-partial-failure.md) - both concern rollback leaving the system in a worse or inconsistent state than either the old or new version alone
- [Deployment Ordering Violation](./deployment-ordering-violation.md) - shares the root theme of code and data changes being coupled but managed by disconnected processes
- [Version Downgrade Failure](./version-downgrade-failure.md) - the forward-only-migration variant of this same underlying problem, where the downgrade path itself is technically blocked rather than just producing bad behavior
