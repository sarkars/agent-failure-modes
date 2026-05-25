# Timeout Misconfiguration

## Issue: Timeouts Set Too Short or Too Long for Use Case

**Frequency**: Common

**Symptoms**
- Premature request termination (too short)
- Resources held indefinitely (too long)
- Inconsistent behavior across environments
- Cascading failures from timeout mismatches

**Root Cause**
Default timeouts don't match actual operation latency. Too short: valid requests killed. Too long: failed requests block resources. Timeout values not coordinated across system layers.

**Example**
```
Misconfigured timeout chain:

Client timeout: 30s
├── API Gateway: 29s
├── Load Balancer: 60s (too long - holds connection)
├── App Server: 25s
└── LLM API: 120s (never reached - killed at 25s)

Problem: App kills request at 25s, but LLM continues processing.
User sees error, but tokens still consumed.

Correct configuration:
Client > Gateway > LB > App > LLM
30s    > 28s     > 27s > 26s > 25s (cascading shorter)
```

**Contributing Factors**
- Default timeout values used blindly
- No end-to-end timeout analysis
- Different teams own different layers
- Timeouts not tested under load
- No timeout budget allocation

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Slow LLM response | 20s generation | Completes | Timeout at 15s |
| Cascading timeout | Multi-layer request | Clean error | Partial completion |
| Resource cleanup | Timeout triggered | Resources freed | Connection leak |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Timeout rate | < 1% | timeouts / total requests |
| Timeout cascade correctness | 100% | outer > inner at all layers |
| Resource leak on timeout | 0 | connections after timeout |

---

## Mitigation Strategies

### Prevention
1. **Timeout budgeting**: Allocate across layers
2. **Cascading timeouts**: Outer > inner at each layer
3. **Operation-specific timeouts**: Different for different operations
4. **Timeout testing**: Verify under realistic conditions
5. **Documentation**: Document timeout values and rationale

### Timeout Architecture
```python
# Timeout budget allocation
TOTAL_BUDGET = 30  # seconds

TIMEOUT_CONFIG = {
    "client": TOTAL_BUDGET,
    "gateway": TOTAL_BUDGET - 2,
    "app": TOTAL_BUDGET - 4,
    "llm_api": TOTAL_BUDGET - 6,
    "tool_calls": min(5, TOTAL_BUDGET - 10),  # Cap tool timeouts
}

# Per-operation overrides
OPERATION_TIMEOUTS = {
    "simple_query": 10,
    "complex_analysis": 45,
    "document_processing": 120,
}
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `request.timeout.rate` | > 2% |
| `timeout.cascade.violation` | > 0 |
| `connection.leak.count` | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Timeout Rate | rate > 5% | P2 |
| Timeout Cascade Broken | inner > outer | P2 |
| Connection Leak | leaks > 10 | P1 |

---

## References

- [Timeout Best Practices](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Cascading Timeout Design](https://microservices.io/patterns/reliability/circuit-breaker.html)
