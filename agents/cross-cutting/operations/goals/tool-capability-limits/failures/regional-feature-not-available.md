# Regional Feature Not Available

## Issue
An agent depends on a tool capability that is only available in certain geographic regions — often due to data residency law, licensing agreements, or a vendor's staged global rollout — while the agent's deployment runs in or serves users from a region where the feature isn't offered. Because development and testing typically happen from a single region (usually wherever the engineering team is based), the gap is invisible in testing and only appears once the agent is exercised against traffic or infrastructure in the unsupported region.

**Frequency**: Occasional

**Symptoms**
- The exact same agent code and configuration works in one deployment region and fails in another
- API calls from certain regions return a region-specific error (e.g., "not available in your region," "unsupported locale") while identical calls from the home region succeed
- Feature works fine for the engineering team's own testing (based in one region) but fails for actual end users or infrastructure located elsewhere
- Vendor documentation mentions regional availability only in a footnote, a separate compliance page, or not at all
- A newly added deployment region (e.g., expanding to EU or APAC) triggers a wave of new failures with no code change

## Root Cause
Vendors often restrict feature availability by region for legal reasons (data residency requirements like GDPR, export control regulations), infrastructure reasons (a feature depends on data centers not yet built out in a given region), or licensing reasons (the vendor's underlying data/model provider only has rights in certain markets). This regional gating frequently isn't exposed through any capability-introspection API, and engineering teams building and testing an agent typically only exercise it from their own region's infrastructure, so the regional gap is structurally invisible until the agent is actually deployed or serving traffic tied to the unsupported region.

## Example
```
1. A global e-commerce company builds a fraud-detection agent using a risk-scoring
   vendor's real-time API, developed and tested entirely from the company's US-based
   engineering team and US-hosted staging environment.
2. The vendor's real-time risk-scoring feature depends on a data-center presence and
   licensing agreements that only cover North America and Western Europe; it silently
   excludes several other regions where the vendor lacks the necessary data licensing.
3. The company expands operations to a new APAC market and routes that region's
   transaction traffic through the same fraud-detection agent, unchanged.
4. Every risk-scoring call for APAC transactions returns
   `{"error": "service_unavailable_in_region"}`.
5. The agent's fallback logic (written for generic API errors, not region-specific ones)
   treats the failure as "unable to score, default to manual review," which is the
   intended safe fallback — but manual review queues aren't staffed for the sudden
   100% review rate in the new market, causing multi-day order processing delays.
6. It takes several days to trace the review backlog to the region-gated feature rather
   than a capacity or bug issue.
```

## Statistics
| Finding | Context |
|---------|---------|
| Regional feature-availability gaps are a recurring cause of "works in testing, fails after expansion" incidents for companies scaling into new geographic markets, frequently surfacing within the first 1-3 months of expansion | Consistent with dev/test environments rarely exercising non-home-region infrastructure |
| Vendors citing data residency or export-control restrictions account for a large share of documented regional feature gaps, often the majority in regulated industries like finance and healthcare | Reflects legal rather than purely technical constraints |
| Pre-expansion capability audits (checking regional availability for every tool dependency before launching in a new market) have been observed to catch the large majority of these gaps before they cause a production incident | By treating regional expansion as a dependency-review checkpoint rather than a pure infrastructure task |

## Mitigations
1. **Pre-expansion dependency audit**: Before routing traffic from a new region through an existing agent, explicitly verify regional availability for every third-party tool capability it depends on, not just infrastructure readiness.
2. **Region-aware capability checks at runtime**: Where feasible, query or configure known regional availability per tool/feature and route requests accordingly, rather than discovering the gap via a failed call.
3. **Explicit fallback sized for the actual failure volume**: Ensure fallback paths (like manual review) are provisioned to handle the case where an entire region's traffic falls back simultaneously, not just occasional individual failures.
4. **Region-specific vendor selection**: For capabilities with known regional gaps, maintain a secondary vendor or approach specifically for unsupported regions rather than assuming one vendor covers global operations.
5. **Test from representative regional infrastructure**: Include staging/testing traffic originating from (or tagged as) each deployment region, not just the engineering team's home region, to surface regional gating before production rollout.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.region_unavailable_error_rate` | Rate of region-specific unavailability errors from a tool, broken down by region | Alert on any occurrence in production |
| `fallback.volume_by_region` | Volume of requests routed to fallback/manual paths, segmented by region | Alert when any single region's fallback volume spikes above its provisioned capacity |
| `expansion.unaudited_dependency_count` | Count of tool dependencies not yet verified for availability in a newly launched region | Alert on any nonzero count before a regional launch |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Region-wide feature unavailability detected | `region_unavailable_error_rate` spikes for a specific region | High | Confirm regional gating with vendor, activate region-specific fallback/vendor |
| Fallback capacity exceeded for a region | `fallback.volume_by_region` exceeds provisioned manual-review or backup capacity | Critical | Scale fallback capacity immediately, escalate to vendor for regional support timeline |

## Related Patterns
- [Feature Flag Disabled](./feature-flag-disabled.md) - same "capability gap invisible until exercised in the affected context" pattern, account-level instead of region-level
- [Paid Feature Cost Not Disclosed](./paid-feature-cost-not-disclosed.md) - another undisclosed constraint tied to account/region configuration rather than the API contract itself
- [Sla Availability Not Met](../../tool-sla-quality-limits/failures/sla-availability-not-met.md) - related but distinct: regional unavailability is a permanent gap, not a transient outage
