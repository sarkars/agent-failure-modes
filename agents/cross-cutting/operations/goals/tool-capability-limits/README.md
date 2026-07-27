# What Are the Most Common Tool Capability Limit Failures in AI Agents?

**Tool capability fails when agents call deprecated endpoints that no longer exist, when beta features are unstable and cause unpredictable failures, when feature flags disable critical functionality, when regional or paid features are unavailable, or when API schema changes break parsing.** The 6 capability-limit patterns documented here cover the versioning and availability challenges of tool lifecycle management — from deprecated endpoints that should have been removed but still exist (causing confusion and encouraging continued use), through beta features that appear available but are unstable, to regional or paid features that are silently unavailable in some contexts. Capability failures are particularly challenging because they're often invisible in testing environments (which often run on stable, feature-complete endpoints) but appear in production when agents call endpoints that don't exist in production, use features disabled by feature flags, or attempt regional operations on non-regional infrastructure.

## Key Takeaways

- 6 patterns are documented here, spanning API versioning, beta-feature instability, deprecated-endpoint retirement, feature-flag disabling, regional availability, and paid-feature cost disclosure.
- Deprecated Endpoint Retirement and Beta Feature Instability are the most severe: deprecated endpoints often still exist for backward compatibility but should never be called by new agents, and beta features may appear available but fail unpredictably under real load.
- Feature Flag Disabled and Regional Feature Not Available are second-order failures specific to infrastructure: agents discover that a capability is disabled only when calling it, not before attempting to use it.
- API Version Schema Mismatch is the highest-level failure: agent code was written against v1.0 API, but production is running v2.0 with incompatible schema, causing parsing failures that break agent behavior.

## Scope

- **Versioning and Schema** — [API Version Schema Mismatch](failures/api-version-schema-mismatch.md). API versions have incompatible schemas; agent written for v1.0 parses v2.0 responses incorrectly or fails to parse them.
- **Lifecycle and Deprecation** — [Deprecated Endpoint Retirement](failures/deprecated-endpoint-retirement.md). Deprecated endpoints are removed; agents still calling them get 404s or errors.
- **Beta and Stability** — [Beta Feature Instability](failures/beta-feature-instability.md). Beta features are not guaranteed stable; they fail unpredictably or change behavior mid-use.
- **Feature Control** — [Feature Flag Disabled](failures/feature-flag-disabled.md). Feature flags disable critical functionality; agents call disabled features and get errors instead of discovering the flag state before attempting to call.
- **Geographic and Regional Scope** — [Regional Feature Not Available](failures/regional-feature-not-available.md). Features are regional-only; agent in unsupported region calls feature and gets error.
- **Cost and Visibility** — [Paid Feature Cost Not Disclosed](failures/paid-feature-cost-not-disclosed.md). Accessing a feature requires a paid tier; cost is not disclosed upfront and agents incur surprise charges.

## When Tool Capability Matters

- An agent is deployed across multiple API versions or environments (dev, staging, production), where capabilities differ and agents must adapt.
- Tools are in active development with beta features, feature flags, and deprecations, where agent behavior must be resilient to capability changes.
- Regional or paid features are involved, where an agent that works in one region or with one subscription tier fails in another.

## Cross-Pattern Insight

The 6 capability-limit patterns describe systems where capability information is incomplete or stale: agents don't know (or can't query) which features are available in their environment, deprecated endpoints still exist for backward compatibility (causing confusion), and beta features appear stable until production load reveals instability. Most teams discover capability failures only when deploying agents to production and hitting errors from disabled features, missing endpoints, or unsupported capabilities. The mitigation that recurs across nearly every pattern here is the same architectural move — make capability information queryable and always-current: expose capability information at runtime (feature flag state, regional availability, paid-tier requirements), not just in documentation, validate agent assumptions about capabilities before deploying (don't assume a feature that existed in dev also exists in prod), and test agents against all deployed API versions and regional configurations, not just the primary one.

## Frequently Asked Questions

### How do you handle APIs that have multiple versions in production simultaneously?
Per [API Version Schema Mismatch](failures/api-version-schema-mismatch.md), require agents to explicitly specify API version in each call, and test agents against all supported versions. Never assume all instances are on the same version — they won't be. Use API contracts (OpenAPI, schema definitions) to detect compatibility before deploying.

### Should agents call deprecated endpoints for backward compatibility?
No — per [Deprecated Endpoint Retirement](failures/deprecated-endpoint-retirement.md), deprecated endpoints should be migrated away from before retirement. If deprecation is announced, plan migration and update agents before the endpoint is removed. Don't keep calling deprecated endpoints because they'll eventually be gone.

### How do you test agents for beta-feature instability?
Per [Beta Feature Instability](failures/beta-feature-instability.md), test agents against beta features under realistic load (not just happy-path), and have an explicit degradation strategy if beta features fail: either don't use them in production, or wrap calls in try-catch with fallback behavior. Beta features are "caveat emptor" — expect them to be unstable.

### How do you prevent feature-flag-related failures?
Per [Feature Flag Disabled](failures/feature-flag-disabled.md), agents should query feature-flag state before calling disabled features: `if feature_enabled('critical_feature'): call_feature() else: fail with 'feature disabled'`. Don't call the feature and hope it's enabled — discover the flag state first.

## Patterns

| Pattern | Mechanism |
|---|---|
| [API Version Schema Mismatch](failures/api-version-schema-mismatch.md) | Agent written for API v1.0, production runs v2.0 with incompatible schema; parsing fails or returns wrong data |
| [Beta Feature Instability](failures/beta-feature-instability.md) | Beta features appear available but are unstable; they fail unpredictably or change behavior under real load |
| [Deprecated Endpoint Retirement](failures/deprecated-endpoint-retirement.md) | Agent calls deprecated endpoint that has been removed; gets 404 or error |
| [Feature Flag Disabled](failures/feature-flag-disabled.md) | Agent calls feature controlled by feature flag, but flag is disabled and call fails instead of being prevented upfront |
| [Paid Feature Cost Not Disclosed](failures/paid-feature-cost-not-disclosed.md) | Feature requires paid tier; agent calls it without knowing cost impact |
| [Regional Feature Not Available](failures/regional-feature-not-available.md) | Feature is regional-only; agent in unsupported region calls it and gets error |

**Total: 6 patterns**

## Related Goals

- [Tool Reliability](../tool-reliability/) — capability changes can cause reliability failures
- [Tool Integration Limits](../tool-integration-limits/) — compatibility and integration issues related to capabilities
- [Tool Financial Limits](../tool-financial-limits/) — cost disclosure for features, similar to paid-feature requirements
