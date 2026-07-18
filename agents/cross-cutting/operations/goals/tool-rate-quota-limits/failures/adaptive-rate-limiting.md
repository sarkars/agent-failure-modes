# Adaptive Rate Limiting

## Issue
Some tool vendors don't publish a fixed rate limit at all — instead they throttle dynamically based on backend load, shedding traffic more aggressively during peak hours or incident windows. An agent that learned "this API allows ~50 requests/minute" from yesterday's behavior has no way to know that the vendor has silently tightened the effective limit to 10 requests/minute right now, so it keeps firing at its old cadence and racks up a string of 429s it can't explain.

**Frequency**: Common

**Symptoms**
- 429 rate-limit errors appear and disappear over the course of a day with no code or traffic change on the agent's side
- The same call pattern that worked fine an hour ago now fails consistently
- Retry-After values (when present) fluctuate wildly between requests, sometimes 1 second, sometimes 60
- Agent logs show no correlation between the agent's own request volume and the failure rate — the limit seems to move on its own
- Support tickets to the vendor get "we adjust limits based on system load" as the explanation, with no published schedule

## Root Cause
The vendor's gateway implements load-shedding or adaptive throttling (often via a token-bucket or leaky-bucket algorithm whose refill rate is itself a function of aggregate backend health) rather than a static per-key quota. Because the effective limit is not exposed as a documented constant, agents built with a hardcoded assumption ("this tool allows N req/s") have no signal to detect that the ceiling moved, and naive fixed-cadence request loops have no mechanism to discover the new ceiling except by colliding with it repeatedly.

## Example
```
09:00 — Agent's "ResearchBot" sub-agent calls the WebSearchAPI connector at a steady 20 requests/minute, matching the documented "typical" limit from the vendor's marketing page.
09:00–13:00 — Works fine, zero errors.
13:15 — WebSearchAPI's backend experiences elevated load from other tenants; the vendor's edge gateway drops the effective per-key limit to 6 requests/minute without any status-page notice.
13:16 — Agent's next batch of 20 requests/minute produces 14 consecutive 429s.
13:16 — Agent's retry logic re-issues the failed calls immediately (no backoff tuned for adaptive limits), which are also rejected, because it is still pacing at the stale 20/min assumption.
13:20 — Orchestrator marks the WebSearchAPI tool "degraded" and fails the whole research task, even though 6 requests/minute of throughput was still available the entire time.
```

## Statistics
| Finding | Context |
|---------|---------|
| Adaptive/load-based throttling is used by an estimated 15-25% of high-traffic third-party APIs agents commonly integrate with (search, LLM inference, data enrichment) | Observed across production agent deployments |
| Agents without adaptive-limit detection see 3-5x more 429 errors during vendor peak-load windows than during off-peak, despite identical agent-side request volume | Typical of fixed-cadence integrations |
| Median time-to-recovery after an adaptive throttle event is 4-12 minutes when agents passively retry, vs under 60 seconds when they actively probe for the new ceiling | Comparison of naive vs adaptive backoff strategies |

## Mitigations
1. **AIMD-style self-tuning throughput**: Treat the effective rate limit as unknown and continuously estimated. Increase request cadence additively on success streaks, cut it multiplicatively (e.g., halve) on any 429, similar to TCP congestion control, so the agent converges on the vendor's current real ceiling instead of a stale assumption.
2. **Header-driven probing when available**: If the tool exposes any rate-limit headers (even inconsistently), parse them on every response and use the most recent value rather than a cached constant — treat the header as the source of truth, not the documentation.
3. **Circuit breaker with gradual re-open**: On sustained 429s, open a circuit breaker that stops all traffic to the tool, then re-probe with a single low-cost request every 30-60 seconds and only resume full traffic after several consecutive successes, rather than resuming at the old cadence immediately.
4. **Decouple task success from tool cadence**: Design orchestration so a slower-than-expected tool degrades task latency rather than failing the task outright — queue and retry at the discovered rate instead of treating adaptive throttling as a hard tool failure.
5. **Vendor load-window telemetry correlation**: If the vendor publishes a status page or incident feed, poll it and correlate throttle events with published load windows to distinguish adaptive throttling from an outage, so alerting and retries can be tuned differently for each.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.effective_rate_estimate` | Agent's current AIMD-estimated safe request rate for the tool | Alert if estimate drops below 30% of its 7-day rolling median |
| `tool.429_rate` | Fraction of calls to the tool returning 429 over a 5-minute window | Alert if sustained above 10% for more than 5 minutes |
| `tool.rate_estimate_volatility` | Standard deviation of the rate estimate over a rolling hour | Alert if volatility exceeds 2x the 7-day baseline, indicating vendor instability |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Adaptive throttle detected | 429 rate crosses 10% while agent-side request volume is flat or declining | Warning | Trigger AIMD backoff, notify on-call if sustained over 15 minutes |
| Rate estimate collapse | Effective rate estimate falls below 20% of baseline for over 10 minutes | Critical | Open circuit breaker, page on-call, check vendor status page |

## Related Patterns
- [Rate Limit Header Not Honored](./rate-limit-header-not-honored.md) - adaptive limits are especially painful when the agent also ignores the headers that could reveal the current ceiling
- [Rate Limit Grace Period Missing](./rate-limit-grace-period-missing.md) - both patterns involve a tight failure loop when the agent doesn't back off correctly after a 429
- [Per-Tool Requests Per Minute Exceeded](./per-tool-requests-per-minute-exceeded.md) - a fixed-limit variant of the same underlying symptom, without the added complication of a moving target
