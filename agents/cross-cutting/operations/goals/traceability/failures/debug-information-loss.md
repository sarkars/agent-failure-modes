# Debug Information Loss

## Issue: Information Needed for Debugging Lost Before Investigation

**Frequency**: Common

**Symptoms**
- Logs rotated before incident investigated
- Detailed traces only available briefly
- Error context summarized away
- Production debug info not captured
- Must reproduce bug to get debug data

**Root Cause**
Debug information—detailed traces, full payloads, intermediate states—is expensive to store and often contains sensitive data. Organizations configure short retention periods or sampling that discards information before it's needed. When incidents occur, the detailed information required for root cause analysis has already been deleted or was never captured.

**Example**
```
Incident: Agent made incorrect financial calculation
Reported: 3 days after occurrence

Investigation attempt:

Day 1:
  Logs available: Last 24 hours only
  Incident data: Already rotated
  
Day 2:  
  Request traces: Sampled at 1%, incident not in sample
  Full payloads: Only kept for 1 hour
  
Day 3:
  Detailed metrics: Aggregated to hourly, precision lost
  Error context: Summarized to "calculation error"
  
Available information:
  - Aggregated error count for that day
  - General system health metrics
  - Summary log: "Error in calculation module"
  
Needed information:
  - Exact input values
  - Intermediate calculation steps
  - External data retrieved
  - Model reasoning trace
  - Comparison calculations

Result: 
  - Cannot determine root cause
  - Cannot verify fix
  - Must wait for recurrence with monitoring in place
  - Customer issue unresolved for weeks
```

**Key Statistics**
From Observability Research (2026):
- Average log retention: 7-30 days
- Detailed trace retention: 1-24 hours
- Full payload retention: 1-4 hours
- 60% of incidents require data older than retention
- Debug reproduction adds 3-10x to resolution time

**Information Loss Types**
| Type | Typical Retention | Need Duration |
|------|-------------------|---------------|
| Detailed traces | 1-4 hours | Days to weeks |
| Full payloads | 1-24 hours | Days |
| Debug logs | 24-72 hours | Weeks |
| Error context | 7 days | Months |
| Metrics (detailed) | 24 hours | Weeks |

**Contributing Factors**
- Storage cost concerns
- Privacy and compliance limits
- Default retention too short
- Debug levels only in development
- No tiered retention strategy

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent performing financial calculations, with detailed trace retention set to 1-4 hours, full payload retention to 1 hour, and request sampling at a flat 1% rate
- No incident-triggered retention extension exists to preserve traces flagged as anomalous
- No cold-storage archival path exists once the hot-retention window expires; data is simply deleted
- The agent makes an incorrect financial calculation during normal operation

### Trigger Mechanism
1. The agent produces an incorrect financial calculation, but the error isn't visible to anyone at the time it occurs
2. The customer notices the discrepancy and reports it 3 days later
3. By the time the investigation begins, detailed traces (1-4 hour retention), full payloads (1 hour), and precise metrics (aggregated to hourly after 24 hours) have all already rotated out
4. The investigator is left with only an aggregated error count and a generic summary log entry: "Error in calculation module"

### Example Reproduction Steps
```
1. Day 0, 10:00: Agent performs calculation with input X, produces
   incorrect output Y (bug present, no anomaly flag raised at the time)
2. Day 0, 11:00: Full payload for this request is deleted (1-hour
   retention expired)
3. Day 0, 14:00: Detailed trace for this request is deleted (4-hour
   retention expired)
4. Day 3: Customer reports the incorrect calculation
5. Investigator queries for the original request:
   GET /traces?request_id=X -> 404, trace already rotated
   GET /logs?date=Day0 -> only "Error in calculation module" summary
   remains, no exact input values or intermediate steps
6. Investigation concludes: root cause cannot be determined; team must
   wait for recurrence with additional monitoring in place
```

### Expected Failure State
Three days after the incident, no exact input values, intermediate calculation steps, or reasoning trace remain retrievable, forcing the investigation to stall until the bug recurs with monitoring specifically added, leaving the customer's issue unresolved for weeks. A correctly defended system either extends retention automatically for traces later flagged as anomalous, or moves detailed traces to cold storage instead of deleting them, so the 3-day-later investigation can still retrieve the exact calculation steps.

## Mitigation Strategies

### Prevention
1. **Tiered retention keyed to error/anomaly status**: Automatically extend retention for traces and payloads associated with any detected error or anomaly (well beyond the default 1-4 hour full-payload window), so an incident reported 3 days later — as in the example — still has its detailed trace available instead of only an aggregated hourly metric. Trade-off: requires reliably classifying "this trace is error-adjacent" at capture time, and false negatives in that classification mean the extension never triggers for the traces that need it.
2. **Sampling with guaranteed rare-event capture**: Replace flat 1% sampling (which missed the incident entirely in the example) with a sampling strategy that always captures traces meeting anomaly criteria (unusual latency, error codes, out-of-range values) regardless of the base sampling rate. Trade-off: guaranteed-capture sampling costs more storage than flat-rate sampling and needs a well-tuned anomaly definition to avoid capturing everything.
3. **Cold-storage archival instead of hard deletion**: Move detailed traces/payloads to cheap cold storage after the hot-retention window instead of deleting them, so a 3-day-later investigation can still retrieve the exact input values and reasoning trace even if not from the fast-access tier. Trade-off: cold storage retrieval is slower and adds engineering work to build a retrieval path, and doesn't eliminate the need for privacy/compliance-driven redaction before archival.

### Detection & Response
1. **"Insufficient data" investigation-outcome tracking**: Explicitly tag incident investigations that conclude "cannot determine root cause due to missing data" (as in the example) and track this rate over time — a persistently high rate is a direct, measurable signal that retention policy is misconfigured relative to actual investigation needs.
2. **Debug-data-availability-at-incident-time measurement**: For each incident, measure how much of the ideally-needed data (exact inputs, intermediate steps, reasoning trace) was actually still available versus already rotated away, quantifying the gap the example describes numerically rather than anecdotally.
3. **Retention-vs-discovery-delay correlation**: Track the typical delay between an issue occurring and being reported/discovered, and compare it against current retention windows; the example's 3-day report delay against a 24-hour full-payload retention is exactly the mismatch this metric would surface proactively.

### Architecture Patterns
1. **Incident-triggered retention extension pipeline**: Build an automated mechanism that, upon error/anomaly detection, immediately extends retention for the relevant trace/payload/context data before the normal rotation window would delete it, rather than relying on someone to notice and manually intervene in time. Deployment consideration: needs to trigger fast enough (within the normal 1-4 hour full-payload window) to actually catch the data before it's gone, which requires real-time anomaly detection integrated with the retention system.
2. **Structured intermediate-state capture for calculation-heavy agent tasks**: For domains like financial calculations where "exact input values, intermediate calculation steps, external data retrieved" matter (as listed in the example's "needed information"), instrument the pipeline to capture these as structured, queryable records rather than relying on generic request/response logging that gets summarized away. Deployment consideration: requires per-domain instrumentation effort rather than a one-size-fits-all logging layer.
3. **Tiered storage architecture with automatic hot-to-cold migration**: Architect storage so detail level degrades gracefully over time (full detail → summarized → cold archive) instead of a hard cutoff to deletion, so investigations initiated late still have a fallback data source even if not the richest one. Deployment consideration: requires investment in a multi-tier storage pipeline and consistent tagging so data can be found across tiers during an investigation.

### Metrics
1. **insufficient_data_investigation_rate**: % of incident investigations that conclude with missing/insufficient debug data as a stated blocker; target < 10%; alert if > 30%.
2. **incident_data_availability_rate**: % of ideally-needed debug data elements (inputs, intermediate steps, reasoning trace) actually available at investigation time; target > 80%; alert if < 50%.
3. **retention_vs_report_delay_gap**: Difference between typical incident-report delay and current full-detail retention window; target ≤ 0 (retention covers typical delay); alert if retention is shorter than the median report delay.
4. **debug_reproduction_time_multiplier**: How much longer resolution takes when data must be reproduced rather than retrieved from retained detail; target < 2x; alert if > 5x (baseline research cites 3-10x, the failure state to avoid).

### Alerts
1. **Insufficient Data Rate Elevated** (P2): Condition — insufficient_data_investigation_rate exceeds 30% over a rolling month. Action: review retention tiers against actual incident-report delay patterns and extend the highest-value tiers (error context, detailed traces).
2. **Retention Window Shorter Than Report Delay** (P2): Condition — retention_vs_report_delay_gap is positive (retention window ends before the typical report delay). Action: extend retention for error-adjacent data specifically, using tiered/cold-storage strategies rather than uniformly extending all data retention.
3. **Reproduction Time Multiplier Spike** (P3): Condition — debug_reproduction_time_multiplier exceeds 5x for a category of incidents. Action: prioritize instrumentation improvements (structured intermediate-state capture) for that category to reduce reliance on reproduction.

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Retention strategies
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Debug challenges
- [Google SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/) - Observability retention
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Production debugging
