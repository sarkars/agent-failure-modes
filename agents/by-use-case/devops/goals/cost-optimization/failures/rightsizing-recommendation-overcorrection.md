# Rightsizing Recommendation Overcorrection

## Issue: Agent Recommends Downsizing Compute Resources Based on Average Utilization, Ignoring Peak Load Requirements That Drive Actual Capacity Needs

**Frequency**: Very Common

**Symptoms**
- Cost-optimization agent recommends reducing instance size or replica count because average CPU/memory utilization over the analysis window is low
- Recommendation does not account for periodic peak load (end-of-month batch jobs, daily traffic peaks, seasonal spikes) that the average obscures
- Rightsizing is applied and the service subsequently fails to meet latency SLOs during the next peak period
- Cost savings are realized and reported as a win before the next peak period exposes the under-provisioning

**Root Cause**
Rightsizing recommendation agents commonly optimize against average or percentile utilization over a fixed historical window because it is the most readily available aggregate signal, but actual capacity requirements are driven by peak load, not average load — a service correctly sized for its average utilization can be severely under-provisioned for its peak. Without explicitly modeling the peak-to-average ratio and the business criticality of meeting peak demand, the agent's cost-minimizing recommendation systematically trades away headroom that exists specifically to absorb peaks.

**Example**
```
Scenario: Batch-processing service runs at 15% average CPU utilization most of the month
Agent recommendation: Downsize instance type to match the 15% average utilization, project 60% cost savings
Actual usage pattern: CPU utilization spikes to 95% during the last 3 days of each month for financial close processing
Rightsizing applied: Instance downsized
Next month-end: Batch jobs fail to complete within the required window due to insufficient capacity
Impact: Missed financial close deadline; the realized cost savings are offset by the business impact of the capacity shortfall
```

**Key Statistics**
- Average-utilization-based rightsizing without peak analysis is a commonly cited cause of capacity-related incidents following cost-optimization initiatives in cloud cost management practice
- Peak-to-average utilization ratios vary substantially by workload type, with batch, financial, and seasonal-retail workloads showing some of the largest peak-to-average gaps
- Self-learning autonomic infrastructure management research recommends incorporating peak-aware and workload-pattern-aware signals specifically because pure average-based optimization underperforms on workloads with periodic peaks

---

## Mitigation Strategies

1. **Peak-Aware Sizing**: Base rightsizing recommendations on a defined high percentile (e.g., p99 or documented peak periods) of historical utilization, not the average, especially for workloads with known periodicity
2. **Workload Pattern Classification**: Classify workloads by their peak-to-average ratio and periodicity (steady, daily-cyclical, monthly-batch, seasonal) before applying a rightsizing policy, since a one-size-fits-all average-based policy is unsafe for high-variance workloads
3. **Business-Criticality Weighting**: Weight rightsizing aggressiveness by the cost of missing peak capacity (e.g., financial close, order-processing peak) against the savings from downsizing, not cost savings alone
4. **Staged Rollout with Peak Validation**: Apply rightsizing changes ahead of, and validate against, the next known peak period before treating the change as final

### Metrics
- Peak-period SLO compliance rate following a rightsizing change
- Peak-to-average utilization ratio per workload, tracked as an input to sizing decisions
- Cost-savings-vs-capacity-incident rate following rightsizing initiatives

### Alerts
- Rightsizing recommendation generated using average utilization only, with no peak-period analysis, for a workload with known periodicity → P2
- SLO breach during a peak period following a recent rightsizing change → P1

---

## References

- [Enabling Autonomic Microservice Management through Self-Learning Agents](https://arxiv.org/pdf/2501.19056)
- [RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection](https://arxiv.org/pdf/2603.02345)
