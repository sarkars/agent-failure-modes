# Agent Timeout Cascade

## Issue
One agent in a multi-agent pipeline runs slow or hangs, and its caller times out and gives up waiting on it. Because that caller is itself being awaited by another agent upstream, its own timeout consumes most of the upstream agent's remaining budget, and the pattern repeats up the chain — each layer's timeout firing shortly before the one above it, so a single slow agent deep in the pipeline produces a wave of timeouts that appears to hit the entire system simultaneously.

**Frequency**: Common

**Symptoms**
- Multiple unrelated-looking agents timing out within seconds of each other during an incident
- Timeout errors that trace back, layer by layer, to a single slow or hung agent at the bottom of a call chain
- Retry attempts from multiple layers landing on the same already-overloaded downstream agent simultaneously, worsening the slowdown
- Overall pipeline latency spiking to just under the sum of every layer's individual timeout, rather than failing fast
- Incident timelines showing timeout log entries firing in a strict, chain-like sequence from deepest layer outward

## Root Cause
In a nested multi-agent call chain (orchestrator -> planner -> worker -> tool-calling sub-agent), each layer typically sets its own timeout independently, often without knowledge of how much time budget remains from the original caller's perspective. When the deepest agent stalls, it consumes its full local timeout before failing, leaving the layer above it with less time than it assumed it had; that layer then times out too, but only after also burning its own full timeout duration on top. Because timeouts aren't budgeted from a shared deadline propagated down the call chain, each layer effectively double-counts wait time, and layers with automatic retries multiply the effect further by re-invoking an already-struggling downstream agent instead of failing fast.

## Example
```
A document-processing pipeline has four nested layers, each with its own
independently configured timeout:

  Orchestrator Agent (timeout: 60s)
    -> Planning Agent (timeout: 45s)
         -> Extraction Agent (timeout: 30s)
              -> OCR Tool-Calling Agent (timeout: 20s)

10:02:00 - A request enters the Orchestrator, which calls the Planning
           Agent, which calls the Extraction Agent, which calls the OCR
           Agent to process a scanned PDF.
10:02:00 - The OCR provider is degraded and the call hangs.
10:02:20 - OCR Agent hits its 20s timeout, returns an error to Extraction
           Agent. Extraction Agent's retry logic fires, re-calling the
           still-degraded OCR provider.
10:02:40 - The retry also times out at 20s (cumulative 40s elapsed).
           Extraction Agent, now at 40s of its own 30s budget, has
           already breached its timeout and returns an error to Planning
           Agent -- but the error surfaces 10s late because the retry
           was allowed to run past the parent's deadline.
10:02:45 - Planning Agent, unaware its child was already over-budget,
           times out at its own 45s mark and returns an error upstream.
10:03:00 - Orchestrator times out at 60s and returns a generic failure to
           the user, roughly 60 seconds after a problem that itself only
           needed 20 seconds to become apparent.
```

## Statistics
| Finding | Context |
|---------|---------|
| Nested timeout misconfiguration is implicated in an estimated 20-30% of "slow failure" incidents in layered agent pipelines | Typical range observed in production incident reviews |
| Deep call chains (4+ layers) without deadline propagation commonly take 2-4x longer to surface a failure than the deepest layer's own timeout | Estimated from instrumented pipeline latency traces |
| Adopting shared-deadline propagation (a single budget passed and decremented at each layer) reduces total failure-surfacing time by an estimated 60-75% | Reported range across teams that added deadline propagation |

## Mitigations
1. **Deadline propagation**: Pass a single absolute deadline (or remaining-budget value) down through every layer of the call chain, and have each layer's timeout be derived from that shared deadline rather than independently configured.
2. **Fail-fast on child timeout**: When a directly-called agent times out, propagate the failure upward immediately rather than retrying at every layer, reserving retries for a single, deliberately-chosen layer.
3. **Retry budget coordination**: Centralize retry policy so that only one layer in a chain retries a given failure, preventing multiple layers from independently re-invoking an already-struggling downstream agent.
4. **Timeout margin enforcement**: Require each layer's configured timeout to be strictly shorter than its caller's remaining budget by a defined margin, catching misconfigured timeout chains at deploy time via a lint or config check.
5. **Circuit breaking on downstream degradation**: Once a downstream agent has failed or timed out repeatedly within a short window, short-circuit further calls to it for a cooldown period instead of letting every upstream layer independently discover the same degradation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| timeout_cascade_depth | Number of chained layers that timed out in sequence for a single request | Alert if > 1 |
| time_to_failure_surfaced | Wall-clock time from request start to the failure reaching the caller | Alert if > 1.5x the deepest layer's timeout |
| duplicate_retry_on_same_downstream | Count of retries issued by multiple layers against the same downstream agent for one logical request | Alert if > 1 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Timeout cascade detected | timeout_cascade_depth >= 2 for a single request trace | High | Page on-call, check deepest failing agent's health, review deadline propagation |
| Retry storm on degraded downstream | Multiple layers retrying the same downstream agent within a short window | Medium | Trigger circuit breaker, throttle retries at all but one layer |

## Related Patterns
- [Agent Resource Contention](./agent-resource-contention.md) - contention-driven slowdowns at a shared resource are a common root trigger for a timeout cascade
- [Agent Priority Inversion](./agent-priority-inversion.md) - a stalled low-priority holder's unbounded wait can be the initiating slow layer in a cascade
- [Inter-Agent Latency Imbalance](./inter-agent-latency-imbalance.md) - persistent latency imbalance between agents increases the likelihood that one layer will trigger cascading timeouts in others
