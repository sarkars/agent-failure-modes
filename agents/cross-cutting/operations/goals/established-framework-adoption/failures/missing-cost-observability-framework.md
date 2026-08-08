# Missing Cost Observability Framework

## Issue: Team tracks LLM spend via manual log scraping or spreadsheet exports instead of adopting an established gateway/observability framework, losing real-time budget enforcement and per-call cost attribution.

**Frequency**: Common

**Symptoms**
- Cost data is reconstructed after the fact from raw provider billing exports rather than attributed per-call, per-session, or per-customer in real time
- Budget limits, if they exist at all, are enforced by a human periodically checking a spreadsheet rather than a gateway rejecting or throttling calls before spend occurs
- Per-customer or per-feature cost attribution requires a manual join between provider invoices and application logs, taking days to answer "which customer/feature drove this spike"
- A runaway agent loop or retry storm is only discovered once the monthly provider invoice arrives, days or weeks after the spend occurred
- Token usage and cost figures differ between the finance spreadsheet, the provider dashboard, and engineering's own estimates, with no single source of truth reconciling them

**Root Cause**
Cost tracking was never evaluated against an established gateway or observability framework before the team built custom logging, largely because spend monitoring was treated as a finance/ops afterthought bolted on after launch rather than an architectural requirement designed in alongside the model integration. Direct provider SDK calls scattered across multiple services with no shared proxy layer make it structurally difficult to retrofit centralized budget enforcement later, and because no one owns "LLM spend" as a metric the way an SRE owns latency or error rate, nobody is incentivized to invest in real-time attribution tooling. The gap stays hidden as long as usage volume is low enough that manual log scraping appears to "work," and only becomes visible once volume outpaces what a spreadsheet workflow can catch before the damage is done.

**Example**
```
A B2B SaaS company adds an AI writing assistant feature, calling a third-party
model provider directly from the application backend. To "keep an eye on cost,"
the team exports the provider's monthly usage CSV into a shared spreadsheet and
eyeballs the total against revenue once a month.

One customer's account gets compromised and an attacker scripts thousands of
rapid-fire requests through the writing assistant overnight. Because there was
no gateway enforcing a per-customer or per-session budget in real time, and no
observability layer attributing cost per call as it happened, nothing blocked
or even flagged the spike. The team only discovered the problem three weeks
later when the provider's monthly invoice arrived nearly 40x higher than
usual. By then they had no way to quickly determine which customer, endpoint,
or prompt template had driven the spend - that required manually cross-referencing
application logs against the provider's raw usage export line by line, a two-day
exercise that an established LLM gateway with per-call cost attribution and
budget enforcement would have prevented from happening in the first place.
```

**Contributing Factors**
- No evaluation of established LLM gateway (budget enforcement before spend) or tracing/observability (cost attribution after the fact) frameworks was done before building custom logging
- Cost tracking is treated as a finance/ops afterthought bolted on post-launch, rather than an architectural requirement designed in alongside the model integration
- Direct provider SDK calls are scattered across multiple services with no shared proxy layer, making it structurally hard to retrofit centralized budget enforcement later
- Nobody owns "LLM spend" as a metric the way an SRE owns latency or error rate, so no one is incentivized to invest in real-time attribution tooling
- Early-stage usage volumes were low enough that manual log scraping "worked fine," so the gap wasn't visible until usage scaled past what a spreadsheet workflow could handle

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Per-customer budget enforcement | Simulated burst of requests from a single customer exceeding their configured daily budget | Gateway throttles or blocks further calls once budget is hit, in real time | Requests continue to succeed past the configured budget with no rejection |
| Cost attribution latency | A batch of tagged test calls (known customer/feature labels) run through the pipeline | Cost dashboard reflects per-call, per-customer, per-feature cost within minutes | Attributing cost to the correct customer/feature requires manual log cross-referencing or waiting for a billing export |
| Runaway loop detection | Simulated retry storm / infinite agent loop generating rapid repeated calls | Anomaly detection flags the spike and alerts within minutes | Spike is only visible after the monthly invoice arrives |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Time to detect a cost anomaly | < 15 minutes | Inject a synthetic spend spike in staging and measure time until an alert fires |
| Per-call cost attribution coverage | 100% of calls tagged with customer/feature/session ID | Audit a sample of gateway/trace logs for missing attribution metadata |
| Budget enforcement latency | < 1 request over-budget before block | Run a scripted burst against a test budget and count requests that succeed after the limit is reached |

---

## Mitigation Strategies

### Prevention
1. **Adopt an LLM gateway (LiteLLM, Portkey, or Helicone)**: Route all model calls through a proxy layer that enforces per-customer/per-session/per-team budgets before spend occurs, rather than discovering overspend after the invoice arrives.
2. **Adopt an observability/tracing framework (Langfuse, LangSmith, or Braintrust)**: Attribute cost per call, per session, and per customer/feature in real time, replacing manual log scraping and spreadsheet reconciliation.
3. **Run a build-vs-buy evaluation before extending in-house logging**: Before adding another custom cost-logging script, compare it against the budget-enforcement and attribution capabilities an established gateway/observability stack already ships with.

### Detection & Response
1. **Real-time anomaly detection on spend rate**: Alert when spend-per-minute or spend-per-customer deviates significantly from a rolling baseline, rather than waiting for month-end reconciliation.
2. **Automatic circuit breaker on budget breach**: Gateway automatically throttles or blocks further calls once a configured budget threshold is hit, with an audit trail of the block event.
3. **Monthly reconciliation review**: Compare gateway-reported spend against the provider's actual invoice to catch attribution or configuration drift, treating discrepancies as a bug to fix, not routine noise.

### Architecture Patterns
1. **Gateway-first integration**: All application services call the model through a shared gateway/proxy rather than the provider SDK directly, so budget enforcement and attribution can't be bypassed by a new integration point.
2. **Two-layer cost architecture**: Layer 1 (gateway/proxy) enforces budgets before spend; Layer 2 (tracing/observability) attributes cost after the fact for analysis and reporting - mirroring how the missing framework class is typically structured.
3. **Tagged-call convention**: Every call carries structured metadata (customer ID, feature, session) at the point of the request so downstream attribution never requires reconstruction from unstructured logs.

### Metrics
1. **cost_anomaly_detection_latency_minutes**: Target: < 15 min; Alert threshold: > 60 min
2. **per_call_attribution_coverage_pct**: Target: 100%; Alert threshold: < 95%
3. **budget_enforcement_overshoot_requests**: Target: 0; Alert threshold: > 5 requests past budget

### Alerts
1. **Customer Budget Breach Without Enforcement** (P1 - Critical): Condition - a customer/session exceeds its configured budget and calls continue to succeed past the limit. Action: page on-call, manually throttle the offending key/customer, open incident review.
2. **Spend Rate Anomaly** (P2 - Warning): Condition - spend-per-minute exceeds rolling baseline by a large margin. Action: notify on-call, investigate for runaway loop or compromised credential.
3. **Attribution Coverage Gap** (P3 - Info): Condition - a percentage of calls lack customer/feature attribution metadata. Action: notify the owning team to add tagging to the integration.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| cost_anomaly_detection_latency_minutes | > 60 min |
| per_call_attribution_coverage_pct | < 95% |
| budget_enforcement_overshoot_requests | > 5 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Budget breach without enforcement | Customer/session spend exceeds configured budget and calls keep succeeding | High |
| Spend rate anomaly | Spend-per-minute deviates sharply from rolling baseline | Medium |
| Attribution coverage gap | A rising share of calls lack customer/feature attribution metadata | Medium |

---

## Related Patterns

- [Cost Anomaly Blindness](../../cost-tracking/failures/cost-anomaly-blindness.md) - the downstream symptom of not noticing cost spikes; this pattern is the upstream root cause of not adopting a framework that would surface them by default
- [Budget Enforcement Bypass](../../cost-tracking/failures/budget-enforcement-bypass.md) - a related downstream failure this pattern's missing gateway layer would help prevent

## References

- [LLM Gateway 2026: OpenRouter vs LiteLLM vs Portkey vs Helicone](https://klymentiev.com/blog/llm-gateway-guide) - layered architecture: Layer 1 gateway/proxy (LiteLLM, Helicone, Portkey) enforces budget limits before spend; Layer 2 observability/tracing (Langfuse, LangSmith, Braintrust) attributes cost after the fact
- [Best LLM Cost Tracking Tools (2026)](https://leanlm.ai/blog/llm-cost-tracking-tools) - comparison of cost-tracking tooling options
- Langfuse (MIT), Opik (Apache 2.0), and MLflow (Apache 2.0) are named as fully open-source, no-restriction options for cost/observability tracing
