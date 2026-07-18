# Time-Based Data Access Not Enforced

## Issue
Access to certain data is supposed to be restricted to a temporal window — only during business hours, only for a fixed number of days after an event (e.g., 30 days after an employee's termination, or 90 days after a transaction for fraud review), or only before a record's scheduled expiration — but the tool that serves the data has no check against the current time relative to that window. The data remains fully queryable indefinitely, or outside the intended hours, because the temporal restriction was defined as a policy rule rather than implemented as a runtime condition on the query path.

**Frequency**: Occasional

**Symptoms**
- An agent retrieves data for a terminated employee, closed case, or expired record well past its intended retention/access window
- Tools that are meant to be usable only during business hours (e.g., for compliance reasons around trading data) return results identically at any hour
- The same query returns different results depending on when it's run relative to a policy-defined window, but nothing in the tool enforces or even signals that boundary to the agent or caller
- Data-retention or access-expiry policy documents specify a time limit that has no corresponding code path checking a timestamp before serving a response
- Time-restricted access violations are discovered during compliance audits by comparing policy documents against actual query logs, not caught by the system itself

## Root Cause
Temporal access restrictions are usually expressed as business or compliance policy ("access to X is limited to Y days") without a corresponding technical mechanism that computes "is now within the permitted window" at query time. Because the underlying data itself doesn't disappear or become invalid at the boundary — it's still sitting in the same table, fully queryable — nothing structurally prevents a tool from serving it unless an explicit time-comparison check was added to the query or response path, and that step is easy to omit since the data "still exists" and looks like any other valid record.

## Example
```
A company's policy states that access to a departed employee's detailed
HR file (compensation history, performance reviews, exit interview
notes) is restricted to 30 days after their termination date, after
which only a minimal record (name, dates of employment) should remain
accessible to general HR-assistant tooling; anything beyond that
requires a separate legal-hold request process.

The HR-assistant agent's "get employee file" tool queries the same
`employees` table regardless of termination date, with no check against
the 30-day policy window. Ninety days after an employee's departure, a
manager asks the assistant, "what was on file for this person before
they left," and the tool returns the full detailed record — compensation
history, performance reviews, and exit notes — exactly as it would have
on day one, because nothing in the query path ever computed how much
time had elapsed since termination or gated the response accordingly.
```

## Statistics
| Finding | Context |
|---------|---------|
| Data-retention and time-limited-access policies are frequently found to lack a corresponding automated enforcement mechanism, relying instead on manual purge or review processes that lag the policy's stated window | Common finding in data-retention compliance audits |
| Business-hours-restricted access controls, where implemented, are more commonly enforced at the network/infrastructure layer (e.g., VPN access windows) than at the individual tool/query layer, leaving application-level tools unrestricted even when infrastructure-level restrictions exist | Typical gap in layered access-control architectures |
| Time-based access violations are disproportionately discovered through periodic compliance audits rather than real-time detection, since the query itself produces no error and the data hasn't been deleted | Common in retention-policy incident reviews |

## Mitigations
1. **Query-time temporal predicate**: Require every tool subject to a time-based access policy to compute the current time against the relevant reference timestamp (event date, termination date, creation date) as part of the query itself, returning a restricted or empty result outside the permitted window rather than the full record.
2. **Automated data tiering at policy boundaries**: When a time window expires, automatically move or transform the data into a restricted-access tier or a minimized record (rather than leaving the full record queryable and relying on the tool to check the clock), so the restriction is enforced by data placement, not just query logic.
3. **Explicit access-window metadata on records**: Store the computed access-expiry timestamp directly on the record (rather than deriving it from a separate event date at query time) so any tool reading the record can check a single, unambiguous field.
4. **Scheduled compliance reconciliation**: Run a recurring job comparing all time-restricted data against current policy windows and flag any tool response path that served data outside its permitted window, even if no complaint was raised.
5. **Time-restricted tool access logging**: Log the computed "within window" determination on every access to time-restricted data, so audits can verify enforcement occurred rather than inferring it from the absence of complaints.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `out_of_window_access_count` | Count of tool responses serving time-restricted data outside its permitted access window | Alert threshold: > 0 (any occurrence) |
| `missing_temporal_predicate_count` | Count of tools/queries subject to a time-based policy with no runtime time-window check | Alert threshold: > 0 for any policy-covered dataset |
| `expired_record_tier_migration_lag` | Time elapsed between a record's policy window expiring and its migration to a restricted/minimized tier | Alert threshold: > defined SLA (e.g., 24 hours) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Time-Restricted Data Served Out of Window | A tool response includes data outside its policy-defined access window | P2 | Patch the missing temporal check, review recent access logs for the extent of the gap |
| Tiering Migration Overdue | A record's policy window has expired but it hasn't yet been migrated to the restricted tier | P3 | Investigate the tiering job, expedite migration |

## Related Patterns
- [Geographic Data Access Restriction](./geographic-data-access-restriction.md) - both involve a compliance-driven access dimension treated as policy metadata rather than a runtime gate
- [Data Classification Access Not Enforced](./data-classification-access-not-enforced.md) - shares the pattern of a policy label existing without a corresponding enforcement mechanism
- [Record Ownership Not Validated](./record-ownership-not-validated.md) - both illustrate access checks that exist in intent but aren't wired into the actual query/write path
