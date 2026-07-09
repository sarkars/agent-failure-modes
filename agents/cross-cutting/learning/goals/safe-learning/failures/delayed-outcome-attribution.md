# Delayed Outcome Attribution

## Issue: Business outcome arrives later and cannot be attributed to agent action.

**Frequency**: Occasional

**Symptoms**
- No link from agent trace to KPI outcome.
- [Add more specific symptoms]

**Root Cause**
Business outcome arrives later and cannot be attributed to agent action.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **End-to-End Trace-to-Outcome Linking**: Propagate a persistent trace/session ID from every agent action through downstream systems (CRM, billing, support tickets) so that a KPI event arriving weeks later can be joined back to the specific agent decisions that preceded it, rather than being attributed at the account or campaign level.
2. **Delayed-Reward Windowing**: Define an explicit attribution window and decay function per outcome type (e.g., churn attributed to actions within the prior 30 days, weighted by recency) so credit assignment has a documented, reviewable methodology instead of ad hoc guessing when the outcome finally arrives.
3. **Outcome Proxy Validation**: Before relying on any fast-arriving leading indicator (e.g., immediate CSAT) as a stand-in for the true lagging outcome, validate its correlation against historical ground-truth outcomes; only promote proxies with demonstrated predictive validity to short-term learning signals.

### Detection & Response
1. **Attribution Coverage Monitoring**: Track the percentage of lagging outcome events that successfully join back to an agent trace; a drop indicates the linking pipeline is broken or trace IDs are being dropped somewhere in the outcome path.
2. **Attribution Latency Tracking**: Measure the time between agent action and outcome arrival per outcome type; if latency regularly exceeds the attribution window or trace-retention TTL, extend retention or the window rather than silently losing credit.
3. **Silent Attribution Gap Alerting**: Flag outcome events that arrive with no matching trace at all (not just low-confidence joins), since these represent completely unattributed business impact that skews any downstream learning that ignores them.

### Architecture Patterns
1. **Outcome Event Bus with Trace ID Propagation**: An async event bus (e.g., Kafka topic keyed by trace_id/session_id) that downstream systems publish outcome events to, decoupling the agent's real-time path from the delayed join, which runs as a separate consumer.
2. **Deferred Credit Assignment Store**: A store holding pending trace-to-outcome pairs while awaiting the lagging outcome, with TTL-based expiry so unmatched traces age out explicitly rather than accumulating unbounded or being silently discarded.
3. **Multi-Touch Attribution Model**: Where multiple agent actions precede a single outcome, apply a documented attribution model (last-touch, decay-weighted, or Shapley-value) so credit is split defensibly across contributing actions instead of assigned arbitrarily to the most recent one.

### Metrics
1. **trace_to_outcome_join_rate_percent**: Target: > 90%; Alert threshold: < 70%
2. **median_attribution_latency_days**: Target: within defined attribution window; Alert threshold: exceeds window for > 10% of outcomes
3. **unattributed_outcome_rate_percent**: Target: < 10%; Alert threshold: > 25%
4. **proxy_ground_truth_correlation**: Target: > 0.6; Alert threshold: < 0.3 (proxy no longer predictive)

### Alerts
1. **Attribution Pipeline Broken** (P1 - Critical): Condition - trace-to-outcome join rate drops below 70%. Action: Halt any learning updates relying on outcome attribution, investigate trace propagation/retention pipeline immediately.
2. **Attribution Window Exceeded** (P2 - Warning): Condition - median attribution latency exceeds the configured window for a growing share of outcomes. Action: Extend trace retention/window, re-evaluate whether current window still matches business reality.
3. **Proxy Metric Decoupled from Ground Truth** (P3 - Info): Condition - proxy-to-outcome correlation degrades below 0.3. Action: Stop using proxy for short-term learning decisions, re-derive or replace proxy metric.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
