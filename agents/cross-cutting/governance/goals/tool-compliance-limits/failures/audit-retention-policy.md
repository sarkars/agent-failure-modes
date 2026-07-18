# Audit Retention Policy

## Issue
Regulatory or internal policy requires audit logs of agent tool activity to be retained for a defined period (e.g. seven years for financial records, a shorter window for other categories), but the actual log storage system rotates, compresses-and-discards, or hard-deletes entries on a default retention schedule that's shorter than policy requires — often because the logging infrastructure's default retention setting was never explicitly reconfigured to match the compliance requirement.

**Frequency**: Common

**Symptoms**
- The logging platform's default retention window (commonly 30, 90, or 180 days) is still in effect for a data category with a multi-year compliance requirement
- Different tool categories with different required retention periods are all stored in one log stream with a single, uniform retention setting
- No automated check compares actual configured retention against the compliance policy document
- A request for historical audit records (from a regulator, auditor, or legal hold) turns up nothing beyond the platform's default window
- Retention configuration lives in infrastructure-as-code that was set once at initial deployment and never revisited as compliance requirements were formalized or changed

## Root Cause
Log retention is an infrastructure configuration setting (a bucket lifecycle rule, a log-platform retention policy, a database partition-drop schedule) that is typically set once, based on cost or platform defaults, without a direct, maintained link to the compliance policy document that actually specifies the required retention period. Because the two live in different systems — one in a policy wiki, the other in infrastructure config — they drift apart silently: nothing breaks when the config's retention window is shorter than policy requires, until someone specifically needs a record that's already gone.

## Example
```
1. Financial-services compliance policy requires that audit records of any tool call affecting customer
   account balances be retained for seven years.
2. The audit logs for the agent's balance-adjustment tool are shipped to a centralized logging platform
   that was configured, at initial setup, with the platform's default 90-day retention to control storage
   costs -- a setting made by an infrastructure engineer unaware of the seven-year requirement.
3. No process exists to compare configured retention windows against the compliance policy document, so
   the mismatch is never caught during normal operation.
4. Three years later, a regulatory inquiry requests audit records for a customer account adjustment made
   two years prior.
5. The records no longer exist; they were deleted by the logging platform's 90-day retention rule long
   before the seven-year requirement's window closed, leaving the organization unable to produce evidence
   it is required to retain.
```

## Statistics
| Finding | Context |
|---------|---------|
| Logging platform default retention windows are commonly shorter than the compliance retention period required for regulated data categories | Common finding in compliance-readiness audits |
| Retention misconfiguration is disproportionately discovered only when a specific historical record is requested, rather than through proactive audit | Typical pattern in compliance incident review |
| Automated, policy-linked retention configuration with alerting on drift closes most of these gaps before evidence is lost | Standard remediation for retention-policy findings |

## Mitigations
1. **Map every log category to its compliance-required retention period explicitly**: Maintain a single source of truth linking each tool/data category to its required minimum retention, and derive infrastructure retention settings from it rather than platform defaults.
2. **Use the longest applicable retention period as the default floor**: Where a single log stream mixes categories with different requirements, either split streams by category or set retention to the maximum required across all categories present.
3. **Automate drift detection between policy and configuration**: Run a scheduled job comparing each log store's actual configured retention against the compliance policy mapping, and alert on any mismatch.
4. **Apply legal-hold overrides independent of standard retention**: Build a mechanism to place specific records or time windows under an extended hold that overrides the normal deletion schedule when litigation or investigation requires it.
5. **Review retention settings whenever compliance requirements change**: Treat retention policy documents as a trigger for an infrastructure-config review, not a one-way document that infrastructure config is assumed to already satisfy.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| retention_policy_drift_count | Log categories whose configured retention is shorter than their documented compliance requirement | > 0 |
| logs_deleted_before_required_window | Count of log entries deleted before their category's required retention period elapsed | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Retention below compliance requirement | Automated audit finds a log category's configured retention shorter than policy requires | Critical | Correct the retention setting immediately, assess whether any records were already lost, notify compliance |
| Legal hold conflicts with default deletion | A record under active legal hold is scheduled for deletion by the standard retention job | Critical | Block the deletion, escalate to legal/compliance immediately |

## Related Patterns
- [Audit Logging Not Enforced](./audit-logging-not-enforced.md) - complementary failure: even correctly-retained logs are useless for compliance if the entries were never written in the first place
- [Audit Log Tampering](./audit-log-tampering.md) - both result in audit evidence being unavailable when needed, through deletion versus alteration
- [PII Retention Policy Violation](./pii-retention-policy-violation.md) - the same retention-drift root cause applies to PII data stores, not just audit logs
