# Sales CRM AI Agent Failures by Goal: 16 Patterns, Causes, and Fixes

**Sales CRM AI agents fail in 4 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 16 documented patterns across 4 goals; the most documented is [Quota Achievement](quota-achievement/) with 5.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Sales CRM Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Deal Management](deal-management/) | When agents assemble contract clauses, track negotiated terms, or approve deals using stale pricing data, wrong contract templates, or missing handoff fields that capture negotiated exceptions | 3 |
| [Lead Scoring](lead-scoring/) | When agents compute a lead's likelihood-to-close using stale scoring rules, fabricated data when tool results are unavailable | 4 |
| [Pipeline Forecasting](pipeline-forecasting/) | Pipeline-forecasting failures occur across multiple independent dimensions: agents apply outdated stage-probability weights instead of current configuration | 4 |
| [Quota Achievement](quota-achievement/) | When agents calculate rep quota attainment using stale discount policies, fabricated approval records, mismatched coaching recommendations, or unverified credit adjustments | 5 |

**Total: 16 patterns**

## Frequently Asked Questions

### How do you prevent discount-policy cache lag from causing unauthorized approvals?

Implement event-coupled cache invalidation: when RevOps publishes a discount-policy change, immediately trigger cache-invalidation events that clear the discount-tool's cache within the same transaction. See [Quota Achievement](quota-achievement/).

### Can reps be trained to ignore stale-heuristic explanations even if an agent provides them with high confidence?

Partially. See [Lead Scoring](lead-scoring/).

### How much probability calibration discount should be applied to sales-rep estimates?

Typical empirical finding: reps estimate 40-60% higher probability than actual close rates. See [Pipeline Forecasting](pipeline-forecasting/).

## Related

- [Sales CRM overview](../)
- [All agent failure patterns](../../../)
