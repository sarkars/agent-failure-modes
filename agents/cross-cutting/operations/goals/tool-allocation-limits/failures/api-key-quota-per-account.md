# Api Key Quota Per Account

## Issue
An agent authenticates to a tool using a shared account-level API key, and that key's quota (requests/minute, tokens/day, credits/month) is pooled across every consumer that happens to use it — other agents, human users, cron jobs, and staging environments. The agent has no visibility into who else is drawing down the same quota, so it plans its own call volume as if it owned the full allocation, then gets throttled or rejected by calls it never made.

**Frequency**: Common

**Symptoms**
- 429 or quota-exceeded errors appear in bursts that don't correlate with the agent's own request volume
- Quota resets mid-task, unblocking the agent with no code change on its side
- Two unrelated agents/services report hitting the same quota ceiling at the same wall-clock time
- Dashboards from the tool vendor show usage the agent's own logs can't account for
- Retrying a previously-successful call pattern now fails because a different consumer already spent the budget

## Root Cause
Vendor billing and access-control models are usually scoped to an account or API key, not to an individual caller or workload. When an organization provisions one key for convenience — shared across a marketing bot, an internal dashboard, and an agent — the tool has no concept of per-caller fairness; it just enforces one aggregate ceiling. The agent's rate-limiting and retry logic is built around its own request rate, which is only a fraction of the actual load on the key.

## Example
```
1. Team provisions a single Stripe-like billing API key for "internal-tools" used by
   (a) a nightly reconciliation script, (b) a support-ticket agent, (c) a finance dashboard.
2. The key has a account-wide quota of 1,000 requests/minute.
3. The support agent is mid-task, paginating through 400 customer records at 8:58 AM.
4. The nightly reconciliation script (unrelated cron job) kicks off at 9:00 AM and issues
   900 requests/minute against the same key for 4 minutes.
5. The support agent's next call returns 429 Too Many Requests.
6. The agent's retry logic assumes it caused the overage, backs off exponentially, and
   times out the user-facing task after 3 retries — even though its own usage was ~15 req/min.
7. On-call engineer spends 20 minutes before finding the reconciliation script in the
   provider's usage dashboard as the actual source of the spike.
```

## Statistics
| Finding | Context |
|---------|---------|
| Shared-key quota exhaustion accounts for an estimated 10-20% of "mysterious" 429 errors in multi-service deployments | Based on typical incident postmortems in orgs with >3 services per API key |
| Median time-to-diagnose for shared-quota incidents is 3-5x longer than single-consumer rate-limit incidents | Because the responding team must correlate cross-service logs |
| Teams that migrate to per-consumer API keys report 60-80% fewer quota-related pages | Attributable to isolated blast radius per key |

## Mitigations
1. **Per-consumer API keys**: Provision a distinct key (or OAuth client) per agent/service, even against the same account, so quota consumption and rate-limit errors are attributable and isolated.
2. **Client-side quota budgeting**: Have each consumer request or negotiate a sub-allocation (e.g., via a token-bucket proxy in front of the shared key) so no single caller can starve the others.
3. **Usage attribution headers**: Tag outbound requests with a consumer identifier (custom header, user-agent suffix) so vendor dashboards and logs can be filtered per-service even when the key is shared.
4. **Circuit breaker with cause detection**: On 429, query the vendor's usage/quota-status endpoint (if available) before retrying, so the agent can distinguish "I caused this" from "someone else caused this" and adjust backoff accordingly.
5. **Centralized rate-limit gateway**: Route all consumers of a shared key through an internal proxy that enforces fair-share allocation and exposes per-consumer metrics independent of the vendor's own dashboard.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `shared_key.quota_remaining_pct` | Percentage of account-level quota remaining, polled from vendor status endpoint | Alert below 20% |
| `agent.429_rate_vs_own_volume` | Ratio of 429 responses to the agent's own request count | Alert when ratio > 0.3 while own volume is flat |
| `shared_key.unattributed_usage_pct` | Share of quota consumption not traceable to a known consumer identifier | Alert above 25% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Shared quota near exhaustion | `quota_remaining_pct` < 10% for 5 minutes | High | Page on-call, identify top consumer via vendor dashboard, throttle non-critical jobs |
| Unattributed spike detected | Aggregate usage jumps >3x baseline with no matching increase in known consumers' logs | Medium | Audit for new/rogue integrations using the same key |

## Related Patterns
- [Concurrent User Quota](./concurrent-user-quota.md) - both stem from a tool-side allocation shared across unrelated consumers
- [Storage Quota Shared Across Agents](./storage-quota-shared-across-agents.md) - same root pattern applied to storage instead of request rate
- [Storage Quota Soft Limit](./storage-quota-soft-limit.md) - degraded-mode behavior that can compound with shared quota exhaustion
