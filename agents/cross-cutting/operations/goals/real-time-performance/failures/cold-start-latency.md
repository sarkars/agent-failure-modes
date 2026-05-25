# Cold Start Latency

## Issue: First Request After Idle Has Unacceptable Delay

**Frequency**: Common

**Symptoms**
- First request takes 5-30x longer than subsequent requests
- Latency spikes after deployment or scaling events
- Inconsistent user experience after idle periods
- Timeout errors on first requests

**Root Cause**
Model loading, container initialization, connection pool warming, and cache population create significant delays on first request. Serverless and auto-scaling architectures amplify this issue.

**Example**
```
Cold start breakdown:
- Container start: 2-5s
- Model loading: 3-15s (depends on model size)
- Connection pool: 500ms-2s
- Cache warming: varies

Timeline:
00:00 - Request arrives at cold instance
00:02 - Container ready
00:12 - Model loaded into memory
00:13 - First inference starts
00:14 - Response sent (14s total vs 800ms warm)

User impact: First user waits 14s, subsequent users get 800ms
```

**Contributing Factors**
- Large model sizes
- Serverless/auto-scaling architecture
- No keep-alive or pre-warming
- Aggressive scale-to-zero policies
- No connection pooling

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Cold start timing | Request after 30min idle | < 5s | > 10s |
| Scale-up latency | Sudden traffic spike | New instances < 10s | > 30s |
| Post-deploy first request | After deployment | < warm + 5s | > 3x warm |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Cold start time | < 5s | First request latency after idle |
| Warm ratio | > 95% | warm requests / total |
| Scale-up time | < 30s | Time to handle traffic spike |

---

## Mitigation Strategies

### Prevention
1. **Keep-alive requests**: Prevent scale-to-zero
2. **Pre-warming**: Initialize instances before traffic arrives
3. **Minimum instances**: Maintain warm pool
4. **Model optimization**: Quantization, smaller models
5. **Lazy loading**: Load model components on-demand

### Architecture Patterns
```python
# Pre-warming strategy
def prewarm_schedule():
    # Keep N instances warm during business hours
    if is_business_hours():
        min_instances = 3
    else:
        min_instances = 1
    
    # Periodic health checks prevent idle timeout
    schedule.every(5).minutes.do(health_ping)
```

### Recovery
- Graceful degradation to lighter model during cold start
- Queue requests during initialization
- Return cached responses while warming

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `instance.cold_start.duration` | > 10s |
| `instance.warm.ratio` | < 90% |
| `scaling.event.latency` | > 30s |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Cold Start Spike | cold_start > 15s | P2 |
| Too Many Cold Starts | warm_ratio < 80% | P2 |
| Scale-up Timeout | new instance > 60s | P1 |

---

## References

- [AWS Lambda Cold Starts](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Model Loading Optimization](https://huggingface.co/docs/transformers/perf_infer_gpu_one)
