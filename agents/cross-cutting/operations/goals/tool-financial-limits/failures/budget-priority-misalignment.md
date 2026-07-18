# Budget Priority Misalignment

## Issue
An agent operating under a fixed tool-spend cap (e.g. $50/day across a web-search API, an enrichment API, and a document-generation API) has no concept of which calls matter most. It burns the budget on early, low-value exploratory calls — re-querying the same search API with slight prompt variations, or calling an enrichment tool on leads that were already disqualified — and then has nothing left when a high-value call (verifying a contract term before it's sent to a customer) is needed later in the same session.

**Frequency**: Common

**Symptoms**
- Budget exhausted well before the highest-value task in a session runs
- High cumulative call counts on cheap, exploratory, or retried operations relative to task value
- Critical late-session tool calls fail with "budget exceeded" while trivial early-session calls succeeded
- No difference in how the agent treats a $0.01 lookup versus a $2.00 verification call
- Post-hoc review shows the spend would have covered the important calls if the cheap ones had been rationed

## Root Cause
Most agent budget enforcement is implemented as a simple running counter compared against a ceiling — a gate, not an allocator. The agent's planning/tool-selection logic and the budget-enforcement logic are separate subsystems that don't share information: the planner doesn't know the remaining budget when it decides what to call next, and the budget gate doesn't know how important the current call is relative to calls still to come. Without an explicit priority or value scoring layer sitting between the two, spend order is effectively determined by task order, not task value.

## Example
```
An agent runs a 40-step research-and-draft workflow with a $20 session cap on
the "DocIntel" paid extraction API ($0.15/call).

Steps 1-25: agent calls DocIntel on every candidate document it finds during
broad discovery, including near-duplicate filings and low-relevance
attachments, spending $18.75 (125 calls).

Step 30: the agent reaches the step that actually matters — extracting
structured terms from the final, counterparty-signed contract, the one
output the user asked for — and the call fails: "budget exceeded, $20.00
cap reached."

The agent falls back to a regex-based heuristic on the raw text, produces
a lower-quality extraction, and the user only discovers the degradation
when a contract term is misread three weeks later.
```

## Statistics
| Finding | Context |
|---------|---------|
| 60-75% of tool-budget exhaustion incidents in multi-step agent workflows involve the failing call being lower business-value than calls made earlier in the same session | Typical range observed in production agent telemetry |
| Agents without call-level value scoring spend an estimated 30-40% of budget on exploratory/redundant calls | Estimated from workflows instrumented with post-hoc call classification |
| Adding a simple three-tier priority scheme (critical/normal/exploratory) reduces high-value call failures by roughly half | Reported range across teams that added priority-aware budget gates |

## Mitigations
1. **Priority-tagged budget pools**: Split the single budget into tiers (e.g. 70% reserved for "critical" calls, 30% for "exploratory"), tagged at call time by the agent's own task classifier, so exploratory spend physically cannot crowd out critical spend.
2. **Reserve-and-release accounting**: Before starting a multi-step plan, have the planner estimate and reserve budget for known high-value steps later in the plan; only release the reservation if those steps are skipped, rather than letting early steps freely consume the whole pool.
3. **Value-aware tool selection**: Require the agent's tool-call decision step to attach an explicit expected-value or task-criticality score, and sort/ration calls by that score when spend is running high relative to remaining budget.
4. **Late-session budget floor**: Enforce a minimum reserved balance that cannot be spent by calls before a configurable point in the workflow (e.g. the last 20% of planned steps), forcing early steps to economize.
5. **Post-session value audit**: Log every call with its cost and a retrospective value label, and periodically review whether spend order correlates with value; use this to recalibrate the priority scheme.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| budget_spent_before_critical_step_ratio | Fraction of total session budget spent before the first "critical"-tagged call | Alert if > 0.6 |
| exploratory_call_spend_share | Share of total spend attributed to exploratory/low-priority calls | Alert if > 40% |
| critical_call_failure_rate | Rate of critical-tagged calls failing due to budget exhaustion | Alert if > 1% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Critical call blocked by budget | A priority="critical" tool call is rejected due to insufficient remaining budget | High | Page on-call, allow manual budget top-up, review session's earlier spend |
| Exploratory spend spike | exploratory_call_spend_share exceeds 40% mid-session | Medium | Throttle exploratory calls, notify workflow owner |

## Related Patterns
- [Cross-Tool Total Budget Exceeded](./cross-tool-total-budget-exceeded.md) - both stem from budget enforcement that ignores call context, one across tools and one across priority
- [Tool Budget Starvation](./tool-budget-starvation.md) - a shared-pool variant of the same underlying problem, but across tasks/agents rather than within one session
- [Per-Tool Daily Budget Exhaustion](./per-tool-daily-budget-exhaustion.md) - describes the exhaustion mechanics that priority misalignment makes worse
