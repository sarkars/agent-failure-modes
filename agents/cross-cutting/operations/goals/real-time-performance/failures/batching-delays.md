# Batching Delays

## Issue: Request Batching Adds Unacceptable Wait Time

**Frequency**: Occasional

**Symptoms**
- Low-traffic periods have higher latency than high-traffic
- Requests wait for batch to fill
- Latency bimodal: fast (batch ready) vs slow (waiting)
- First request after idle is slow

**Root Cause**
Batching improves throughput but adds latency. Systems wait for batch to fill before processing. In low-traffic scenarios, requests wait for a batch that never fills, adding unnecessary delay.

**Example**
```
Batch configuration: size=8, timeout=100ms

High traffic (good):
- 8 requests arrive in 20ms
- Batch processes immediately
- Latency: 500ms (inference only)

Low traffic (bad):
- 1 request arrives
- Waits 100ms for batch timeout
- Processes alone
- Latency: 600ms (100ms wait + 500ms inference)

Result: 20% latency penalty during low traffic
```

**Contributing Factors**
- Fixed batch timeout too long
- Batch size too large for traffic
- No adaptive batching
- Batching applied where not needed
- Traffic pattern not analyzed

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Low traffic latency | 1 req/min | < 1.2x solo inference | > 1.5x |
| Batch wait time | Single request | < 50ms wait | > 200ms wait |
| Adaptive behavior | Variable traffic | Adjusts batch params | Static |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Batch wait time | < 50ms | Time until batch executes |
| Batch fill rate | > 50% | actual_size / max_size |
| Adaptive efficiency | Optimal | throughput vs latency curve |

---

## Mitigation Strategies

### Prevention
1. **Adaptive batch sizing**: Adjust based on traffic
2. **Short batch timeouts**: < 50ms for real-time
3. **Minimum batch of 1**: Process immediately if needed
4. **Traffic-aware batching**: Disable during low traffic
5. **Priority lanes**: Skip batching for urgent requests

### Adaptive Batching
```python
class AdaptiveBatcher:
    def __init__(self):
        self.batch = []
        self.last_request_time = time.time()
    
    def get_timeout(self):
        """Shorter timeout when traffic is low."""
        gap = time.time() - self.last_request_time
        
        if gap > 1.0:  # Low traffic
            return 0.01  # 10ms - almost immediate
        elif gap > 0.1:  # Medium traffic
            return 0.03  # 30ms
        else:  # High traffic
            return 0.1   # 100ms - wait for full batch
    
    def add_request(self, request):
        self.last_request_time = time.time()
        self.batch.append(request)
        
        if len(self.batch) >= self.max_size:
            return self.flush()
        
        # Schedule flush with adaptive timeout
        schedule_flush(self.get_timeout())
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `batch.wait.p95` | > 100ms |
| `batch.fill.rate` | < 30% |
| `batch.timeout.ratio` | > 50% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Batch Wait Excessive | wait_p95 > 200ms | P3 |
| Low Batch Efficiency | fill_rate < 20% | P3 |
| Batching Overhead | timeout_ratio > 70% | P2 |

---

## References

- [Dynamic Batching for ML](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html#dynamic-batcher)
- [Batching Strategies](https://www.anyscale.com/blog/continuous-batching-llm-inference)
