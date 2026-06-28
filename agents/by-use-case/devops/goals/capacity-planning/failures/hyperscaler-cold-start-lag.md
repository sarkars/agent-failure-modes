# Hyperscaler Cold Start Lag in Auto-Scaling

## Issue: Auto-Scaling Agent Doesn't Account for Cloud Provider Cold-Start Latency; Instances Take 2-5 Min to Start; Traffic Lost During Gap

**Frequency**: Common

**Symptoms**
- Traffic spike detected; scale-out triggered
- But new instances take 2-5 minutes to start (AMI boot, app startup)
- Traffic hits system before scaling completes
- Latency spikes, requests timeout, cascade failure

**Root Cause**
Scaling models predict traffic spikes; trigger scale-out. But assume instances start instantly. Reality: cloud instances need AMI boot (~1-2 min) + application startup (~1-3 min) = 2-5 min total. During this window, traffic hits under-provisioned cluster; latency spikes.

**Example**
```
Scenario: E-commerce site traffic spike (Black Friday)
Autoscaler detects: "QPS from 1K to 5K (5x spike)"
Action: Spin up 4 new instances
Reality: Instances take 3 minutes to start
Timeline:
- T=0: Spike detected
- T=0-3min: 4 instances starting (not serving yet)
- T=0-3min: Traffic hits original 2 instances
- Latency: 200ms → 2000ms (request timeout)
- Requests fail; customers see errors

After T=3min: New instances start; cluster has 6 instances; latency recovers
Impact: 3 minutes of bad customer experience; lost sales
```

**Key Statistics**
- Cold start latency: 2-5 minutes (EC2, varies by AMI)
- Warmup time to full performance: 2-5 more minutes (JVM startup, etc.)
- Total scale-out delay: 4-10 minutes
- Traffic lost during gap: 10-30% of requests

---

## Mitigation Strategies

1. **Predictive Scaling**: Scale ahead of demand, not reactively
2. **Warm Instance Pool**: Keep N warm instances ready (trade cost for latency)
3. **Serverless**: Use serverless (Lambda, Cloud Run) for instant scaling
4. **Canary Instances**: Pre-warm instances during low-traffic periods
5. **Brownout Handling**: Gracefully degrade service during scale lag

### Metrics
- Scale-out latency (minutes to serve traffic)
- Request loss during scale-out
- Cost of warm pools vs. benefit

### Alerts
- Cold start latency >2 min detected → Adjust scaling strategy

---

## References

- [Auto-Scaling in Cloud Systems](https://arxiv.org/abs/2007.00066)
- [Predictive Scaling & Workload Forecasting](https://arxiv.org/abs/2006.00685)
