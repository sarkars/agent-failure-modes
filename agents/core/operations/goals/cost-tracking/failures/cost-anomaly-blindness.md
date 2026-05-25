# Cost Anomaly Blindness

## Issue: Unusual Cost Patterns Go Undetected

**Frequency**: Common

**Symptoms**
- Runaway costs discovered only at month-end
- Gradual cost creep unnoticed
- Sudden spikes not alerted
- No baseline for "normal" costs
- Anomalies buried in aggregate metrics

**Root Cause**
Without anomaly detection, cost problems are only discovered when invoices arrive or budgets exhaust. Gradual increases (prompt bloat, new features) go unnoticed. Sudden spikes (loops, attacks) aren't caught in real-time. Organizations need both baseline tracking and anomaly detection.

**Example**
```
Cost timeline (undetected):

Week 1: $500/day (baseline)
Week 2: $520/day (prompt got longer - unnoticed)
Week 3: $580/day (new feature - unnoticed)
Week 4: $4,200/day (agent loop - UNNOTICED until Friday)

Total unexpected spend: $25,000

With anomaly detection:
Week 2: Alert - 4% above baseline (investigate)
Week 3: Alert - 16% above baseline (confirm new feature)
Week 4: Alert - 840% above baseline (STOP IMMEDIATELY)

Anomaly detection would have caught the loop on Day 1
```

**Contributing Factors**
- No cost baseline established
- Aggregate-only metrics
- Alerting only on absolute thresholds
- No velocity/rate-of-change tracking
- Manual review only
- Alerts go to unmonitored channels

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Spike detection | 5x cost spike | Alert in <5 min | No alert |
| Gradual increase | 10% daily increase | Alert by day 3 | Never alerted |
| New pattern | Different cost profile | Flagged for review | Unnoticed |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Detection latency | <5 min | Time to alert on anomaly |
| False positive rate | <10% | False alerts / total alerts |
| Anomaly coverage | 100% | Detected / actual anomalies |

---

## Mitigation Strategies

### Prevention
1. **Establish baselines**: Track normal cost patterns
2. **Rate-of-change alerts**: Alert on velocity, not just totals
3. **Statistical detection**: Use stddev-based thresholds
4. **Per-user/agent baselines**: Granular anomaly detection
5. **Real-time monitoring**: Sub-minute cost tracking
6. **Actionable alerts**: Route to on-call, not email

### Detection Methods
```
Simple: Alert if cost > 2x daily average
Better: Alert if cost > baseline + 3*stddev
Best:   ML-based anomaly detection with seasonality
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `cost.rate` | >3x baseline |
| `cost.velocity` | >2x previous hour |
| `cost.zscore` | >3.0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Cost Spike | >5x baseline | P1 |
| Cost Creep | +20% week-over-week | P3 |
| Velocity Anomaly | >3x normal rate | P2 |

---

## References

- [Arize: Cost Monitoring](https://arize.com/)
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code)
