# SLA Availability Not Met

## Issue
A tool's actual uptime falls short of its advertised availability SLA (e.g., "99.9% uptime" translating to roughly 43 minutes of allowed downtime per month, but real outages exceeding that budget). The agent, built with no fallback path because the SLA implied outages would be rare and brief, treats every outage as an unexpected, unhandled condition — retrying blindly, failing the entire user-facing workflow, or queuing work indefinitely — rather than having a designed response for a scenario the SLA math said should barely ever happen but that occurs often enough in practice to matter.

**Frequency**: Common

**Symptoms**
- The tool experiences outages more frequently or for longer durations than its advertised SLA would predict over a given period
- The agent has no fallback, degraded mode, or circuit breaker for the dependency, because the team designed around the assumption that the SLA made extended handling unnecessary
- User-facing failures during an outage window are total (complete workflow failure) rather than degraded (reduced functionality but still operating)
- SLA credits offered by the vendor after an outage don't come close to covering the actual business impact of the downtime, since SLA credit terms are typically capped at a small percentage of the fees paid
- Multiple unrelated internal workflows all fail simultaneously during the same vendor outage window, since they all shared the same unhandled dependency

## Root Cause
Advertised SLA percentages describe an aggregate historical or contractual commitment, not a guarantee about the distribution of outages — a vendor can meet "99.9% over the year" while still having one outage lasting several hours in a single month, and many outages don't count against the SLA at all due to exclusions for "scheduled maintenance," "force majeure," or dependencies on third parties the vendor itself relies on. Teams often translate a headline SLA percentage into an assumption that failures will be rare enough not to warrant investment in fallback logic, when the actual distribution of outages (which can cluster, or be much longer than the SLA's implied average outage length) makes that assumption unsafe. Because building genuine failover (multi-vendor redundancy, degraded-mode operation) is expensive, it's frequently deprioritized based on an SLA number that wasn't actually a promise about worst-case outage severity.

## Example
```
1. A customer support agent uses a third-party ticketing platform's API, advertised at
   "99.95% uptime SLA," to create, update, and close support tickets, with no fallback
   path since the team judged sub-1-hour-per-year expected downtime as not worth
   building redundancy for.
2. The ticketing platform experiences a single major outage lasting 6 hours due to a
   cascading failure in one of its own upstream dependencies (excluded from their SLA
   calculation as a "third-party service disruption").
3. During the outage, every attempt by the agent to create or update a ticket fails;
   the agent's retry logic retries indefinitely with exponential backoff, queuing an
   ever-growing backlog of failed operations in memory with no persistent fallback store.
4. When the agent process restarts for an unrelated reason mid-outage, the entire
   in-memory backlog of queued ticket updates is lost.
5. Support operations are completely blind for 6 hours; when the platform recovers,
   roughly 200 customer interactions during the outage window have no ticket record
   at all, discovered only when customers follow up and reference conversations that
   don't exist in the system.
6. The vendor's SLA credit for the outage amounts to a small fraction of one month's
   subscription fee, far short of the operational and reputational cost of the 6-hour
   blackout.
```

## Statistics
| Finding | Context |
|---------|---------|
| A single SLA-percentage figure can be met on an annual basis while still including individual outages substantially longer than the implied "typical" outage duration a customer might assume from the headline number | Because SLA math is an aggregate over the measurement period, not a cap on any single incident's length |
| SLA credit terms in most vendor contracts are capped at a modest percentage of monthly or annual fees, typically far below the actual business cost of a significant outage for dependent workflows | Consistent with SLA credits functioning as a goodwill gesture rather than a true damages remedy |
| Systems with a designed degraded-mode fallback recover functional capability during vendor outages substantially faster than systems with no fallback, which typically remain fully blocked for the outage's entire duration | By design, since a fallback provides continued (if reduced) operation instead of total dependency |

## Mitigations
1. **Design for outages longer than the SLA implies, not shorter**: Assume any single outage could be hours, not minutes, regardless of the aggregate SLA percentage, and build fallback logic sized for that realistic worst case rather than the statistical average.
2. **Durable local queuing, not in-memory retry**: Persist failed operations to durable storage (a local queue, a database) rather than holding retry state only in memory, so an agent restart during an outage doesn't lose the backlog.
3. **Degraded-mode operation for critical workflows**: For workflows where availability really matters, design an explicit degraded mode (e.g., local caching of recent state, manual-entry fallback) that keeps the workflow partially functional during a vendor outage rather than fully blocked.
4. **Multi-vendor redundancy for the highest-criticality dependencies**: For capabilities where an outage causes severe business impact, evaluate whether a secondary vendor or self-hosted fallback is justified, despite the added cost and complexity.
5. **Track actual observed availability independently of the vendor's self-reported SLA compliance**: Measure uptime from the agent's own perspective (based on actual call success/failure) rather than trusting the vendor's own SLA compliance reporting, since vendor exclusions can make their reported number look better than the customer's lived experience.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.observed_availability_pct` | Actual measured availability from the agent's own call success rate, independent of vendor-reported SLA compliance | Alert when trailing 30-day observed availability falls below the contracted SLA figure |
| `tool.outage_duration_current_incident` | Duration of the current ongoing outage, tracked from first detected failure | Alert when duration exceeds the typical single-incident allowance implied by the SLA |
| `fallback.activation_rate` | Rate at which the agent's fallback/degraded mode is activated due to primary tool unavailability | Track as an indicator of how often the fallback path is being exercised in practice |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Extended outage detected | `outage_duration_current_incident` exceeds 15-30 minutes with no recovery | Critical | Activate degraded-mode fallback, begin durable queuing of failed operations |
| Trailing availability below contracted SLA | `observed_availability_pct` (30-day) falls below the vendor's contracted commitment | High | Document for SLA credit claim, reassess fallback investment given actual observed reliability |

## Related Patterns
- [Latency Sla Violation](./latency-sla-violation.md) - a related SLA-gap failure focused on response time rather than availability
- [Degraded Sla Not Communicated](./degraded-sla-not-communicated.md) - covers the case where the tool stays technically "available" but silently degrades quality instead of going down outright
- [Webhook Delivery Guarantee Not Enforced](../../tool-integration-limits/failures/webhook-delivery-guarantee-not-enforced.md) - availability gaps on the receiving or sending side are a common proximate cause of dropped webhook deliveries
