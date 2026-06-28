# Metric Cardinality Explosion & Storage Overflow

## Issue: Monitoring System Creates High-Cardinality Metrics (Unbounded Labels); Storage & Performance Collapse

**Frequency**: Common

**Symptoms**
- Metric: request_latency{endpoint: "/api/users/:id", user_id: "12345"}
- Millions of unique user IDs → Millions of metric time series
- Metric storage database explodes in size
- Query performance degrades; monitoring becomes unusable
- Database crashes under cardinality load

**Root Cause**
High-cardinality labels (user ID, request ID, etc.) create combinatorial explosion. Each unique label value = new time series. Monitoring systems have hard limits on cardinality (Prometheus: millions, not billions). Labels should have bounded values (status code, endpoint). Unbounded labels cause system collapse.

**Example**
```
Scenario: API request latency monitoring
Metric: api_request_latency{endpoint, method, status_code, user_id}
Normal case: 10 endpoints × 5 methods × 3 status × 100 users = 15K metrics (OK)
Production case: 10 endpoints × 5 methods × 3 status × 10M users = 1.5B metrics (DISASTER)

Storage: Designed for 10K metrics; now stores 1.5B
Time series database: Crashes; monitoring goes down
Consequence: Can't see what's happening in production!

Impact: Blind to issues; fire fighting without data
```

**Key Statistics**
- Cardinality explosion risk: 10-100x growth with unbounded labels
- Storage multiplier: From 1GB to 100GB+ for single metric
- Query performance: Linear slowdown with cardinality

---

## Mitigation Strategies

1. **Label Guidelines**: Define which labels are allowed; enforce bounded cardinality
2. **Cardinality Monitoring**: Alert when metric cardinality exceeds threshold
3. **Sampling**: Sample high-cardinality data (e.g., 1% of users) instead of 100%
4. **Separate Storage**: Use distinct storage systems for different cardinality levels

### Metrics
- Metric cardinality (should be <1M per metric)
- Storage usage (should remain under budget)
- Query latency (should remain <1 second)

### Alerts
- Cardinality growth >10x → Investigate; likely misconfiguration

---

## References

- [Metric Cardinality Management](https://arxiv.org/abs/2106.04835)
- [Monitoring System Scalability](https://arxiv.org/abs/2001.05289)
