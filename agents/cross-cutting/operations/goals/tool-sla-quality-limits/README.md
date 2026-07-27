# What Are the Most Common Tool SLA Quality Limit Failures in AI Agents?

**Tool SLA and quality limits fail when agents exceed tool-provided quality thresholds, when SLA targets are set but not monitored, when cascading failures from tool SLA breaches propagate upstream, or when tool quality degrades but agents don't detect or adapt.** The 5 SLA-quality patterns documented here cover the challenge of maintaining service-level agreements while using tools with their own SLAs — from monitoring tool SLA compliance through handling SLA breaches, to designing agents resilient to quality degradation. SLA failures are particularly insidious because they're invisible until an SLA is breached, by which point thousands of requests may have already seen degraded quality.

## Key Takeaways

- 5 patterns span SLA monitoring, breach handling, cascading failures, tool quality degradation, and availability SLAs.
- Tool SLA Breach and Tool Availability SLA Miss are most severe: when tool SLA is breached, agent SLA is also breached unless agent has fallback strategies.
- Tool Quality Degradation Undetected is second-order: tool quality silently degrades but agent doesn't detect it.
- SLA Monitoring Missing is architectural: SLAs are promised but not monitored, so breaches are discovered only by users.

## Scope

- **SLA Monitoring** — Tool SLA tracking, breach detection, alerting.
- **Quality Assurance** — Tool quality metrics, degradation detection, quality validation.
- **Availability** — Tool availability guarantees, uptime SLAs, downtime handling.
- **Cascading Impact** — Agent SLA depending on tool SLA, fallback strategies.

## When SLA Limits Matter

- Agents promise SLA to users; agent SLA depends on tool SLAs.
- Tool quality degradation should trigger agent fallback or degradation.
- Tools have published SLAs that may be breached; agent must handle breaches.

## Cross-Pattern Insight

SLA failures result from not explicitly tracking and responding to tool SLA status. Agents call tools assuming they meet SLA, but don't monitor whether they do. The mitigation is continuous SLA monitoring and adaptive degradation: measure tool availability and quality continuously, alert immediately when approaching SLA limits, and have fallback strategies for tools approaching SLA breach (use cached results, use alternative tool, degrade quality).

## Frequently Asked Questions

### How do you monitor tool SLA compliance?
Track tool availability percentage (uptime / total time), latency percentiles (p50, p95, p99), and error rate. Compare against published SLA. Alert if any metric approaches SLA breach threshold.

### What should an agent do if a tool SLA is breached?
If tool SLA is breached, agent SLA is also breached unless agent has fallback. Use cached results, switch to alternative tool, or degrade quality (use cheaper approximation, reduce result precision).

## Patterns

| Pattern | Mechanism |
|---|---|
| Tool SLA breach | Tool promises SLA but breaches it; agent SLA also breached |
| Tool availability SLA miss | Tool promises 99.9% uptime but is down more than promised |
| Tool quality degradation undetected | Tool quality silently degrades; agent doesn't detect until users complain |
| Tool latency SLA violation | Tool latency exceeds SLA; agent requests timeout |
| Cascading SLA impact | Tool SLA breach cascades to agent SLA; no fallback strategy |

**Total: 5 patterns**

## Related Goals

- [Real-Time Performance](../real-time-performance/) — latency SLA alignment
- [Reliability and Resilience](../reliability-and-resilience/) — availability SLA alignment
- [Observability Monitoring](../observability-monitoring/) — SLA monitoring infrastructure
