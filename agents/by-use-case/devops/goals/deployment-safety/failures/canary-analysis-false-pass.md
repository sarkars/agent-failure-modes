# Canary Analysis False Pass

## Issue: Agent Approves a Canary Deployment as Healthy Based on Aggregate Metrics That Mask a Regression Affecting a Specific Traffic Segment

**Frequency**: Common

**Symptoms**
- Canary analysis compares aggregate error rate/latency between canary and baseline and approves promotion when both look statistically similar overall
- A regression affecting a specific customer segment, region, or request type (e.g., a particular API version, a specific geography) is diluted into the aggregate and falls below the detection threshold
- Canary traffic volume or composition does not match production traffic composition closely enough for the comparison to be valid, but the agent proceeds anyway
- Full rollout proceeds and the segment-specific regression becomes visible only once it affects a larger absolute number of requests

**Root Cause**
Canary analysis agents are typically configured to compare a small number of aggregate health metrics between canary and baseline cohorts. When the regression is concentrated in a minority traffic segment, its effect on the aggregate metric can fall within normal statistical noise even though the regression is severe within that segment — the aggregate comparison is mathematically sound but answers a question ("is the canary healthy overall?") different from the one that actually matters for safe rollout ("is the canary healthy across every meaningful segment?").

**Example**
```
Scenario: Canary deployment receiving 5% of production traffic
Aggregate error rate: Canary 0.4% vs. baseline 0.3% — within normal variance, approved
Segment breakdown (not checked): Canary error rate for mobile-app-v2 requests specifically is 8%, baseline is 0.3%
Mobile-app-v2 share of total traffic: 5% — small enough that its regression is statistically invisible in the aggregate
Full rollout: Proceeds; mobile-app-v2 users experience widespread failures
Impact: Production incident affecting a specific user segment, detected only after full rollout
```

**Key Statistics**
- Segment-level metric dilution is a documented failure mode in canary analysis and progressive delivery practice, particularly for low-traffic-share segments
- Multi-dimensional canary analysis (segmented by region, client version, request type) is consistently recommended in SRE practice specifically because aggregate-only comparison has a known blind spot for segment-concentrated regressions
- Agentic deployment-safety research on automated rollout decision-making identifies single-metric or aggregate-only gating as a leading cause of false-pass canary approvals

---

## Mitigation Strategies

1. **Mandatory Segment-Level Comparison**: Require canary analysis to compute health metrics broken down by the highest-cardinality dimensions that matter operationally (client version, region, request type), not aggregate-only
2. **Minimum Per-Segment Sample Size Gate**: Do not approve promotion if any tracked segment has too little canary traffic to draw a statistically meaningful conclusion — flag for extended observation instead
3. **Worst-Segment Gating**: Gate promotion on the worst-performing tracked segment, not the aggregate, so a severe localized regression cannot be diluted away
4. **Traffic Composition Matching**: Verify canary traffic composition is representative of production traffic composition before relying on the comparison; if not representative, extend or reshape canary traffic first

### Metrics
- Per-segment error rate/latency delta between canary and baseline, for all tracked segments
- Minimum segment sample size achieved before promotion decision
- Rate of post-promotion regressions traced back to a segment that was statistically invisible in aggregate metrics

### Alerts
- Any tracked segment shows a statistically significant regression even if aggregate metrics pass → P1
- Canary promoted with a tracked segment below minimum sample size threshold → P2

---

## References

- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
- [RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection](https://arxiv.org/pdf/2603.02345)
