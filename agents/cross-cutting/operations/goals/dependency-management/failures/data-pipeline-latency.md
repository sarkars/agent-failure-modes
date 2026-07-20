# Data Pipeline Latency

## Issue
An agent that reads from a multi-stage pipeline treats the data it receives as current, but each stage (ingestion, normalization, enrichment, batching, indexing) adds its own processing delay, and those delays compound. By the time the agent acts — approving a trade, flagging inventory as low, answering "what is the current status" — the data reflects the world as it was minutes or hours earlier, not as it is now, and nothing in the agent's context signals how stale the value actually is.

**Frequency**: Very Common

**Symptoms**
- Agent confidently reports a state ("stock level: 42 units") that was already wrong by the time it was retrieved
- Decisions based on "latest" data are contradicted by the source system when checked directly
- End-to-end latency grows gradually over weeks as more enrichment/processing stages are added, without any single change looking like a regression
- No timestamp or staleness indicator is exposed to the agent alongside the data value itself
- Incidents traced back to "the pipeline was technically working, just slow" rather than an outright failure

## Root Cause
Each pipeline stage is typically designed and monitored for its own latency in isolation (a batching stage optimized for throughput, an enrichment stage calling a slow third-party API, an indexing stage on a fixed schedule), and no one owns the end-to-end latency budget across the whole chain. Latency composes additively (or worse, under load) across stages, so a pipeline where every individual stage looks "fast enough" in isolation can still produce data that is many minutes stale by the time it reaches the agent. Because the agent's interface to the data is usually just a value with no attached freshness metadata, the agent has no way to distinguish "this is current" from "this is however old the slowest path through the pipeline made it," so it treats all reads as equally fresh.

## Example
```
A logistics agent answers "where is shipment SH-88213 right now" by querying
a "current_location" table populated by a pipeline: GPS pings (real-time) ->
message queue (avg 5s lag) -> batch enrichment job that geocodes coordinates
into addresses (runs every 10 min) -> materialized view refresh (runs every
15 min) -> agent's query layer.

Under normal conditions the end-to-end lag is roughly 20-25 minutes, which
the team considered acceptable when the pipeline was designed for
warehouse-to-warehouse tracking.

The agent is later repurposed to answer live customer support questions:
"is my driver still 10 minutes away?" A customer messages support at 2:47pm
when the driver has already arrived and unloaded at 2:44pm. The agent, reading
the materialized view last refreshed at 2:35pm, reports "estimated arrival in
9 minutes," directly contradicting what the customer can see out their window.
The pipeline never failed -- every stage processed every message -- but the
compounded latency made the data wrong for the new use case.
```

## Statistics
| Finding | Context |
|---------|---------|
| End-to-end pipeline latency in agent-facing data systems is commonly underestimated by 3-5x when each stage is assessed only in isolation | Typical range observed in latency budget audits |
| An estimated 30-40% of "wrong answer" incidents in read-heavy agent workflows trace back to staleness rather than incorrect logic | Estimated from production incident classification |
| Adding explicit freshness/staleness metadata to agent-facing reads reduces staleness-driven incorrect decisions by an estimated 50-70% | Reported range across teams that added freshness SLAs |

## Mitigations
1. **End-to-end latency budget and ownership**: Define a single target for total pipeline latency from source event to agent-visible data, and require every stage owner to justify their contribution against that budget, not just their own stage's throughput.
2. **Freshness metadata on every read**: Attach a `data_as_of` timestamp to every value the agent reads, and require the agent's prompt/logic to reason about staleness explicitly rather than assuming currency.
3. **Staleness-aware fallback**: When freshness exceeds a use-case-specific threshold, have the agent fall back to a direct real-time query or explicitly flag the answer as potentially stale, rather than presenting it with false confidence.
4. **Per-stage latency SLOs with alerting**: Instrument each pipeline stage with a latency SLO and alert when any stage's contribution grows, catching gradual creep before it compounds into a customer-visible problem.
5. **Use-case-specific pipeline review on repurposing**: When an existing data pipeline is repurposed for a new, more time-sensitive use case, re-evaluate whether its designed-for latency budget still fits, rather than assuming "it already works."

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| end_to_end_pipeline_latency | Time from source event to data being agent-visible | Alert if > use-case-defined freshness SLA |
| per_stage_latency_contribution | Latency added by each individual pipeline stage | Alert if any stage's contribution grows > 25% week-over-week |
| stale_read_rate | Fraction of agent reads where data_as_of exceeds the freshness threshold | Alert if > 5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| End-to-end latency SLA breach | Total pipeline latency exceeds the defined freshness SLA for the consuming use case | High | Page pipeline owner, flag affected agent responses as potentially stale |
| Gradual latency creep | Per-stage latency trending upward over a rolling multi-week window | Medium | Schedule latency budget review before it breaches SLA |

## Related Patterns
- [Data Pipeline Backpressure Unhandled](./data-pipeline-backpressure-unhandled.md) - unhandled backpressure is an acute cause of the same staleness this pattern describes as a chronic condition
- [Data Lineage Loss](./data-lineage-loss.md) - without lineage and timestamps, staleness cannot even be diagnosed after the fact
- [Integration Timeout Mismatch](./integration-timeout-mismatch.md) - mismatched timeouts across integrated systems are one common contributor to compounding pipeline latency
