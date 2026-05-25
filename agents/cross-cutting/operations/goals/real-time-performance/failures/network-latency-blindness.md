# Network Latency Blindness

## Issue: System Doesn't Account for Network Round-Trip Time

**Frequency**: Occasional

**Symptoms**
- Latency much higher in production than local testing
- Cross-region deployments have poor performance
- API calls slower than expected
- Timeout calculations wrong

**Root Cause**
Development and testing often ignore network latency. Production deployments span regions, cross network boundaries, and involve multiple hops. Each hop adds 10-200ms that isn't accounted for in design.

**Example**
```
Local testing: LLM API call = 500ms

Production reality:
- Client to edge: 20ms
- Edge to app server: 15ms
- App to LLM API (cross-region): 80ms
- LLM processing: 500ms
- LLM to app: 80ms
- App to edge: 15ms
- Edge to client: 20ms
Total: 730ms (46% overhead)

Multi-tool scenario (3 API calls):
Local: 1500ms
Production: 1500 + (3 × 160) = 1980ms (32% overhead)
```

**Contributing Factors**
- Testing only in local/same-region
- Not measuring network latency separately
- Cross-region API calls
- No CDN/edge deployment
- DNS resolution time ignored

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Cross-region latency | Request from distant region | Measured, documented | Unknown |
| Network overhead | Multi-hop request | < 30% of total | > 50% |
| DNS impact | Cold DNS resolution | < 100ms | > 500ms |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Network overhead ratio | < 25% | network_time / total |
| Per-hop latency | < 50ms | Tracing |
| Geographic variance | < 2x | max_region / min_region |

---

## Mitigation Strategies

### Prevention
1. **Measure network separately**: Instrument network time
2. **Co-locate services**: Minimize network hops
3. **Edge deployment**: Process closer to users
4. **Connection pooling**: Reuse connections
5. **DNS caching**: Avoid repeated lookups

### Network-Aware Architecture
```python
class NetworkAwareClient:
    def __init__(self):
        self.latency_by_region = {}
        self.connection_pool = {}
    
    def call_api(self, endpoint, region=None):
        start = time.time()
        
        # Reuse connection
        conn = self.get_pooled_connection(endpoint)
        
        # Measure network vs processing
        network_start = time.time()
        response = conn.request(endpoint)
        network_time = time.time() - network_start
        
        total_time = time.time() - start
        processing_time = total_time - network_time
        
        # Track for routing decisions
        self.latency_by_region[region] = network_time
        
        return response, {
            'network_ms': network_time * 1000,
            'processing_ms': processing_time * 1000,
        }
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `network.latency.p95` | > 200ms |
| `network.overhead.ratio` | > 40% |
| `region.latency.variance` | > 3x |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Network Overhead High | ratio > 50% | P3 |
| Region Latency Spike | region > 2x baseline | P2 |
| Cross-Region Degradation | cross_region > 500ms | P2 |

---

## References

- [Global Latency Considerations](https://cloud.google.com/architecture/reducing-latency)
- [Network Performance Monitoring](https://www.datadoghq.com/blog/network-performance-monitoring/)
