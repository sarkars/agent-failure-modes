# Per-Tool Tiered Pricing Unknown

## Issue
A tool vendor prices calls on a volume-tiered schedule — for example $0.05/call for the first 10,000 calls/month, dropping to $0.03/call from 10,001-50,000, and $0.015/call above that — but the agent has no visibility into which tier its current usage falls into. Without that knowledge, the agent can't make batching or scheduling decisions that would push usage into a cheaper tier, and in some cases actively spreads or throttles calls in ways that keep usage stuck in an expensive lower tier when consolidating the same volume would have unlocked meaningfully cheaper pricing.

**Frequency**: Occasional

**Symptoms**
- Effective cost-per-call stays flat or high across months even as total volume grows past documented tier breakpoints
- No component in the system tracks cumulative monthly volume against the vendor's published tier boundaries
- Manual, retrospective analysis of invoices reveals that volume crossed a cheaper-tier threshold mid-month, but the agent's behavior (call rate, batching) didn't change to take advantage of it
- Two teams or workflows using the same tool independently each stay under a tier breakpoint that they would have jointly crossed if usage were pooled and tracked together
- Cost-saving opportunities from consolidating or timing calls are only discovered by finance during contract renewal review, not by the system in real time

## Root Cause
Tiered pricing requires tracking cumulative usage against a running total and knowing the tier boundaries, which is meaningfully more complex than the flat per-call price most cost estimators are built around. Because the savings from tier optimization are usually not urgent (nothing breaks — it's a missed optimization, not an outage), this tracking is rarely prioritized during integration, and the agent's tool-selection and batching logic ends up making decisions based on a flat assumed price that may be significantly higher than what the account would actually be billed at its true usage level.

## Example
```
"SentimentAPI" bills at three tiers per month: $0.04/call for calls
1-50,000, $0.025/call for calls 50,001-200,000, and $0.012/call above
200,000. The agent's cost estimator uses a flat $0.04/call for all
budgeting and routing decisions, which was correct when the integration
was built and volume was well under 50,000/month.

Nine months later, organic growth has pushed monthly volume to roughly
180,000 calls — solidly in the $0.025 tier for most of those calls, with
real effective average cost around $0.027/call. But the agent's routing
logic, still assuming $0.04/call, periodically diverts sentiment-scoring
tasks to a lower-quality free heuristic whenever the (overestimated)
budget projection looks tight, even though the real budget has
substantial headroom at the true tier pricing.

Finance's quarterly vendor review finds the account has been paying the
correct tiered rate all along, but the agent has been needlessly
downgrading output quality based on a stale flat-rate cost assumption,
and nobody had updated the estimator since the original integration.
```

## Statistics
| Finding | Context |
|---------|---------|
| Volume-tiered pricing with 2-4 discrete tiers is a common structure for usage-based APIs, particularly in data enrichment, ML inference, and messaging categories | Common industry pricing pattern |
| Cost estimators are frequently calibrated once at integration time and not revisited as usage volume crosses tier boundaries over subsequent months | Frequently observed pattern in long-lived integrations |
| Effective cost-per-call misestimation of 20-40% has been observed in tools where usage has grown past the initial pricing tier without the cost model being updated | Typical range in mature integrations with organic volume growth |

## Mitigations
1. **Cumulative-volume-aware cost model**: Track running monthly call volume per tool and compute the actual marginal and blended cost-per-call based on the vendor's published tier schedule, rather than a fixed flat rate.
2. **Tier-boundary alerting**: Alert when monthly usage approaches a tier breakpoint (from either direction) so routing/budgeting logic can be reviewed and, where relevant, usage can be consolidated to cross into a cheaper tier.
3. **Periodic cost-model recalibration**: Schedule a recurring (e.g. quarterly) review that re-derives the effective cost-per-call from actual invoices and updates the estimator, rather than leaving it fixed from initial integration.
4. **Usage pooling across teams/workflows**: Where multiple internal workflows call the same vendor tool, track and report combined volume so tier optimization opportunities aren't missed due to fragmented, siloed usage tracking.
5. **Batching to intentionally reach favorable tiers**: For predictable, non-time-sensitive workloads, consider deferring or batching calls within a billing period specifically to help usage cross into a cheaper tier where the vendor's schedule rewards volume.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| current_pricing_tier | Which vendor pricing tier current cumulative monthly volume falls into | Informational; alert on tier transition |
| cost_model_staleness | Time since the cost estimator's per-call rate was last calibrated against actual invoices | Alert if > 90 days |
| effective_vs_modeled_cost_per_call | Actual blended cost-per-call from invoices versus the rate used in the agent's cost model | Alert if divergence exceeds 15% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Tier boundary approaching | Monthly cumulative volume is within 10% of the next tier breakpoint | Low | Consider batching remaining planned calls into the current billing period |
| Cost model stale | cost_model_staleness exceeds 90 days for a tiered-pricing tool | Medium | Recalibrate cost estimator against latest invoices |

## Related Patterns
- [Per-Tool Minimum Usage Penalty](./per-tool-minimum-usage-penalty.md) - both involve volume-dependent pricing structures the agent's optimization logic doesn't model
- [Per-Tool Cost-Per-Operation Surprise](./per-tool-cost-per-operation-surprise.md) - both stem from an oversimplified flat-rate cost model missing real pricing structure
- [Hidden Tool Costs Not Visible](./hidden-tool-costs-not-visible.md) - a related visibility gap where the true price driver isn't reflected in the agent's cost tracking
