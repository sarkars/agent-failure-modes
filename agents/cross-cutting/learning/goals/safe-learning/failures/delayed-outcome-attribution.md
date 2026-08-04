# Delayed Outcome Attribution

## Issue: Business outcome arrives later and cannot be attributed to agent action.

**Frequency**: Occasional

**Symptoms**
- No link from agent trace to KPI outcome.
- Credit for a lagging outcome (e.g., renewal, churn, chargeback) gets assigned to whichever agent action is temporally closest, even when an unrelated action actually drove the result.
- Learning updates stall or apply stale/wrong reward because the outcome event arrives after the trace has already expired or been purged.

**Root Cause**
Business outcome arrives later and cannot be attributed to agent action.

**Example**
```
A retention agent offers a customer a discount during a support chat in week 1. The customer churns
in week 6, after several unrelated product-quality issues in weeks 2-5. The billing system's churn
event carries only an account ID, not a trace ID, so the learning pipeline joins the churn outcome to
the most recent agent action on that account -- a routine password-reset macro run in week 5 -- and
penalizes that unrelated action while the actual discount-offer decision (which may have delayed the
churn by five weeks) receives no credit or blame at all.
```

**Contributing Factors**
- Trace/session IDs are not propagated into downstream systems (billing, CRM, support) that eventually emit the outcome event.
- Trace retention TTL is shorter than the typical outcome latency, so the linking record has already expired by the time the outcome arrives.
- Multiple agent actions precede a single outcome with no documented multi-touch attribution model, so credit defaults arbitrarily to the last or nearest action.
- No validated short-term proxy metric exists, forcing either a long wait for ground truth or reliance on an unvalidated stand-in.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Late-arriving outcome join | Simulated churn event arriving 45 days after the originating agent action, trace TTL set to 30 days | Pipeline either extends retention to capture the join or explicitly logs the trace as expired/unattributed | Outcome silently attributes to an unrelated, more recent action on the account |
| Multi-touch credit split | Account with 3 distinct agent actions in the 30 days preceding a renewal outcome | Credit is split per the documented attribution model (e.g., decay-weighted) across all 3 actions | All credit lands on only the single most recent action |
| Proxy-vs-ground-truth backtest | Historical dataset with both an immediate proxy signal (e.g., CSAT) and the eventual ground-truth outcome | Correlation between proxy and ground truth is computed and reported before the proxy is used for learning | Proxy is used for reward without any correlation check against ground truth |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| trace_to_outcome_join_rate_percent (eval set) | > 90% | Replay historical outcome events against stored traces and measure successful join rate |
| attribution_window_coverage_percent | > 90% of outcomes arrive within the configured window | Compare outcome arrival latency distribution against the documented attribution window in a backtest |
| proxy_ground_truth_correlation | > 0.6 | Correlate proxy metric values with eventual ground-truth outcomes on a held-out historical cohort |

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
| trace_to_outcome_join_rate_percent | < 70% |
| unattributed_outcome_rate_percent | > 25% |
| proxy_ground_truth_correlation | < 0.3 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Attribution Pipeline Broken | trace-to-outcome join rate drops below 70% | Critical |
| Attribution Window Exceeded | median attribution latency exceeds the configured window for a growing share of outcomes | Medium |
| Proxy Metric Decoupled from Ground Truth | proxy-to-outcome correlation degrades below 0.3 | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
