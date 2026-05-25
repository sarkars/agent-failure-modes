# Response Time SLA Breach

## Issue: System Exceeds Latency Commitments

**Frequency**: Common

**Symptoms**
- User-facing latency exceeds promised SLA
- Customer complaints about slow responses
- Timeout errors in downstream systems
- Degraded user experience scores

**Root Cause**
System design doesn't account for real-world latency distribution. P50 may be acceptable but P99 exceeds SLA. Load spikes, model complexity, or infrastructure issues push response times beyond commitments.

**Example**
```
SLA: 95% of requests under 2 seconds

Actual performance:
- P50: 800ms ✓
- P90: 1.8s ✓
- P95: 3.2s ✗ (SLA breach)
- P99: 8.5s ✗✗

Root causes:
- Complex queries hit P99: long context, multi-tool
- Peak hours: 3x normal latency
- Cold starts after scaling events
```

**Contributing Factors**
- No latency budgeting across components
- Testing only happy path scenarios
- Not accounting for tail latency
- Missing load testing at scale
- Infrastructure not right-sized

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Load test at 2x traffic | Sustained load | P95 < SLA | P95 exceeds SLA |
| Complex query latency | Multi-tool query | < 3s | > 5s |
| Peak hour simulation | Spike traffic | Graceful degradation | Cascading failures |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| P95 response time | < SLA | Percentile tracking |
| SLA compliance rate | > 99% | (requests under SLA) / total |
| Latency variance | Low | stddev of response times |

---

## Mitigation Strategies

### Prevention
1. **Latency budgeting**: Allocate time budget per component
2. **Tail latency design**: Design for P99, not P50
3. **Load testing**: Regular tests at 2-3x expected load
4. **Graceful degradation**: Fallback to faster, simpler responses
5. **Right-sizing**: Match infrastructure to latency requirements

### Detection
- Real-time percentile monitoring
- SLA compliance dashboards
- Anomaly detection on latency distribution

### Recovery
- Auto-scaling triggers
- Circuit breakers for slow dependencies
- Request shedding under extreme load

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `response.latency.p95` | > SLA target |
| `response.latency.p99` | > 2x SLA target |
| `sla.compliance.rate` | < 99% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| SLA Breach | P95 > SLA for 5 min | P1 |
| Latency Degradation | P50 > 2x baseline | P2 |
| Tail Latency Spike | P99 > 3x P50 | P2 |

---

## References

- [Google SRE: Latency SLOs](https://sre.google/sre-book/service-level-objectives/)
- [Tail Latency at Scale](https://research.google/pubs/pub40801/)
