# Rate Limit Mishandling

## Issue: Agent Fails or Degrades When Hitting API Rate Limits

**Frequency**: Common

**Symptoms**
- Agent crashes on 429 errors
- Aggressive retries worsen rate limiting
- No backoff strategy implemented
- Queue builds up during rate limit windows
- User requests timeout waiting for capacity

**Root Cause**
LLM APIs enforce rate limits (requests/minute, tokens/minute). When agents hit these limits without proper handling, they either crash, retry aggressively (making things worse), or queue indefinitely. Production agents need graceful degradation, exponential backoff, and capacity planning.

**Example**
```
Scenario: Traffic spike hits rate limits

12:00 - Normal traffic: 50 req/min (limit: 100)
12:15 - Spike begins: 150 req/min
12:16 - Rate limit hit: 429 errors returned
        
Poor handling:
  Agent: Immediate retry on 429
  Result: More 429s, exponential problem
  Agent: Retry again immediately
  Result: Account flagged, longer timeout
  
Better handling:
  Agent: Exponential backoff (1s, 2s, 4s...)
  Agent: Queue excess requests
  Agent: Shed load if queue too deep
  Agent: Alert ops team
```

**Contributing Factors**
- No retry strategy implemented
- Missing exponential backoff
- No request queuing
- Ignoring rate limit headers
- No capacity planning
- Single API key bottleneck

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Rate limit hit | Exceed limit | Graceful backoff | Crash or tight loop |
| Sustained pressure | 2x limit for 5 min | Queue + backoff | Timeout or crash |
| Recovery | Limit lifted | Resume normally | Stuck state |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| 429 recovery rate | >99% | Successful retry / 429s |
| Backoff compliance | 100% | Follows backoff curve |
| Queue depth | <100 | Max pending requests |

---

## Mitigation Strategies

### Prevention
1. **Exponential backoff**: 1s, 2s, 4s, 8s... with jitter
2. **Rate limit headers**: Respect `Retry-After`, `X-RateLimit-*`
3. **Request queuing**: Buffer requests during limits
4. **Load shedding**: Reject excess when queue full
5. **Multiple API keys**: Distribute across keys
6. **Capacity planning**: Stay under 80% of limits

### Architecture Pattern
```
Request → [Queue] → [Rate Limiter] → LLM API
              ↓           ↓
         [Shed if    [Backoff on
          full]       429]
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `rate_limit.hits` | >10/min |
| `queue.depth` | >50 |
| `retry.count` | >3 per request |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Rate Limit Storm | >50 429s/min | P1 |
| Queue Overflow | Depth >100 | P2 |
| Sustained Limiting | >5 min at limit | P2 |

---

## References

- [OpenAI: Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Anthropic: Rate Limits](https://docs.anthropic.com/en/api/rate-limits)
