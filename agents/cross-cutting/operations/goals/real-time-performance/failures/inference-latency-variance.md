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

## References

- [LLM Inference Optimization](https://arxiv.org/abs/2309.06180)
- [Speculative Decoding](https://arxiv.org/abs/2211.17192)
