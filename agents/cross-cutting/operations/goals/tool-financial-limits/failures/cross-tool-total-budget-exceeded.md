# Cross-Tool Total Budget Exceeded

## Issue
An agent has separate, independently-tracked budget caps for each tool it uses — say $10/day for a search API, $15/day for an enrichment API, and $25/day for an LLM-based summarization tool — and each individual cap is respected. But no component tracks the sum across tools, so the agent can legitimately spend up to $50/day per user session while whoever set the budgets believed they were capping total spend at, say, $20/day. The org discovers the real number only when the consolidated vendor invoice arrives.

**Frequency**: Very Common

**Symptoms**
- Each individual tool's dashboard shows "within budget" while the combined bill is far above what finance expects
- No single metric or dashboard shows aggregate spend across all tools for a given agent, task, or user
- Finance/billing surprises originate from combinatorial use (agent calling 3-4 tools per task) rather than any one tool being abused
- Budget alerts fire per-tool but never at the workflow or account level
- Retroactively reconstructing "how much did this agent cost in total" requires manually summing multiple vendor invoices

## Root Cause
Budget controls are typically implemented at the point of integration — each tool connector or SDK wrapper enforces its own spend ceiling because that's where the cost data (API responses, per-call pricing) is naturally available. Building an aggregate view requires a cross-cutting accounting layer that observes every tool call regardless of which tool it targets, which is architecturally a separate concern from the connectors themselves and is frequently never built, especially as tools are added incrementally over time by different teams.

## Example
```
A support-automation agent uses three billed tools per ticket: "LookupAPI"
($0.02/call, capped at $10/day), "TranslateAPI" ($0.05/call, capped at
$15/day), and "SentimentAPI" ($0.01/call, capped at $8/day).

Each tool's per-tool budget guard reports healthy all month: none of the
three ever hits its individual cap.

At month end, finance receives three separate invoices totaling $940,
against an assumed ceiling of ($10+$15+$8) x 30 = $990/month — technically
under the sum, but nobody had approved a $990/month aggregate figure in
the first place; the $33/day implied combined rate was never reviewed or
signed off as a single number, and ticket volume growth means next month's
combined total is projected at $1,400 with no single alert that will fire
before the invoice does.
```

## Statistics
| Finding | Context |
|---------|---------|
| Agent systems using 3+ billed tools show aggregate spend 1.5-3x higher than any single tool's tracked budget would suggest | Typical multiplier observed when teams first build a cross-tool cost dashboard |
| Fewer than half of production agent deployments have a single aggregate spend metric spanning all tools used by one workflow | Estimated share based on common architecture patterns |
| Time-to-detection for cross-tool overspend is typically one full billing cycle (invoice-driven) versus same-day for per-tool caps | Typical range |

## Mitigations
1. **Central spend ledger**: Route every billable tool call, regardless of vendor, through a shared accounting middleware that increments one aggregate counter per session/task/account, independent of each tool's own cap.
2. **Workflow-level budget envelope**: Define the real spend ceiling at the level users actually care about (per task, per user, per day) and enforce it as a hard gate that checks the aggregate ledger before allowing any billable call to proceed, not just the target tool's own limit.
3. **Per-tool caps set as a fraction of the envelope, with headroom removed**: Ensure per-tool caps summed together do not exceed the intended aggregate ceiling; if independent caps must stay in place, compute them programmatically from the aggregate budget rather than setting each one in isolation.
4. **Daily reconciliation job**: Run an automated job that pulls actual usage from every connected tool and compares it against the aggregate envelope, alerting on drift before the billing cycle closes.
5. **Cost attribution tagging**: Tag every tool call with a task/session ID so aggregate spend can be sliced by workflow, making it possible to identify which combinations of tools are driving the overrun.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| aggregate_daily_spend_all_tools | Sum of billed spend across every tool for a given account/workflow | Alert if > 90% of aggregate envelope |
| per_tool_budget_healthy_but_aggregate_over_ratio | Count of periods where all per-tool caps passed but aggregate envelope was breached | Alert if > 0 in any 24h window |
| tool_combination_cost_variance | Day-over-day change in combined cost across the tool set used by one workflow type | Alert on > 25% day-over-day increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Aggregate envelope breach | Combined spend across all tools exceeds the approved aggregate ceiling for the period | High | Freeze non-critical billable calls, notify budget owner, reconcile against invoices |
| Silent per-tool pass / aggregate fail | All individual tool caps report healthy while the aggregate ledger shows > 90% of envelope consumed | Medium | Trigger manual review of tool-combination usage patterns |

## Related Patterns
- [Budget Priority Misalignment](./budget-priority-misalignment.md) - both involve budget enforcement blind spots, one across priority and one across tools
- [Per-Tool Monthly Budget Overrun](./per-tool-monthly-budget-overrun.md) - a single-tool version of the same detection-lag problem
- [Tool Cost Override Incident](./tool-cost-override-incident.md) - aggregate visibility gaps make overrides even harder to notice once granted
