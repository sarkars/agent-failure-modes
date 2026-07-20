# Dependency Availability Region

## Issue
An agent's toolchain depends on a third-party service, model endpoint, or package registry that is not available in every region the agent is deployed to — due to data residency law, provider infrastructure gaps, or export restrictions. The dependency works fine in development and in the primary deployment region, so the regional gap goes unnoticed until the agent is deployed or scaled into a new region and a specific tool call starts failing for every user in that geography.

**Frequency**: Occasional

**Symptoms**
- A tool call or API integration fails with connection errors or 403s only for traffic originating from, or routed through, specific regions
- The failure is invisible in the primary region's monitoring dashboards, since aggregate error rates stay low relative to total traffic
- Users in an affected region silently receive a degraded experience (a feature quietly disabled, a fallback path with lower quality) with no clear error surfaced
- The gap is discovered reactively, during a regional expansion launch or a customer complaint, rather than proactively during planning
- Legal/compliance teams flag a data residency violation after discovering the agent was routing regional user data to an unauthorized region's endpoint to work around unavailability

## Root Cause
Regional availability is a property of the third-party provider's own infrastructure and legal footprint, not something the calling application controls, and it is rarely tested because development and initial launch happen in a single well-supported region. Teams building the dependency integration typically hard-code a single endpoint or assume global availability because that assumption holds for the region they test in, and provider documentation about regional restrictions is often buried in terms-of-service or infrequently consulted compliance pages rather than surfaced in the SDK or API error messages in an obvious way. The failure only becomes visible when the deployment footprint expands past the region the integration was implicitly designed for.

## Example
```
A customer-support agent uses a third-party sentiment-analysis API as a tool
call to triage incoming tickets. The integration was built and tested
entirely against the company's US-East deployment, where the sentiment API
has full availability and low latency.

The company launches the same agent for its EU customer base, routing EU
traffic to an EU-hosted deployment for data residency compliance. The
sentiment-analysis provider's EU endpoint, however, only supports a subset
of the languages the US endpoint supports, and additionally requires a
separate EU-specific API key that nobody provisioned during the EU launch
because the integration code just pointed at the same global endpoint URL
used in the US.

Every ticket submitted in German or Dutch fails the sentiment-analysis call
with a 403 "region not authorized" error. The agent's fallback path (skip
sentiment scoring, route to a general queue) kicks in silently, so no
alert fires -- but EU tickets are now being triaged without sentiment
signal, causing high-urgency tickets to sit in the general queue for hours
instead of being fast-tracked, a degradation nobody notices until an EU
customer escalates a delayed response.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of agent integrations relying on third-party APIs have at least one region where the dependency is unavailable or restricted | Typical range observed in multi-region deployment audits |
| Regional availability gaps are disproportionately discovered during launch weeks for new geographies rather than through proactive testing | Estimated from incident timing patterns in regional expansion postmortems |
| Silent fallback paths mask an estimated 50%+ of regional availability incidents from standard error-rate monitoring, since aggregate error rates stay low | Estimated from comparison of user-reported vs. monitoring-detected regional incidents |

## Mitigations
1. **Region-aware dependency inventory**: Maintain an explicit inventory of every third-party dependency's supported regions/data-residency zones, checked against the agent's actual and planned deployment footprint before each regional launch.
2. **Pre-launch regional smoke tests**: Run integration tests against every dependency from within each target region (or via region-simulating test infrastructure) before enabling agent traffic there, not just from the primary development region.
3. **Explicit, loud fallback signaling**: When a regional dependency gap forces a fallback path, emit a distinct, monitored signal (not just a silent degrade) so the gap is visible in dashboards even though the immediate request still succeeds.
4. **Regional error-rate segmentation**: Break out error-rate and success-rate monitoring by request origin region, not just in aggregate, so a 100% failure rate in a small region doesn't get diluted into an unnoticed rounding error globally.
5. **Compliance-reviewed dependency onboarding**: Require new third-party dependencies to go through a data-residency and regional-availability review before integration, as part of the same process that reviews licensing and security.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| region_segmented_error_rate | Error rate for a given dependency, broken out by request origin region | Alert if any region's rate exceeds 5x the global baseline |
| fallback_path_activation_rate_by_region | Rate at which the fallback path activates, segmented by region | Alert if any region's rate is disproportionately high relative to others |
| dependency_region_coverage_gap_count | Count of deployment regions where a used dependency has no verified availability | Alert if > 0 for any active deployment region |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Regional dependency failure spike | A dependency's error rate in a specific region exceeds threshold while global rate stays low | High | Investigate regional availability, activate documented fallback, notify affected users if degraded |
| New region launch without dependency review | A deployment expands to a new region without a completed dependency availability audit | Medium | Block launch or require expedited review before enabling full traffic |

## Related Patterns
- [Dependency Breaking Change](./dependency-breaking-change.md) - both involve a dependency's provider making a decision (a breaking change or a regional restriction) the consuming team doesn't control or get advance notice of
- [Integration Timeout Mismatch](./integration-timeout-mismatch.md) - regional routing to a farther-away available endpoint can introduce latency that trips timeout assumptions tuned for the primary region
- [Dependency Version Conflicts](./dependency-version-conflicts.md) - both are dependency properties invisible in single-environment testing that only surface under a specific deployment configuration
