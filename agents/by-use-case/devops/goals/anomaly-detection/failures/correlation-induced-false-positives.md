# Correlation-Induced False Positives in Multi-Metric Anomaly Detection

## Issue: Multiple Correlated Metrics All Spike Together; Model Flags as Coordinated Attack But Actually Cascading Failure

**Frequency**: Common

**Symptoms**
- Multiple metrics spike simultaneously (CPU, Memory, Disk I/O all high)
- Model sees correlated spike → High confidence in alert
- Actually: Single root cause (slow query) causing cascade
- Alert should be single incident, not multi-metric anomaly

**Root Cause**
Metrics in systems are highly correlated. When one goes wrong, others follow. Models sometimes learn that coordinated metric spikes are more anomalous; but in reality, correlated metrics indicate cascade, not coordinated attack. Missing the causal structure; treating correlation as stronger signal than it is.

**Example**
```
Scenario: Database performance monitoring
Event: Slow query on table X locks rows
Metrics all spike together:
- Query latency: up 10x
- CPU: up 200%
- Disk I/O: up 500%
- Memory: up 100%

Model sees 4 metrics abnormal simultaneously → "CRITICAL MULTI-SYSTEM FAILURE"
Reality: 1 root cause (slow query), 4 effects
Impact: Wrong diagnosis; time wasted investigating "multi-system failure"
```

**Key Statistics**
- Metric correlation in normal operation: 0.7-0.9 (high)
- Correlation during cascade failure: 0.8-0.95 (higher, but not anomalous)
- Precision with correlation-aware: 95%, without: 60%

---

## Mitigation Strategies

1. **Root Cause Analysis**: Trace cascades to single root cause
2. **Correlation Normalization**: Adjust anomaly scores for expected correlation
3. **Causal Models**: Learn causal relationships; reduce redundant alerts
4. **Single-Incident Grouping**: Group correlated alerts into single incident

### Metrics
- Alert precision (true incidents / total alerts)
- Incident clustering accuracy

### Alerts
- Multi-metric spike → Trace to root cause, group into single incident

---

## References

- [Correlation-Aware Anomaly Detection](https://arxiv.org/abs/2012.08844)
- [Root Cause Analysis in Monitoring](https://arxiv.org/abs/1906.04905)
