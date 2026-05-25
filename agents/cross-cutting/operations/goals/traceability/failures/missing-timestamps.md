# Missing Timestamps

## Issue: Events Logged Without Accurate Timing Information

**Frequency**: Common

**Symptoms**
- Cannot determine action sequence order
- Performance analysis impossible
- SLA compliance unverifiable
- Concurrent events indistinguishable
- Causality unclear in incident analysis

**Root Cause**
Log entries are created without timestamps, with inaccurate timestamps (wrong timezone, clock drift), or with insufficient precision. When investigating incidents or analyzing performance, the timing of events is crucial for understanding what happened and in what order. Missing or wrong timestamps make this impossible.

**Example**
```
Incident: Customer saw inconsistent data

Log entries found:
  "Customer record updated"
  "Cache invalidated" 
  "Customer record read"
  "Response sent"

Questions:
  Q: "Did cache invalidate before or after read?"
  A: No timestamps - cannot determine
  
  Q: "Was update before read?"
  A: Log order suggests yes, but logs may be out of order
  
  Q: "How long between update and cache invalidation?"
  A: Unknown - no timing data

With proper timestamps:
  10:30:01.234 - Customer record updated
  10:30:01.890 - Customer record read      ← Read before invalidation!
  10:30:02.001 - Cache invalidated         ← Root cause found
  10:30:02.005 - Response sent (stale data)

Without timestamps:
  - Cannot prove cache timing issue
  - Cannot calculate latencies
  - Cannot verify SLA compliance
  - Cannot reproduce timing-dependent bugs
```

**Key Statistics**
From Observability Research (2026):
- 30% of log entries lack precise timestamps
- Timezone issues affect 15% of distributed systems
- Clock drift causes 5% ordering errors
- Millisecond precision needed for most debugging
- Nanosecond precision needed for high-frequency operations

**Timestamp Issues**
| Issue | Impact | Frequency |
|-------|--------|-----------|
| No timestamp | Cannot order events | Occasional |
| Second-only precision | Cannot order fast events | Common |
| Wrong timezone | Correlation errors | Common |
| Clock drift | Ordering errors | Occasional |
| Batch timestamps | False simultaneity | Common |

**Contributing Factors**
- Timestamps added as afterthought
- Different precision across services
- Timezone handling inconsistent
- Clock synchronization neglected
- Log batching loses precision

**Mitigation Strategies**
1. **Automatic timestamps**: Framework-level timestamp injection
2. **High precision**: Microsecond or nanosecond timestamps
3. **UTC everywhere**: Standardize on UTC, convert for display
4. **Clock sync**: NTP or better time synchronization
5. **Monotonic clocks**: Use monotonic clocks for ordering
6. **Timestamp validation**: Check for timestamp anomalies

**Detection**
- Audit log entries for timestamp presence
- Check timestamp precision distribution
- Monitor clock drift across services
- Alert on out-of-order timestamps
- Validate timezone consistency

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Timestamp requirements
- [Google SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/) - Observability best practices
- [AWS: Distributed Tracing](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html) - Timing correlation
- [OpenTelemetry](https://opentelemetry.io/) - Standardized timestamp handling
