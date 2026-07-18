# Per-Tool Burst Rate Exceeded

## Issue
A tool enforces a short-window burst limit (e.g., no more than 5 requests in any 1-second window) that is much tighter than its sustained rate limit (e.g., 300 requests/minute). An agent orchestrating parallel sub-agent fan-out — say, dispatching 15 research sub-agents that each immediately call the same search tool the instant they spawn — blows through the burst ceiling in the first second even though the resulting sustained average is comfortably under the per-minute quota.

**Frequency**: Common

**Symptoms**
- 429s appear in the very first second of a fan-out burst, then stop once the burst spreads out, even though total requests/minute stays well under the documented sustained limit
- Rejections correlate with sub-agent spawn events, not with overall traffic volume
- The vendor's dashboard shows the account is at 5% of its monthly/daily quota when the burst rejections occur
- Staggering identical total request volume over a few seconds instead of firing it at once eliminates the failures entirely
- Error responses reference a short window (e.g., "rate limit: 5 req/sec exceeded") distinct from the documented per-minute or per-day limit

## Root Cause
Vendors commonly layer multiple rate-limit windows on the same API key — a tight burst window to protect against thundering-herd spikes, and a looser sustained window for overall capacity planning. Agent orchestration patterns that launch parallel sub-agents synchronously (all fire their first tool call within milliseconds of each other) are exactly the shape burst limits are designed to catch, but agent developers typically only account for the advertised sustained limit and have no code path that paces or jitters the initial burst of a fan-out.

## Example
```
A "MarketScan" orchestrator agent spawns 12 sub-agents in parallel to research 12 competitors, each immediately calling the WebSearchAPI connector as its first action.

WebSearchAPI's documented limit is "300 requests per minute," which the orchestrator's design assumed was the only constraint — 12 requests is nowhere near 300.
WebSearchAPI also enforces an undocumented (or buried-in-fine-print) burst cap of 5 requests per second per key.
All 12 sub-agents fire their first call within the same 200ms window at task start.
Requests 6-12 receive 429 "burst limit exceeded" within the first second.
The orchestrator's retry logic waits a fixed 60 seconds before retrying (tuned for the per-minute limit), so 7 of 12 competitor research streams stall for a full minute even though the burst window itself clears in under 2 seconds.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 30-40% of third-party APIs enforce a separate short-window burst limit in addition to a sustained rate limit | Common in agent tool integrations against search, payments, and enrichment APIs |
| Synchronous parallel sub-agent fan-out of 10+ concurrent first-calls triggers burst-limit rejections in the majority of integrations lacking explicit start-time jitter | Observed in multi-agent orchestration testing |
| Adding 50-200ms of randomized jitter to sub-agent tool-call start times eliminates the large majority of burst-limit 429s without materially affecting total task latency | Typical outcome of jitter-based remediation |

## Mitigations
1. **Jitter sub-agent start times**: When spawning N parallel sub-agents that will each immediately call the same tool, stagger their first call with small randomized delays (e.g., 0-300ms) so they don't all land in the same sub-second window.
2. **Token-bucket the fan-out at the orchestrator level**: Route all calls to a given tool through a shared client-side token bucket sized to the tool's known burst limit, so the orchestrator enforces pacing locally instead of relying on the vendor to reject and the agent to recover.
3. **Discover and document both limit tiers**: When integrating a new tool, explicitly test for and record both the sustained and burst limits (many vendors bury the burst limit in fine print or omit it from primary docs), and configure separate pacing logic for each.
4. **Use burst-aware backoff, not sustained-limit backoff**: When a 429 is attributable to a burst limit (check the error body/headers for window hints), back off for a duration matched to the burst window (often under 2 seconds), not the much longer sustained-limit backoff.
5. **Batch where the tool supports it**: If the tool offers a batch/bulk endpoint, prefer it over N parallel single-item calls for fan-out scenarios — this sidesteps burst limits entirely by making one request represent many logical operations.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.burst_429_count` | 429s occurring within 2 seconds of a fan-out spawn event | Alert if more than 3 in any single fan-out batch |
| `tool.first_call_jitter_ms` | Time spread between the first and last initial call across sub-agents in a fan-out | Alert if median spread is under 50ms for fan-outs of 10+ |
| `tool.burst_vs_sustained_utilization` | Ratio of burst-window usage to sustained-window usage at time of rejection | Flag when burst utilization is near 100% while sustained utilization is under 10% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Burst limit hit during fan-out | `burst_429_count` > 3 correlated with a sub-agent spawn event | Warning | Add/verify start-time jitter or client-side token bucket for the tool |
| Repeated burst rejection despite low sustained usage | Burst 429s recur across multiple fan-outs while daily/monthly quota utilization stays under 20% | Warning | Confirm burst limit value with vendor and update local pacing config |

## Related Patterns
- [Per-Tool Requests Per Minute Exceeded](./per-tool-requests-per-minute-exceeded.md) - the sustained-window sibling of this short-window constraint; agents often tune for one and miss the other
- [Per-Tool Concurrent Connections Exceeded](./per-tool-concurrent-connections-exceeded.md) - fan-out patterns that trigger burst limits often simultaneously trip concurrent-connection limits
- [Rate Limit Grace Period Missing](./rate-limit-grace-period-missing.md) - burst windows are especially likely to have little to no grace period, making backoff timing critical
