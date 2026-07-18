# Feature Flag Disabled

## Issue
A tool capability the agent's logic depends on is gated behind an account- or environment-level feature flag that the vendor has not enabled for this particular customer, tier, or region. The agent has no API-level way to check whether the flag is on before calling the feature, so it discovers the gap only when the call fails or silently no-ops, and the failure looks identical to a bug in the agent's own code rather than an environment configuration gap.

**Frequency**: Common

**Symptoms**
- A feature works flawlessly in one customer's environment or in staging but fails or behaves differently in another environment with no code difference
- The tool's API returns a generic "forbidden," "not available," or "feature not enabled" error with no indication of which flag or how to request it
- The same agent codebase produces different behavior across tenants in a multi-tenant deployment, correlated with account tier rather than any input data
- Support tickets to the vendor reveal the feature requires a manual enablement step or a plan upgrade the team wasn't aware of
- Feature works after a delay with no code change, once someone manually requests the flag be enabled

## Root Cause
Vendors commonly use feature flags to control staged rollouts, plan-tier gating, or account-specific enablement, and this flag state is usually not exposed through any introspection API the caller can query ahead of time. The agent's integration is typically developed and tested in one environment (a developer's sandbox account, a shared staging tenant) where the flag happens to be on, so the dependency on flag-gated behavior isn't discovered until the agent runs against a different account where it's off. Because the flag is often tied to billing tier or a manual sales/support enablement process, there's no self-service way for the agent (or its operators) to detect or fix the gap without contacting the vendor.

## Example
```
1. A support-automation agent uses a helpdesk tool's "auto-tagging" API to categorize
   incoming tickets, developed and tested against the team's own staging account where
   auto-tagging was enabled as part of an early-access program.
2. The agent is deployed to production, integrated with a customer's helpdesk account
   on the tool's standard plan tier, which does not have auto-tagging enabled by default.
3. Every call to the auto-tagging endpoint returns HTTP 403 with body
   `{"error": "feature_not_available"}` — no mention of which flag, no link to request access.
4. The agent's error handling treats 403 as an auth failure and attempts to refresh
   the API token, which succeeds (the token is valid) and retries the call, which fails
   identically.
5. After several days of every ticket landing untagged, a support lead escalates,
   and it takes a call to the vendor's account team to learn that auto-tagging requires
   a plan upgrade or an early-access flag the customer's account doesn't have.
```

## Statistics
| Finding | Context |
|---------|---------|
| Feature-flag-gated capability gaps are a common source of "works in staging, fails in production" incidents for multi-tenant SaaS integrations, frequently cited in the 15-30% range of such incidents | Consistent with staging/dev accounts often having broader feature access than standard production tenants |
| Median time-to-resolution for flag-gated failures is typically longer than for straightforward auth or rate-limit errors, often 2-3x, since resolution usually requires vendor contact rather than a code fix | Because there's no self-service path to detect or toggle the flag |
| Explicit capability-check calls (where the vendor exposes one) at agent startup catch the large majority of flag-gating issues before they reach a production failure | By failing at initialization rather than mid-workflow |

## Mitigations
1. **Capability pre-check at startup**: Where the vendor exposes any kind of account/plan introspection endpoint, call it at agent initialization and fail fast with a clear message if a required feature isn't enabled, rather than discovering it mid-workflow.
2. **Environment parity between staging and production accounts**: Ensure the staging/development account used to build and test the agent has the same feature-flag configuration as the production accounts it will actually run against.
3. **Explicit error classification for flag-gated responses**: Recognize vendor error codes/messages specifically associated with feature-not-enabled conditions (distinct from auth or rate-limit errors) and route them to a "contact vendor / needs manual enablement" alert rather than a retry loop.
4. **Graceful degradation when a flagged feature is unavailable**: Design the agent's workflow so a missing optional capability (like auto-tagging) degrades to a manual/fallback path (e.g., leave ticket untagged for human triage) rather than blocking the whole workflow.
5. **Track feature-flag dependencies per tenant in multi-tenant deployments**: Maintain a record of which flag-gated features each customer account actually has enabled, and validate it during onboarding rather than assuming parity across tenants.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `feature.not_enabled_error_rate` | Rate of vendor responses indicating a feature-flag-gated capability is unavailable | Alert on any occurrence in production |
| `tenant.capability_parity_gap_count` | Count of tenants whose enabled feature flags differ from the reference/staging configuration | Alert on any newly onboarded tenant with a gap |
| `workflow.fallback_path_rate` | Rate at which the agent falls back to a degraded/manual path due to an unavailable flagged feature | Track as a leading indicator of flag-gating impact |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Flag-gated feature unavailable in production | `not_enabled_error_rate` > 0 for a required capability | High | Halt dependent workflow, contact vendor account team, activate fallback path |
| New tenant onboarded with capability gap | `capability_parity_gap_count` increases at tenant onboarding | Medium | Validate required flags before go-live, request enablement proactively |

## Related Patterns
- [Regional Feature Not Available](./regional-feature-not-available.md) - same "capability the agent assumes exists is actually gated" pattern, gated by region instead of account flag
- [Paid Feature Cost Not Disclosed](./paid-feature-cost-not-disclosed.md) - flag-gating is often tied to plan tier, overlapping with undisclosed paid-feature costs
- [Beta Feature Instability](./beta-feature-instability.md) - beta features are frequently the same features gated behind an early-access flag
