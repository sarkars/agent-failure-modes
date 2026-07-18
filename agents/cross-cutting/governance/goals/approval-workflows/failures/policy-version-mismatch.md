# Policy Version Mismatch

## Issue
An agent evaluates a proposed action against a stale, cached copy of a policy while the authoritative version has already been updated elsewhere (a new threshold, a newly added restriction, a removed exception). The resulting approval or auto-approval decision is based on rules that are no longer current, producing an outcome that would be different — and would not hold up — if evaluated against the actual, up-to-date policy.

**Frequency**: Common

**Symptoms**
- Agent approval decisions that don't match what the current, published policy would produce for the same input
- Multiple agents or services in the same system enforcing different effective versions of what should be a single policy
- No cache invalidation triggered when the authoritative policy source is updated, so cached copies persist indefinitely until a TTL (if any) expires
- Compliance discovering that an agent has been operating on a policy version that was superseded weeks or months earlier
- Policy update deployments that don't include a mechanism to confirm all consuming services have picked up the new version

## Root Cause
For performance reasons, agents and policy-evaluation services commonly cache policy definitions locally rather than fetching them fresh on every decision. When policy updates are published without a corresponding invalidation signal (a pub/sub notification, a version-checked pull, a short TTL) reaching every cache, some agents keep evaluating against the old version indefinitely, and there is often no reconciliation process to detect the drift between cached and authoritative policy state.

## Example
```
1. A content-moderation policy is cached by an agent service with a 24-hour
   TTL, refreshed by pulling from a central policy store once per day.
2. The policy team identifies a new abuse pattern and urgently tightens the
   policy at 9:00 AM, publishing the update to the central store
   immediately, with the expectation that it takes effect right away.
3. The agent service, having refreshed its cache at 6:00 AM that same day,
   does not pull the new version again until its next scheduled refresh,
   roughly 24 hours later.
4. For the intervening ~15 hours, the agent continues approving content
   under the old, looser policy, including several items that the new
   policy was specifically designed to catch.
5. The policy team, seeing the update as "live" from the moment it was
   published to the central store, is unaware that a significant share of
   production traffic is still being evaluated against the old rules until
   a downstream report shows content that should have been blocked getting
   through.
```

## Statistics
| Finding | Context |
|---------|---------|
| Systems relying on TTL-based cache expiry rather than active invalidation typically show a policy-propagation lag proportional to the TTL, commonly ranging from minutes to a full day | Typical pattern in cache-based configuration distribution |
| A meaningful share of "policy not enforced as expected" incidents trace back to a stale cache rather than an error in the policy logic itself | Common finding in postmortems for agentic systems with distributed policy evaluation |
| Systems with active push-based invalidation show propagation lag reduced by an order of magnitude or more compared to pure TTL-based approaches | Consistent with the general effect of push versus pull cache invalidation |

## Mitigations
1. **Push-based cache invalidation, not TTL alone**: When a policy is updated at its authoritative source, actively notify (via pub/sub, webhook, or equivalent) all consuming agents/services to invalidate their cached copy immediately, rather than relying solely on a periodic TTL refresh.
2. **Policy version stamped on every decision**: Record the exact policy version (hash or version ID) used for every approval decision, so any mismatch between the version an agent used and the version that was authoritative at that moment is detectable after the fact.
3. **Version-check on critical or high-risk evaluations**: For high-risk action categories, require a live version check against the authoritative source before finalizing a decision, rather than trusting a cache regardless of its age.
4. **Propagation confirmation for urgent policy updates**: When a policy update is marked urgent, require confirmation that all known consuming services have picked up the new version before considering the rollout complete, rather than assuming publication equals propagation.
5. **Periodic reconciliation audit between cached and authoritative policy state**: Regularly compare the policy version each service is actively using against the current authoritative version, flagging any service running a stale copy beyond an acceptable staleness window.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `policy_cache_staleness_p95` | 95th-percentile age of cached policy versions relative to the current authoritative version | > defined TTL + propagation buffer (e.g., 30 minutes) |
| `decision_version_mismatch_count` | Number of decisions made using a policy version older than the authoritative version at decision time | > 0 for urgent-tier policy updates |
| `unconfirmed_propagation_count` | Number of consuming services that haven't confirmed pickup of the latest policy version after an update | > 0 past the propagation SLA |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Urgent policy update not propagated | An urgent-tier policy update has not been confirmed picked up by all consuming services within the propagation SLA | Critical | Force cache invalidation across all services, manually verify enforcement, escalate to platform on-call |
| Decision made on stale policy version | A logged decision's policy version stamp is older than the authoritative version at the time of the decision | Warning | Audit the specific decision for correctness under the current policy, investigate cache invalidation gap |

## Related Patterns
- [Policy Consistency Violation](./policy-consistency-violation.md) - both can result in different effective policies being applied to functionally identical actions
- [Policy Retroactive Application](./policy-retroactive-application.md) - both involve confusion about which policy version governs a decision at a given point in time
- [Policy Temporal Violation](./policy-temporal-violation.md) - both are timing-related failures in how policy state is evaluated relative to the current moment
