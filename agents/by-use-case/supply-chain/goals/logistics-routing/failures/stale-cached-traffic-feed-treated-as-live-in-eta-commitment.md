# Stale Cached Traffic Feed Treated as Live in ETA Commitment

## Issue: A Logistics-Routing Agent Calls a Live Traffic/Transit-Time Tool to Compute a Delivery ETA It Commits to a Customer, the Tool Returns a Cached Response from Before a Major Disruption Event (Accident Closure, Severe Weather Routing Change) Took Effect, and the Agent Commits to an ETA Computed Against Conditions That No Longer Exist

**Frequency**: Occasional

**Symptoms**
- Customer-facing ETA commitments are missed by a margin consistent with a known disruption event (highway closure, severe weather) that was already in effect at the time the ETA was computed, discoverable by comparing the tool-call timestamp against the disruption's actual onset time
- Tool-call logs show the traffic/transit-time API returning a response with a data timestamp older than a disruption event the routing system's own disruption-monitoring feed had already flagged, while the agent's ETA-commitment narrative treats the returned transit time as current
- The mismatch clusters tightly around the time window immediately following a disruption event's onset, then disappears once the underlying traffic tool's cache naturally refreshes
- ETAs committed during the stale-cache window show a transit-time distribution consistent with pre-disruption conditions, while ETAs committed just before or after the window correctly reflect the disruption
- Customer complaints about missed ETAs cluster around shipments routed through the disrupted corridor during the affected window, with the routing agent's own commitment trail showing no acknowledgment of the disruption at the time of commitment

**Root Cause**
The traffic/transit-time tool's response is cached for performance reasons, and the cache invalidation is not tightly coupled to the routing system's own disruption-event feed; the routing agent receiving the tool's response has no way to distinguish a freshly computed transit time from a stale cached one unless the response explicitly carries and the agent explicitly checks a freshness timestamp against known disruption events. Because the cached response is syntactically identical to a fresh one, the agent's ETA-commitment logic -- which treats any successful tool response as authoritative -- proceeds to commit to a delivery window computed against conditions the disruption feed already knows are obsolete.

**Example**
```
A multi-vehicle accident closes a primary highway corridor, and the routing system's disruption-monitoring feed flags the closure within minutes
Logistics-routing agent's transit-time tool call for a shipment routed through that corridor returns a cached response computed before the closure, since the tool's cache TTL had not yet expired
Agent commits to a customer-facing ETA based on the pre-closure transit time, with no check of the response's cache timestamp against the disruption feed's flagged closure time
Shipment is delayed by several hours beyond the committed ETA; customer-service review traces the root cause to the routing agent having committed to an ETA computed against already-obsolete traffic conditions
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Errors in agentic tool-use pipelines commonly originate from stale tool outputs flowing into subsequent agent decisions without being flagged as outdated relative to other available system state | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| LLM agents applied to supply-chain operations are evaluated specifically on their ability to reconcile multiple data sources and reach consensus under disruption conditions, since failing to reconcile a stale source against a live disruption signal propagates directly into operational commitments | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |
| Disruption risk in supply networks requires real-time information integration, since decisions made on data that lags a disruption event by even a short window can materially understate the actual operational impact | [Disruption Risk in Supply Networks](https://arxiv.org/abs/2001.09842) |

**Contributing Factors**
- Traffic/transit-time tool's cache invalidation is not event-coupled to the routing system's own disruption-monitoring feed, leaving a window where cached and current conditions diverge
- Tool response does not surface a freshness timestamp prominently enough for the agent's ETA-commitment logic to check it against known disruption events before treating the returned transit time as current
- No automated reconciliation cross-checks ETA commitments against the disruption-monitoring feed in near-real-time, relying instead on the next natural cache refresh

---

## Mitigation Strategies

1. **Event-Coupled Cache Invalidation on Disruption Detection**: Invalidate the traffic/transit-time tool's cache immediately and synchronously for any corridor flagged by the disruption-monitoring feed, rather than relying on a time-based TTL that can lag a disruption event
2. **Mandatory Disruption-Feed Cross-Check Before Commitment**: Require the agent's ETA-commitment logic to explicitly cross-check the routed corridor against the disruption-monitoring feed before treating the traffic tool's returned transit time as authoritative, holding commitment on an active disruption match
3. **Freshness-Timestamp Gate**: Require the agent to check the traffic tool response's data timestamp against the most recent known disruption-event time for that corridor, blocking ETA commitment on a stale or ambiguous timestamp
4. **Real-Time ETA Re-Commitment on Active Disruptions**: For shipments already committed through a corridor that is subsequently flagged as disrupted, automatically trigger an ETA re-computation and customer re-notification rather than relying on the original, now-stale commitment to stand

### Metrics
- Rate of ETA commitments computed using a traffic-tool response with a data timestamp older than a known disruption event for that corridor
- Time lag between a disruption event being flagged and the traffic tool's cache reflecting the new conditions
- Missed-ETA rate for shipments routed through a disrupted corridor during the stale-cache window versus outside it

### Alerts
- ETA committed using a traffic-tool response with a data timestamp older than a flagged disruption event for that corridor → P1
- Traffic tool cache found to lag a disruption-feed flag by more than the defined freshness SLA during an active commitment → P2
- A disruption event is flagged with no corresponding cache-invalidation event firing for affected corridors within the defined SLA → P3

---

## References

- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
- [Disruption Risk in Supply Networks](https://arxiv.org/abs/2001.09842)
