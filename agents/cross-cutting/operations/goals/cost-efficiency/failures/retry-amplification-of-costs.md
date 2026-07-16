# Retry Amplification of Costs

## Issue: Exponential Retry Logic Multiplies Costs Beyond Original Request

**Frequency**: Common

**Symptoms**
- Single failed request triggers 10+ retries with exponential backoff
- Each retry invokes the LLM (re-processes input, increases tokens)
- Cascading retries across multiple components (agent retries → tool retries → API retries)
- Cost of single request becomes 10-100x original
- Retry logic well-intentioned (improve reliability) but hidden cost multiplier

**Root Cause**
Retry logic is designed to improve reliability (retry on transient failures), but when retries invoke the LLM again or call expensive models, costs multiply explosively. A single $0.10 request with exponential backoff (retry delays: 1s, 2s, 4s, 8s, 16s...) across 3 layers (agent, tool, API) can become $10-100 in costs.

**Example**
```
Original request: Summarize document ($0.10, 100 tokens)

Agent Retry Logic (exponential backoff):
- Attempt 1: Fails → $0.10
- Attempt 2: 1s delay, retry → $0.10
- Attempt 3: 2s delay, retry → $0.10
- ...
- Attempt 10: $0.10
- Total: $1.00 cost for one request

But each retry invokes the LLM with full input (100 tokens again):
- 10 retries × 100 tokens × 10 retries in tool layer × 10 in API layer
- = 10,000 token invocations for a 100-token request
- Cost: $1.00 per attempt × 3 layers × 10 attempts = $30+

Result: $0.10 request becomes $30 in costs
```

**Key Statistics**
- Retry amplification affects 40-60% of agentic systems
- Cost multiplication factor: 5-100x without proper controls
- Most common: exponential backoff used at multiple layers
- Undetected retry storms: $5K-100K monthly cost overages

**Contributing Factors**
- Exponential backoff at multiple layers (no coordination)
- Each retry re-invokes LLM instead of using cached response
- No retry budget enforcement
- Retry limits set too high (10-100 retries common)
- Cascading retries (agent retries → tool retries → external API retries)

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent has retry logic (exponential backoff)
- Tools have retry logic
- External APIs have retry logic
- Single failure can trigger cascading retries across all layers

### Trigger Mechanism
1. Inject transient failure (timeout, 503, connection error) into external service
2. Observe: How many retries triggered at each layer?
3. Measure: Total token cost vs. single request cost

**Example Reproduction Steps:**
```
1. Set up agent with retry logic
2. Set up tool wrapper with retry logic
3. Configure external API call (likely has retry logic)
4. Inject transient failure: temporarily return 503 error
5. Measure: 
   - Agent retries: 1, 2, 5, 10?
   - Tool retries: 1, 2, 5, 10?
   - API retries (hidden): ?
6. Calculate: Total tokens = attempts × input_tokens × layers
7. Calculate: Total cost = token_count × cost_per_token
```

### Expected Failure State
- Single request triggers 10+ retries
- Each retry re-invokes LLM (full token cost)
- Multiple layers all retrying independently
- Total cost: 10-100x original request
- No visibility into retry amplification

---

## Mitigation Strategies

### Prevention

1. **Centralized Retry Budget with Shared Counter**: Set a global retry budget per request (e.g., 3 retries max, shared across all layers). Each layer consumes from budget. When budget exhausted, fail fast. Prevents cascading retries.

2. **Response Caching Across Retries**: Cache the LLM response from the first attempt. If retrying due to external service failure (not LLM failure), use cached response instead of re-invoking LLM. Only retry the failing component.

3. **Exponential Backoff with Reasonable Limits**: Cap exponential backoff: max retry attempts = 3, max backoff = 30s, don't retry on all errors (only transient: timeout, 503). Don't retry on permanent failures (401, 404).

### Detection & Response

1. **Retry Cost Tracking per Request**: Log every retry attempt with cumulative cost. Alert if retry cost >N× original request cost.

2. **Retry Amplification Monitoring**: Track retry counts across layers. If agent retries 5x AND tool retries 5x AND API retries 5x, alert on cascading retries.

3. **Automatic Retry Budget Enforcement**: Implement hard limit on retry attempts per request. When limit reached, fail fast rather than continuing retries.

### Architecture Patterns

1. **Shared Retry Budget Across Layers**:
   ```
   request_retry_budget = 3  # Shared across all layers
   
   agent_call():
       attempts = 0
       while attempts < request_retry_budget:
           try:
               return tool.call()
           except TransientError:
               attempts += 1
               request_retry_budget -= 1  # Consumed by this layer
   
   tool_call():
       # Can only retry if request_retry_budget > 0
       if request_retry_budget <= 0:
           raise  # Fail fast, don't retry
   ```

2. **Response Cache Across Retry Attempts**:
   ```
   def call_with_retry(input):
       cached_response = cache.get(input)  # Use cached response if available
       
       for attempt in range(max_retries):
           try:
               return api.call(input)  # May fail if API is down
           except APIError:
               if cached_response:
                   return cached_response  # Use cache on retry, don't re-invoke LLM
               attempt += 1
   ```

3. **Retry Policy with Transient-Only Logic**:
   ```
   retry_policy = {
       'timeout': True,  # Transient, retry
       '503': True,      # Transient, retry
       '429': True,      # Rate limit, retry with backoff
       '401': False,     # Auth error, don't retry
       '404': False,     # Not found, don't retry
   }
   ```

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `avg_retries_per_request` | Average number of retry attempts | >3 |
| `retry_cost_multiplier` | Total cost vs. first-attempt cost | >5x |
| `cascading_retry_depth` | Retry attempts across all layers | >10 total |
| `retry_success_rate` | % of retries that eventually succeed | <50% (indicates retry isn't helping) |
| `retry_budget_exhaustion_rate` | % of requests hitting retry limit | >5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High Retry Cost | Retry cost >5x original request | P2 | Investigate whether retries are necessary |
| Cascading Retries | Retry attempts >10 across layers | P2 | Review retry policies at each layer |
| Retry Budget Exhausted | Request hits retry limit | P1 | Investigate transient failures; may indicate service issue |
| Low Retry Success Rate | <50% of retries succeed | P2 | Reevaluate retry logic; may be retrying permanent failures |

### Dashboard Panels
- Panel 1: Retry count distribution (most requests: 0-1 retries, outliers >5)
- Panel 2: Retry cost multiplier over time
- Panel 3: Cascading retry depth (layer breakdown)
- Panel 4: Retry success rate by error type
- Panel 5: Retry budget usage (% of requests hitting limit)

---

## Related Patterns

**This pattern focuses on COST EXPLOSION caused by cascading retries across multiple layers within a single request.**

For coordination failures where multiple agents retry simultaneously, see:
- **[Retry Storms](./retry-storms.md)** — When multiple agents retry at the same time without backoff, overwhelming downstream services

**Key distinction:**
- `retry-amplification-of-costs` = Single request → cascading retries across layers → LLM re-invocation → 10-100x cost
- `retry-storms` = Multiple agents → simultaneous retries without coordination → overwhelm downstream → rate limits

Related cost-control patterns:
- **[Expensive Model Cascade](./expensive-model-cascade.md)** — Unnecessary routing to expensive models
- **[Cost-Quality Tradeoff](./cost-quality-tradeoff.md)** — Spending more tokens for diminishing accuracy gains

---

## References

- [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) — Best practices for retry delays
- [Microsoft Polly: Resilience Patterns](https://github.com/App-vNext/Polly) — Retry policy library
- [Retry Storms and Cascading Failures](https://blog.timescale.com/blog/what-we-learned-from-the-recent-outages-how-we-improved-timescale-cloud/) — Real incident analysis
