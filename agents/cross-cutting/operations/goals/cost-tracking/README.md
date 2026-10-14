# AI Agent Cost Tracking Failures: Budget Overruns, Billing Gaps, and Missing Attribution

**Cost tracking failures happen when you cannot see, assign, or cap what your AI agents spend: budgets alert but do not stop spending, internal counts do not match invoices, and costs cannot be traced to a user or use case.** Six patterns cover measurement and enforcement.

## Key Takeaways

- An alert is not a limit: budget enforcement needs a hard stop at the infrastructure level.
- Token counts and invoices disagree for reasons the patterns list, such as different tokenizers and uncounted request types.
- Without request-level tags, multi-tenant costs cannot be attributed.
- Rate limits are handled here too, since mishandling them degrades or amplifies cost.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Billing Reconciliation Gaps](failures/billing-reconciliation-gaps.md) | Internal Cost Tracking Doesn't Match Vendor Invoices |
| [Budget Enforcement Bypass](failures/budget-enforcement-bypass.md) | Agent Exceeds Budget Limits Without Being Stopped |
| [Cost Anomaly Blindness](failures/cost-anomaly-blindness.md) | Unusual Cost Patterns Go Undetected |
| [Cost Attribution Errors](failures/cost-attribution-errors.md) | Costs Cannot Be Accurately Attributed to Users, Agents, or Use Cases |
| [Rate Limit Mishandling](failures/rate-limit-mishandling.md) | Agent Fails or Degrades When Hitting API Rate Limits |
| [Token Counting Inaccuracy](failures/token-counting-inaccuracy.md) | Internal Token Counts Don't Match Actual Usage |

**Total: 6 patterns**

## How These Patterns Group

- **Measuring:** [Token Counting Inaccuracy](failures/token-counting-inaccuracy.md), [Billing Reconciliation Gaps](failures/billing-reconciliation-gaps.md), [Cost Attribution Errors](failures/cost-attribution-errors.md)
- **Detecting and enforcing:** [Cost Anomaly Blindness](failures/cost-anomaly-blindness.md), [Budget Enforcement Bypass](failures/budget-enforcement-bypass.md)
- **Limits:** [Rate Limit Mishandling](failures/rate-limit-mishandling.md)

## When This Matters

- Several users, agents, or teams share the same API account
- Finance asks which feature drives spend
- Agents can run unattended

## Frequently Asked Questions

### How do I stop an AI agent from overspending?

Alerts are not enough. See [budget enforcement bypass](failures/budget-enforcement-bypass.md) for why hard stops matter.

### Why don't my token counts match the bill?

See [token counting inaccuracy](failures/token-counting-inaccuracy.md) and [billing reconciliation gaps](failures/billing-reconciliation-gaps.md).

### How do I know which user or feature costs the most?

That needs request-level tagging. See [cost attribution errors](failures/cost-attribution-errors.md).

## Related

- [All operations goals](../)
- [Operations overview](../../)
