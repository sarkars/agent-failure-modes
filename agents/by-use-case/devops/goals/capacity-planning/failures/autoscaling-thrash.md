# Autoscaling Thrash from Reactive Agent Decisions

## Issue: Agent-Driven Autoscaler Repeatedly Scales Up and Down in Short Cycles Because Scaling Decisions React to Instantaneous Metrics Without Accounting for Provisioning Lag

**Frequency**: Common

**Symptoms**
- Scale-up triggered by a load spike, but by the time new capacity comes online the spike has passed and the agent immediately scales back down
- Scale-down decisions made during a brief lull are reversed seconds later when load returns, causing rapid oscillation
- Cost and latency both degrade simultaneously: cost rises from constant provisioning churn while latency rises from capacity being unavailable exactly when needed
- Cooldown periods are either absent or set identically regardless of how volatile the underlying traffic pattern is

**Root Cause**
Reactive scaling agents make decisions based on the current or very-recent metric value without modeling the lag between issuing a scaling decision and new capacity actually becoming available, nor the recent volatility of the traffic signal. When provisioning lag is non-trivial relative to the timescale of load fluctuations, decisions made on instantaneous readings are systematically late — appropriate for the load level several minutes ago — which produces oscillation rather than convergence to the right capacity level.

**Example**
```
Scenario: Autoscaling agent for a service with 90-second container startup time
Load pattern: Bursty traffic with spikes lasting 60-90 seconds
Agent: Scales up when load crosses threshold; new capacity online after spike has already subsided
Agent: Immediately scales back down seeing reduced load, capacity removed
Next spike: Repeats the same late-arrival cycle
Impact: Constant scaling churn, elevated cost from provisioning/deprovisioning overhead, and latency spikes during every under-provisioned window
```

**Key Statistics**
- Reactive autoscaling oscillation ("flapping") is a long-documented failure mode in cloud capacity management, with cooldown periods and predictive scaling cited as standard mitigations
- Workloads with provisioning lag comparable to or longer than typical load-fluctuation timescales are disproportionately prone to oscillation under purely reactive scaling policies
- Predictive/trend-aware scaling approaches (incorporating recent rate-of-change rather than instantaneous value) have been shown to reduce scaling event frequency substantially compared to threshold-reactive policies in autonomic infrastructure management research

---

## Mitigation Strategies

1. **Trend-Aware Scaling Decisions**: Base scaling decisions on a short trailing window and rate-of-change, not the instantaneous metric value, to account for provisioning lag
2. **Asymmetric Cooldowns Tuned to Lag**: Set scale-down cooldown periods proportional to the service's actual provisioning lag, preventing premature de-provisioning right after a scale-up
3. **Predictive Pre-Scaling**: Where load patterns are partially predictable (daily/weekly cycles), pre-scale ahead of expected demand rather than waiting for reactive triggers
4. **Oscillation Detection Circuit Breaker**: Detect rapid scale-up/scale-down cycling and automatically widen the decision window or escalate to manual review rather than continuing to thrash

### Metrics
- Scaling event frequency and time between consecutive opposite-direction events (oscillation rate)
- Capacity-availability lag relative to actual load changes
- Cost attributable to provisioning/deprovisioning churn vs. steady-state capacity cost

### Alerts
- More than N opposite-direction scaling events within a defined short window → P2
- Latency SLO breach correlated with a recent scale-down immediately preceding a load increase → P1

---

## References

- [Enabling Autonomic Microservice Management through Self-Learning Agents](https://arxiv.org/pdf/2501.19056)
- [RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection](https://arxiv.org/pdf/2603.02345)
