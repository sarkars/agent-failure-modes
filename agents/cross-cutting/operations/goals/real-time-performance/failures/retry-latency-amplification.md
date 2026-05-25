# Retry Latency Amplification

## Issue: Retries Multiply Latency Instead of Improving Reliability

**Frequency**: Common

**Symptoms**
- Failed requests take 3-10x longer than successful ones
- Retry storms during outages
- Latency spikes correlated with error rates
- User waits for all retries before seeing error

**Root Cause**
Automatic retries improve reliability but amplify latency. Each retry adds full request latency. Without proper backoff, retries happen immediately, multiplying load during failures.

**Example**
```
Retry configuration: 3 attempts, no backoff

Successful request: 500ms

Failed request (all retries fail):
- Attempt 1: 500ms → timeout
- Attempt 2: 500ms → timeout  
- Attempt 3: 500ms → timeout
- Return error
Total: 1500ms (3x latency for failure)

With exponential backoff:
- Attempt 1: 500ms → timeout
- Wait 1s
- Attempt 2: 500ms → timeout
- Wait 2s
- Attempt 3: 500ms → timeout
Total: 4500ms (9x latency!)
```

**Contributing Factors**
- Too many retry attempts
- No backoff or excessive backoff
- Retrying non-retryable errors
- No circuit breaker
- Retries at multiple layers (client + server)

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Failed request latency | Guaranteed failure | < 2x success | > 5x |
| Retry storm | 50% error rate | Backoff applied | Immediate retries |
| Circuit breaker | Sustained failure | Fast fail | Keep retrying |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Retry amplification factor | < 2x | failed_latency / success_latency |
| Retry attempt distribution | Decreasing | Histogram of attempts |
| Circuit breaker trigger rate | > 0 when needed | Triggers during outage |

---

## Mitigation Strategies

### Prevention
1. **Limited retries**: Max 2-3 attempts
2. **Exponential backoff with jitter**: Spread retry load
3. **Circuit breakers**: Stop retrying during outages
4. **Retry budgets**: Limit retry percentage of traffic
5. **Fast fail for non-retryable**: Don't retry 4xx errors

### Smart Retry Strategy
```python
class SmartRetry:
    def __init__(self, max_attempts=3, base_delay=0.1):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.circuit_breaker = CircuitBreaker()
    
    async def execute(self, operation, timeout=5.0):
        if self.circuit_breaker.is_open():
            raise FastFailError("Circuit open")
        
        deadline = time.time() + timeout
        
        for attempt in range(self.max_attempts):
            remaining = deadline - time.time()
            if remaining <= 0:
                raise TimeoutError("Retry budget exhausted")
            
            try:
                return await asyncio.wait_for(
                    operation(), 
                    timeout=min(remaining, timeout / self.max_attempts)
                )
            except RetryableError as e:
                if attempt < self.max_attempts - 1:
                    delay = self.base_delay * (2 ** attempt)
                    delay += random.uniform(0, delay * 0.1)  # Jitter
                    await asyncio.sleep(min(delay, remaining))
                else:
                    self.circuit_breaker.record_failure()
                    raise
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `retry.amplification.factor` | > 3x |
| `retry.storm.rate` | > 20% of traffic |
| `circuit_breaker.open.duration` | > 5min |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Retry Storm | retry_rate > 30% | P1 |
| Excessive Amplification | factor > 5x | P2 |
| Circuit Breaker Stuck | open > 10min | P1 |

---

## References

- [Retry Best Practices](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
