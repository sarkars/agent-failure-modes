# Token Budget Overflow Attack

## Issue: Attacker Intentionally Triggers High-Token Operations to Exhaust Cost Budget

**Frequency**: Occasional

**Symptoms**
- Disproportionately high token usage from single user/request
- Agent processes unusually long inputs without cost validation
- Repeated expansive operations (summarize 1000 documents) exhaust budget
- Service degradation as cost budget consumed, feature degradation for other users
- Late discovery: attacker operates for hours before alerts fire

**Root Cause**
When token cost budget is not enforced per-request or per-user, an attacker can submit large inputs or request expensive operations (chain-of-thought, multi-agent coordination, large batch processing) to consume the entire monthly budget in minutes. The attack is especially effective against agents with retry logic (each retry multiplies token cost).

**Example**
```
Monthly budget: $5,000

Attack scenario:
1. Submit 10,000-page document for summarization (20K tokens input)
2. Agent internally: chains 100 summaries + verification (1M tokens total)
3. Cost: $15 per request
4. Submit 400 requests in rapid succession
5. Total cost: $6,000 in <30 minutes
6. Remaining users: service degraded/unavailable for rest of month

Legitimate detection time: Hours to days
Impact: Full budget consumed by single attacker
```

**Key Statistics**
- Average token-budget-overflow attack: $1K-20K cost before detection
- Attacker success rate without per-request limits: 95%+
- Mean time to detection: 4-12 hours (when budget exhaustion noticed)
- Most common vector: summarization/translation of large documents

**Contributing Factors**
- No per-request token limit
- No per-user rate limiting
- Budget enforcement only at monthly level (too late)
- Retry logic multiplies cost of each request
- No real-time budget monitoring

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent processes user-submitted documents/inputs
- Agent has cost budget (e.g., $5K/month)
- No per-request or per-user cost limits
- Attacker can submit large inputs or request expensive operations

### Trigger Mechanism
1. Identify expensive operation (long document processing, chain-of-thought, multi-turn)
2. Calculate cost-per-request (e.g., 20K tokens = $0.30)
3. Calculate budget-exhaustion rate (e.g., 17,000 requests to exhaust $5K)
4. Submit requests rapidly until budget exhausted

**Example Reproduction Steps:**
```
1. Measure token cost for single request (large doc = X tokens, $Y cost)
2. Calculate: requests_to_exhaust_budget = budget / cost_per_request
3. Submit requests at max rate possible
4. Monitor: budget remaining, time to exhaustion
5. Verify: Service degradation / feature unavailable after budget exhausted
```

### Expected Failure State
- Requests execute despite high token consumption
- Budget consumed rapidly
- No blocking/throttling of individual requests
- Late detection (budget warning comes after exhaustion)
- Service available to attacker but unavailable to legitimate users

---

## Mitigation Strategies

### Prevention

1. **Hard Per-Request Token Limits with Immediate Enforcement**: Set a maximum token budget per request (e.g., 50K tokens max, $0.50 max per request). Enforce at request initiation time before any processing. This stops large-input attacks at the gate.

2. **Per-User Rate Limiting and Budget Buckets**: Allocate per-user monthly/daily budgets as a fraction of total budget (e.g., $10/day per user). When a user's bucket is exhausted, subsequent requests fail fast. Resets daily to prevent one user from starving others.

3. **Progressive Cost Estimation Before Execution**: Before processing a request, estimate its likely token cost based on input size + operation type. If estimated cost exceeds threshold, request user confirmation or reject outright.

### Detection & Response

1. **Real-Time Budget Burn Monitoring**: Track cost burn rate in real-time. Alert when any user exceeds their per-user budget or when daily burn rate exceeds baseline by >2x. This catches attacks within minutes.

2. **Anomaly Detection on Request Characteristics**: Flag requests with unusual patterns (very long inputs, many retries, repeated identical requests at high volume). Correlate with cost spike.

3. **Automatic Request Throttling on Budget Overage**: When per-user budget exceeded, automatically throttle that user's requests (increase latency, reduce concurrency) rather than failing hard.

### Architecture Patterns

1. **Staged Cost Budget Enforcement**:
   - Tier 1: Per-request limit (50K tokens max)
   - Tier 2: Per-user daily limit ($10/day)
   - Tier 3: Per-user monthly limit ($100/month)
   - Tier 4: Global monthly budget ($5K)

2. **Cost Estimation Layer Before Execution**: Estimate token cost from request characteristics (input length, operation type). Block/warn if estimated cost exceeds threshold before execution.

3. **Budget-Aware Request Queuing**: Queue requests and process in order of cost-efficiency. High-cost requests go to a lower-priority queue, ensuring budget isn't consumed by expensive outliers.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `cost_burn_rate_per_user_per_hour` | Tokens consumed per user per hour | >10x baseline |
| `budget_exhaustion_velocity` | % of monthly budget consumed per day | >20% per day |
| `per_request_token_usage_p95` | 95th percentile token cost per request | >50K tokens |
| `user_quota_overage_rate` | % of users exceeding daily budget | >5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Budget Burn Spike | Cost burn rate >5x baseline for 1+ hour | P1 | Investigate and throttle affected user |
| User Budget Exhausted | Per-user daily limit exceeded | P2 | Throttle requests; notify user |
| Unusual Request Pattern | High volume of expensive requests from single user | P1 | Rate limit user pending review |
| Monthly Budget Threshold | >80% of monthly budget consumed | P2 | Alert team; prepare contingency |

### Dashboard Panels
- Panel 1: Cost burn rate over time (real-time)
- Panel 2: Per-user cost consumption (identify outliers)
- Panel 3: Budget remaining (trajectory to month-end)
- Panel 4: Top 10 expensive requests (identify cost drivers)
- Panel 5: Request cost distribution (identify anomalies)

---

## References

- [Estimating LLM Inference Costs](https://arxiv.org/abs/2408.12110) — Methods for cost estimation
- [Real-Incident Report: $47K Runaway Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) — Cost overflow incident analysis
- [API Rate Limiting Best Practices](https://stripe.com/docs/rate-limiting) — Rate limiting architecture
