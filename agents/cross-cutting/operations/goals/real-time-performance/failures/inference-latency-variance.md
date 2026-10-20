# Inference Latency Variance

## Issue: Unpredictable Model Inference Times

**Frequency**: Common

**Symptoms**
- Same query has wildly different response times
- P99 is 10x+ P50
- Difficult to set appropriate timeouts
- User experience inconsistent

**Root Cause**
Model inference latency varies based on input length, output length, model state, GPU contention, batch composition, and speculative decoding failures. This variance makes capacity planning and SLA setting difficult.

**Example**
```
Same model, same query type:

Request A: 450ms
Request B: 2800ms
Request C: 520ms
Request D: 4200ms
Request E: 480ms

Variance causes:
- Output length: 50 vs 500 tokens
- GPU memory pressure from concurrent requests
- KV cache misses
- Speculative decoding rejection rate
- Batch padding overhead
```

**Contributing Factors**
- Variable output lengths
- Shared GPU resources
- No request isolation
- Speculative decoding variance
- Dynamic batching inefficiencies

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Latency consistency | 100 identical queries | CV < 0.3 | CV > 0.5 |
| Output length impact | Short vs long output | < 3x difference | > 5x |
| Concurrent load impact | Solo vs loaded | < 2x difference | > 3x |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Latency coefficient of variation | < 0.4 | stddev / mean |
| P99/P50 ratio | < 3 | percentile ratio |
| Output length correlation | Known | latency vs tokens |

---

## Mitigation Strategies

### Prevention
1. **Output length limits**: Cap max tokens to bound latency
2. **Request isolation**: Dedicated capacity for latency-sensitive
3. **Homogeneous batching**: Group similar-length requests
4. **Latency prediction**: Estimate before routing
5. **Speculative decoding tuning**: Optimize for consistency

### Latency Prediction
```python
def predict_latency(request):
    """Estimate latency to enable smart routing."""
    base_latency = 200  # ms
    
    # Input length impact
    input_factor = len(request.tokens) * 0.5  # ms per token
    
    # Expected output length (from similar queries)
    expected_output = estimate_output_length(request)
    output_factor = expected_output * 2  # ms per output token
    
    # Current load factor
    load_factor = get_current_load_multiplier()
    
    estimated = (base_latency + input_factor + output_factor) * load_factor
    
    return estimated, confidence_interval(estimated)
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `inference.latency.cv` | > 0.5 |
| `inference.p99_p50_ratio` | > 5 |
| `inference.outlier.rate` | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Variance | CV > 0.6 | P3 |
| Extreme Outliers | P99 > 10x P50 | P2 |
| Unpredictable Latency | prediction error > 50% | P3 |

---

## Chat assistant examples

### Unpredictable latency

**Before** (support chat on a US airline's mobile app, Friday evening):

> **Maria:** Can I switch my Denver flight to Saturday morning? *(reply in 3 s)*
> **Assistant:** Yes. Saturday has a 7:10 a.m. departure with seats open. *(3 s)*
> **Maria:** What would the fare difference be? *(reply in 41 s, no status shown)*
> **Maria:** hello?? *(she resends at 20 s)*
> **Assistant:** The difference is $38. Say "confirm" to change. *(41 s, plus a duplicate answer to "hello??")*

**After** (same chat, delay flagged and held in a stated range):

> **Maria:** What would the fare difference be?
> **Assistant:** Fare lookups can take up to 40 seconds right now. I'll show the price as soon as it comes back. *(2 s)*
> **Assistant:** The difference is $38. Say "confirm" to change. *(38 s)*

**What the user experiences:** The first answer took 3 seconds, so a 41-second silence looks like a crash, and Maria resends and gets a duplicate reply.

**Fix:** When a reply is likely to take much longer than the usual one, say so within a couple of seconds and give a time range, so the wait is expected instead of mysterious. Details on status and ETA wording: [silent long-running work](../../../../../by-capability/human-machine-interface/goals/response-time/failures/silent-long-running-work.md).

---

## References

- [LLM Inference Optimization](https://arxiv.org/abs/2309.06180)
- [Speculative Decoding](https://arxiv.org/abs/2211.17192)
