# Stale State Use

## Issue: Agent uses old tool results after new data arrives.

**Frequency**: Common

**Symptoms**
- Later output uses earlier version/timestamp.
- [Add more specific symptoms]

**Root Cause**
Agent uses old tool results after new data arrives.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Cache Invalidation on Write Events**: Any cached tool result or fetched state is tied to an invalidation trigger — when the underlying resource changes (via any writer, agent or external), a change event evicts or marks stale the cached copy, so the agent's next read is forced to re-fetch rather than reuse a snapshot taken before the change.
2. **Freshness Timestamp Checks Before Use**: Every piece of fetched state carries a retrieved_at timestamp and, where available, a resource-side last_modified/version marker. Before using state in a decision, the agent compares its freshness against a per-resource max-age policy and re-fetches if stale, rather than assuming the first fetch in the session remains valid throughout.
3. **Mandatory Re-Fetch for Time-Sensitive Operations**: For operations where staleness has real consequences (inventory checks, pricing, availability, account balance), the pipeline structurally disallows using any cached/remembered value older than a defined window — the tool call is re-issued immediately before the dependent action, no exceptions.

### Detection & Response
1. **Version/Timestamp Mismatch Scanning**: Compare the timestamp or version marker embedded in the agent's final output against the current live value of the same resource; a mismatch beyond the acceptable window indicates stale state was used and is logged for review.
2. **Multi-Fetch Session Auditing**: For sessions that fetch the same resource more than once, check whether later decisions correctly used the most recent fetch rather than an earlier one still lingering in context — flag cases where an earlier value's use persisted after a newer fetch was available.
3. **Downstream Error Correlation**: When an action fails because the real-world state had changed (e.g., "item no longer available"), check whether the agent had a stale local copy that should have been invalidated, and feed that resource type into tighter freshness policy.

### Architecture Patterns
1. **Event-Driven Cache Invalidation Bus**: Resource writers publish change events to a bus; a caching layer subscribes and evicts/marks-stale any cached entries for the changed resource, decoupling invalidation from the agent having to manually decide to re-fetch.
2. **Freshness-Aware State Accessor**: All state reads go through an accessor that checks retrieved_at against a per-resource TTL policy and transparently re-fetches expired entries, so freshness enforcement is centralized rather than repeated ad hoc at each call site.
3. **Version-Stamped Tool Responses**: Tool APIs return a version/ETag alongside data; the agent's decision logic can require a version-match against the latest known version before committing an action that depends on that data, refusing to proceed on a version mismatch.

### Metrics
1. **stale_state_use_incident_count**: Target: 0 per week; Alert threshold: > 3 per week
2. **cache_invalidation_lag_ms**: Target: < 1000ms from write event to cache eviction; Alert threshold: > 10000ms
3. **time_sensitive_op_refetch_compliance_percent**: Target: 100%; Alert threshold: < 100%
4. **version_mismatch_at_output_rate_percent**: Target: < 0.5% of resource-dependent responses; Alert threshold: > 2%

### Alerts
1. **Stale State Drove Incorrect Action** (P1 - Critical): Condition - an agent action was taken based on state confirmed stale (version mismatch beyond window) for a time-sensitive resource. Action: Reverse/correct the action if possible, notify affected user, audit the freshness policy for that resource type.
2. **Cache Invalidation Lag Spike** (P2 - Warning): Condition - cache_invalidation_lag_ms exceeds 10s consistently over 1h. Action: Investigate event bus backlog or subscriber lag, check for dropped invalidation events.
3. **Time-Sensitive Refetch Bypass** (P1 - Critical): Condition - a time-sensitive operation proceeded using a cached value instead of the mandated re-fetch. Action: Immediate patch of the bypass, audit recent actions of that type for stale-state impact.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
