# Tool Cost Override Incident

## Issue
During an incident (an outage, a launch under time pressure, a data-quality emergency), an engineer or on-call responder manually raises or disables a tool's cost cap to let the agent push through urgent work unblocked. The override is applied directly in configuration or a feature flag, the incident is resolved, and the override is never reverted — because reverting it isn't part of the incident-closure checklist and no automated expiry was attached to the change. The cap stays effectively uncapped indefinitely, sometimes for months, until an unrelated invoice review discovers it.

**Frequency**: Common

**Symptoms**
- A tool's configured budget cap is dramatically higher than its documented/approved value, with no corresponding change-management record explaining the increase
- The override's origin traces back to an incident ticket that was closed weeks or months earlier
- Cost for the overridden tool has been running above the originally-approved budget for an extended period without triggering any alert, because the alert threshold was raised along with the cap
- No expiry date, ticket reference, or removal task is attached to the override in configuration
- The person who applied the override is no longer actively working on the system that owns it, so nobody notices it's still active

## Root Cause
Incident response is optimized for speed of mitigation, and cost-cap overrides are usually a one-line configuration change or flag flip that's easy to apply under pressure but has no corresponding automatic expiry or revert step built into standard incident tooling. Incident postmortem and closure processes typically focus on the technical root cause and prevention of recurrence, not on auditing every configuration change made during the incident, so a cap override that "worked" and caused no immediate visible problem is simply forgotten rather than explicitly reverted.

## Example
```
During a data pipeline outage, an on-call engineer discovers the recovery
agent is blocked by the $100/day cap on "ValidationAPI" while reprocessing
a backlog of 50,000 records. To unblock the recovery, they edit the
config to raise the cap to $5,000/day and restart the service, noting
"temp bump for incident INC-4821, revert after backlog clears" in the
commit message but not in any tracked follow-up task.

The backlog clears within 36 hours and the incident is closed. The
$5,000/day cap is never reverted — it wasn't a listed action item in the
incident retro, and the config change blends into the codebase's normal
history.

Four months later, ValidationAPI usage has organically grown (unrelated
to the original incident) and is now regularly hitting $1,800-2,200/day,
more than an order of magnitude above the originally-approved $100/day
budget, with no alerts firing because the alert threshold was raised
alongside the cap. Finance flags the tool during a routine vendor spend
review, and it takes a config-history archaeology exercise to determine
the $5,000 cap traces back to an incident resolved four months prior.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of emergency configuration overrides applied during incidents are never explicitly reverted, persisting until discovered incidentally | Frequently observed pattern in incident postmortem audits |
| Time-to-discovery for un-reverted cost overrides is commonly measured in months, typically surfaced by finance/billing review rather than engineering monitoring | Typical range absent automated expiry |
| Overridden budget caps are often set 10-50x above the original approved value to comfortably clear the immediate incident, rather than the minimum needed | Common pattern under incident time pressure |

## Mitigations
1. **Mandatory expiry on overrides**: Require every emergency cap override to include an automatic expiry (time-boxed flag, TTL on the config value) that reverts to the prior value unless explicitly renewed, rather than persisting indefinitely by default.
2. **Incident closure checklist includes config audit**: Add a standard incident-closure step that lists every configuration change made during the incident (including cost caps) and requires explicit sign-off to keep or revert each one.
3. **Override tracking as first-class records**: Log cost-cap overrides in a dedicated, queryable registry (not just a commit message or chat mention) with incident reference, approver, original value, and planned revert date.
4. **Periodic override audit**: Run a recurring (e.g. monthly) automated scan comparing all active budget caps against their originally-approved baseline values, flagging any that differ without an active, non-expired justification.
5. **Alert threshold decoupled from cap**: Keep cost alerting thresholds tied to the originally-approved budget baseline even when the enforcement cap itself is temporarily raised, so overspend relative to the real intended budget still surfaces during the override window.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| active_overrides_past_expiry | Count of cost-cap overrides still active past their intended revert date | Alert if > 0 |
| cap_vs_approved_baseline_delta | Difference between a tool's currently configured cap and its documented approved baseline | Alert if delta > 20% and unexplained by an active, tracked override |
| override_age | Time elapsed since an override was applied without being reverted or renewed | Alert if > 14 days |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Untracked cap deviation | A tool's active cap differs from its approved baseline with no matching entry in the override registry | High | Freeze the cap at current value pending review, identify origin via config history |
| Override past expiry | An override's TTL has lapsed without renewal | Medium | Automatically revert to baseline cap, notify the original requester and team |

## Related Patterns
- [Per-Tool Monthly Budget Overrun](./per-tool-monthly-budget-overrun.md) - un-reverted overrides are a common root cause of overruns that persist across multiple billing cycles
- [Cross-Tool Total Budget Exceeded](./cross-tool-total-budget-exceeded.md) - a forgotten override on one tool compounds aggregate visibility gaps across the whole budget picture
- [Budget Priority Misalignment](./budget-priority-misalignment.md) - overrides applied under incident pressure often bypass whatever priority scheme normally governs spend
