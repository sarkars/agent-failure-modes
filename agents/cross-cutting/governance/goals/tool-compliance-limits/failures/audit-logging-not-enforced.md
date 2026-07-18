# Audit Logging Not Enforced

## Issue
Policy requires that certain tool calls — anything that reads sensitive data, anything that mutates state, anything crossing a compliance boundary — be recorded in an audit log. In practice, the logging call is implemented as a best-effort side effect inside each tool handler (or worse, left to individual developers to remember to add), rather than as a mandatory step enforced at the tool-dispatch boundary. When the logging call fails, times out, is skipped by an exception path, or is simply never added to a new tool, the action still executes and no record is created.

**Frequency**: Very Common

**Symptoms**
- Some tool handlers call `log_audit_event()` and others, added later or by a different engineer, don't
- Logging calls are placed after the action executes, so an exception during logging doesn't roll back or flag the action, it just silently loses the record
- New tools ship without corresponding audit-log integration because there's no CI or review gate requiring it
- Reconciliation between "actions taken" (from downstream system state) and "actions logged" (from the audit store) reveals more of the former than the latter
- Logging is implemented as a fire-and-forget async call with no monitoring of delivery success

## Root Cause
Audit logging is usually treated as an application-level concern bolted onto individual tool implementations rather than a cross-cutting requirement enforced by the framework that dispatches tool calls. Because there's no single choke point through which every tool call must pass a mandatory "log or refuse to execute" check, coverage depends entirely on every engineer remembering to add logging to every new or modified tool — a maintenance burden that reliably degrades over time, especially under deadline pressure or during refactors.

## Example
```
1. Compliance policy requires that every tool call reading customer PII be logged with the calling
   agent's identity, the fields accessed, and a timestamp, to support future data-subject access request
   audits.
2. The original PII-reading tool, get_customer_profile, was built with audit logging correctly wired in.
3. Six months later, a new tool, get_customer_billing_history, is added by a different team to support a
   new agent workflow. It also reads PII (billing address, payment method last-4) but the engineer who
   built it wasn't aware of the audit-logging requirement, and no CI check caught the omission.
4. For months, every call to get_customer_billing_history executes and returns PII with zero audit trail.
5. A compliance audit later asks for a complete record of PII access for a specific customer; the gap for
   billing-history access cannot be reconstructed, and the organization cannot demonstrate compliance for
   that data category.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of new tools added to an existing agent platform ship without the audit-logging coverage required by policy, absent an enforced gate | Common finding in agent platform compliance reviews |
| Reconciliation between downstream action counts and audit-log entry counts frequently reveals meaningful gaps in coverage | Typical finding when compliance teams run first-time audit-log completeness checks |
| Moving the logging call to a mandatory dispatch-layer wrapper, rather than per-tool implementation, closes the majority of these coverage gaps | Standard remediation for logging-coverage findings |

## Mitigations
1. **Enforce logging at the tool-dispatch layer, not inside individual handlers**: Wrap all tool execution in a single dispatcher that writes an audit entry before/after every call, so no tool can execute without a corresponding log entry regardless of whether its author remembered to add one.
2. **Fail closed on logging failure for sensitive operations**: If the audit-log write fails or times out for a tool tagged as requiring logging, block or roll back the action rather than letting it proceed silently.
3. **Add a CI gate requiring audit-log coverage metadata on new tools**: Require every tool registration to declare its audit-logging category, and fail the build if a tool touching a sensitive data category has no logging wired in.
4. **Run periodic reconciliation between actions taken and actions logged**: Compare downstream system state changes (or read-access counts) against audit-log entries on a recurring schedule to surface coverage gaps.
5. **Make logging synchronous and acknowledged for high-sensitivity tools**: For the highest-risk categories (PII access, financial mutation), require the log write to be confirmed before the tool call is considered complete, rather than fire-and-forget async logging.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unlogged_sensitive_tool_calls | Sensitive-tagged tool calls with no corresponding audit-log entry | > 0 per day |
| audit_log_coverage_ratio | Ratio of audit-log entries to actual tool executions for logging-required tools | < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Logging gap detected for sensitive tool | Reconciliation job finds an executed sensitive-tagged action with no matching log entry | High | Investigate the gap, patch the tool's dispatch path, backfill context from other sources if possible |
| New tool deployed without logging metadata | CI detects a tool lacking an audit-logging category declaration | Warning | Block merge until logging metadata and coverage are added |

## Related Patterns
- [Audit Log Tampering](./audit-log-tampering.md) - both undermine audit trail reliability, one by preventing entries, the other by altering them after creation
- [Audit Retention Policy](./audit-retention-policy.md) - even fully-logged actions are useless for compliance if the resulting log is deleted before the required retention period
- [PII Retention Policy Violation](./pii-retention-policy-violation.md) - unlogged PII access compounds the risk of undetected data-handling violations going unnoticed
