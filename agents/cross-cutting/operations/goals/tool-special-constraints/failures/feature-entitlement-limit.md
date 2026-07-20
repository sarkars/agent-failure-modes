# Feature Entitlement Limit

## Issue
An agent calls a tool feature or API endpoint that exists and is documented, but the calling account's subscription tier doesn't actually include entitlement to it — the feature is gated behind a higher plan. The agent's tool-selection logic was built (or tested) against a fuller-featured tier and has no awareness that entitlements vary by account, so it attempts the call as a matter of course and only discovers the gap when the tool rejects the request, often deep into a multi-step task where a cheaper, entitled alternative was available but never considered.

**Frequency**: Occasional

**Symptoms**
- Tool calls failing with errors like "upgrade required," "feature not available on your plan," or a 402/403 response tied to plan tier rather than a technical fault
- The same tool call succeeding in a staging/test environment (provisioned on a higher tier) but failing in production (provisioned on a lower tier)
- Agent retry logic treating an entitlement rejection as a transient error and retrying identically, when retrying cannot succeed regardless of attempt count
- Tasks that fail entirely for lack of a premium feature when a lower-tier equivalent feature could have accomplished the same goal with minor adjustment

## Root Cause
Agents are typically developed and tested against a single account, often provisioned with a generous or full-featured tier for convenience during development, so the agent's tool-calling logic never has to distinguish "this feature exists" from "this account is entitled to this feature." Entitlement is a property of the account-tool relationship, not of the tool's API surface itself, and most tool clients don't expose entitlement status as a queryable precondition — the only way to discover a gap is to attempt the call and parse the resulting error. Because entitlement failures return errors that can look superficially similar to other 4xx failures, agents without specific handling for entitlement errors treat them the same as any other failure, often retrying pointlessly or crashing the task instead of recognizing the failure as permanent and plan-related.

## Example
```
A document-processing agent is developed and tested against an
"Enterprise" tier account for a PDF-extraction API, which includes a
"structured-table-extraction" feature. The production deployment,
however, runs under a "Business" tier account (procured separately by
finance to reduce cost), which does not include table extraction --
only basic text extraction.

The agent's document pipeline calls the table-extraction endpoint as
its default path for any PDF containing what looks like tabular data.
In production, this call returns a 403 with body: {"error":
"feature_not_entitled", "required_tier": "enterprise"}.

The agent's generic error handler logs the failure and retries twice
(per its default retry policy for 4xx errors under a certain code
range), both attempts failing identically, before falling through to
a catch-all failure state that aborts the entire document's processing
-- even though a fallback path using only basic text extraction
(entitled under the Business tier) could have extracted most of the
needed data, just without table structure preserved.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of agent deployments provisioned on a lower tier than their development/staging environment encounter at least one entitlement-gated feature failure in the first month of production use | Typical range observed in tiered-SaaS tool integrations |
| Entitlement errors are frequently misclassified and retried as transient failures when agents lack explicit entitlement-error handling | Reported range across teams auditing retry logic against error taxonomies |
| Building tier-aware fallback paths for entitlement-gated features substantially reduces full task failures caused by this pattern | Estimated from teams that added graceful degradation for entitlement gaps |

## Mitigations
1. **Entitlement-aware error classification**: Explicitly recognize entitlement/plan-tier errors as a distinct, non-retryable error class, separate from transient failures, so the agent doesn't waste retries on a call that cannot succeed.
2. **Pre-flight entitlement check**: Where the tool vendor exposes an account-entitlements or plan-info endpoint, query it once at startup or session initialization and cache which features are available, gating tool selection on the result rather than discovering gaps at call time.
3. **Tier-aware fallback paths**: Design a graceful-degradation path for premium features (e.g., basic extraction if structured extraction isn't entitled), so a missing entitlement degrades output quality rather than failing the task outright.
4. **Environment parity between staging and production**: Provision staging/test accounts on the same tier as production, so entitlement gaps are caught during testing rather than discovered live.
5. **Entitlement change monitoring**: Track and alert on plan/tier changes to the account credentials an agent uses, since a downgrade (deliberate cost-cutting or an expired promotional tier) can silently remove entitlements an agent's logic depends on.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| entitlement_error_count | Count of tool calls failing specifically due to plan/tier entitlement gaps | Alert if > 0 |
| entitlement_error_retry_count | Count of retries attempted on calls that failed due to entitlement gaps | Alert if > 0 (retries cannot succeed) |
| fallback_path_usage_rate | Rate at which tasks fall back to a lower-tier feature path due to entitlement gaps | Informational; review if it rises sharply |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Entitlement gap causing task failure | A task fails entirely due to an entitlement-gated feature with no fallback available | High | Review account tier vs. agent requirements, implement fallback or upgrade plan |
| Retry attempted on entitlement error | The agent's retry logic engages on an error classified as entitlement-related | Medium | Fix error classification to mark entitlement errors as non-retryable |

## Related Patterns
- [License Expiration Not Checked](./license-expiration-not-checked.md) - both involve the agent discovering an account-level access restriction only when a call fails, rather than tracking it proactively
- [Concurrent Session Not Licensed](./concurrent-session-not-licensed.md) - a related licensing-boundary failure, capping simultaneous usage rather than gating specific features
