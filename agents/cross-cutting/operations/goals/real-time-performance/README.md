# Real-Time Performance

Failure patterns for AI systems requiring **low latency** and real-time responsiveness.

## Failure Patterns

| Pattern |
|---------|
| [Response Time SLA Breach](failures/response-time-sla-breach.md) |
| [Cold Start Latency](failures/cold-start-latency.md) |
| [Streaming Stalls](failures/streaming-stalls.md) |
| [Tool Call Latency Accumulation](failures/tool-call-latency-accumulation.md) |
| [Timeout Misconfiguration](failures/timeout-misconfiguration.md) |
| [Queue Backpressure](failures/queue-backpressure.md) |
| [Inference Latency Variance](failures/inference-latency-variance.md) |
| [Network Latency Blindness](failures/network-latency-blindness.md) |
| [Batching Delays](failures/batching-delays.md) |
| [Retry Latency Amplification](failures/retry-latency-amplification.md) |
| [Context Size Latency Impact](failures/context-size-latency-impact.md) |
| [Cascading Multi-Agent Latency](failures/cascading-multi-agent-latency.md) |

**Total: 12 patterns**

## Key Metrics

| Metric | Target | Critical |
|--------|--------|----------|
| P50 response time | <500ms | >1s |
| P99 response time | <2s | >5s |
| Time to first token | <200ms | >500ms |
| Tool call overhead | <100ms | >300ms |

## Cross-References

- [Cost Efficiency](../cost-efficiency/) - Latency vs cost tradeoffs
- [Tool Reliability](../tool-reliability/) - Tool call performance
- [Speech and Audio](../../../by-capability/speech-and-audio/) - Voice latency requirements
