# Queue Backpressure

## Issue: Request Queues Build Up Causing Latency Spiral

**Frequency**: Occasional

**Symptoms**
- Latency increases over time under load
- Old requests processed after fresher ones would be better
- System doesn't recover after load spike
- Memory pressure from queued requests

**Root Cause**
When arrival rate exceeds processing rate, queues grow. Each queued request adds latency for subsequent requests. Without backpressure mechanisms, queues grow unbounded, and latency spirals.

**Example**
```
Load spike scenario:

Normal: 100 req/s capacity, 80 req/s arriving
- Queue depth: ~0
- Latency: 500ms

Spike: 100 req/s capacity, 150 req/s arriving
Minute 1: Queue depth 3000, latency 30s
Minute 2: Queue depth 6000, latency 60s
Minute 3: Queue depth 9000, latency 90s (timeout cascade)

Problem: 90s old requests still processing when
         user has already abandoned and retried.
```

**Contributing Factors**
- No queue depth limits
- No request age/freshness checking
- Missing load shedding
- No autoscaling or slow autoscaling
- Retries without backoff adding to queue

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Sustained overload | 150% capacity for 5min | Graceful shedding | Queue spiral |
| Recovery test | Spike then normal | < 1min recovery | Doesn't recover |
| Request freshness | Queue old requests | Shed stale | Process 60s old request |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Queue depth | < 100 | Current queue size |
| Queue wait time | < 5s | Time in queue |
| Shed rate during overload | > 20% | dropped / arriving |

---

## Mitigation Strategies

### Prevention
1. **Queue limits**: Reject when queue exceeds threshold
2. **Request deadlines**: Drop requests past their deadline
3. **Load shedding**: Reject percentage of requests under load
4. **LIFO queuing**: Process newest requests first (for some use cases)
5. **Autoscaling**: Scale capacity to match demand

### Backpressure Implementation
```python
class BackpressureQueue:
    def __init__(self, max_depth=100, max_age_seconds=30):
        self.max_depth = max_depth
        self.max_age = max_age_seconds
        self.queue = []
    
    def enqueue(self, request):
        # Shed if queue too deep
        if len(self.queue) >= self.max_depth:
            return False, "queue_full"
        
        # Clean stale requests
        self.queue = [r for r in self.queue 
                      if r.age() < self.max_age]
        
        self.queue.append(request)
        return True, None
    
    def dequeue(self):
        while self.queue:
            request = self.queue.pop(0)
            if request.age() < self.max_age:
                return request
            # Silently drop stale
        return None
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `queue.depth` | > 100 |
| `queue.wait.p95` | > 10s |
| `queue.shed.rate` | > 10% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Queue Depth Critical | depth > 500 | P1 |
| Queue Spiral | depth increasing for 5min | P1 |
| High Shed Rate | shed > 30% | P2 |

---

## References

- [Backpressure in Distributed Systems](https://mechanical-sympathy.blogspot.com/2012/05/apply-back-pressure-when-overloaded.html)
- [Load Shedding Patterns](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
