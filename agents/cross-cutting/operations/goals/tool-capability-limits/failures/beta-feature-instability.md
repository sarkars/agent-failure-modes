# Beta Feature Instability

## Issue
An agent depends on a tool capability explicitly marked beta, preview, or experimental. Because beta features carry no stability guarantee, the vendor can change their behavior, response format, or accuracy characteristics between releases — or pull the feature entirely — without the deprecation notice period given to generally-available (GA) functionality. The agent, having no built-in concept of "this dependency is inherently unstable," treats the beta feature the same as any GA capability and has no fallback when it changes shape or disappears.

**Frequency**: Occasional

**Symptoms**
- A previously working call to a beta endpoint starts returning a different response structure with no announced schema change
- The beta feature is suddenly unavailable (404 or "feature not enabled") for accounts that had access days earlier
- Output quality or format from a beta ML/generative feature shifts noticeably between calls with no code or prompt change on the agent's side
- Vendor documentation for the beta feature is updated or removed with no corresponding changelog entry the agent's team was subscribed to
- The feature works in a staging/sandbox environment but behaves differently or is absent in production, or vice versa

## Root Cause
Beta and preview labels exist precisely so vendors can iterate quickly without the compatibility commitments of a GA release — this is a deliberate tradeoff the vendor makes, not an oversight. Vendors rarely apply the same deprecation-notice SLA to beta features that they apply to GA ones, so breaking changes can ship with days of notice or none. Agents built during a project's early stages often reach for beta features because they're the newest or most capable option available at build time, without the team recording anywhere that this specific dependency needs elevated monitoring or a documented fallback path, so the risk stays invisible until it materializes as a production break.

## Example
```
1. An agent uses a document-AI vendor's beta "smart-extract" endpoint to pull structured
   fields out of scanned invoices, chosen because it outperformed the GA "basic-extract"
   endpoint on the team's test set six months ago.
2. The vendor ships a beta update that changes the confidence-score field from a 0-1 float
   to a "high"/"medium"/"low" categorical, and renames `extracted_fields` to `fields_v2`.
3. No deprecation notice is sent for beta-tier features per the vendor's terms of service;
   the change appears only in a beta-specific changelog page the integrating team never
   subscribed to.
4. The agent's downstream logic does `if confidence_score > 0.8: auto_approve()`, which
   now always evaluates false since `confidence_score` no longer exists in the response
   shape (replaced by `fields_v2` internals), silently falling through to manual review
   for every single invoice.
5. Invoice processing throughput drops by 90% as everything routes to manual review;
   the team spends two days investigating before finding the beta changelog entry.
```

## Statistics
| Finding | Context |
|---------|---------|
| Beta/preview API features change their response contract substantially more often than GA features, commonly observed at 3-6x the rate over a comparable time window | Reflects the deliberately lower stability bar vendors set for beta tiers |
| Teams that maintain a documented "beta dependency registry" with fallback plans report meaningfully faster recovery from beta-feature breaks, often citing detection-to-fix times cut by half or more | By having a known fallback path ready rather than improvising during an incident |
| A material share of AI/ML-feature outages in agent pipelines, frequently cited in the 15-25% range, trace back to dependency on a beta-labeled model or feature rather than the GA equivalent | Consistent with beta features being the newest/least battle-tested capability in a given product |

## Mitigations
1. **Maintain a beta-dependency registry**: Explicitly track every beta/preview feature the agent depends on, in a location the team actively monitors, along with its GA equivalent (if any) as a documented fallback.
2. **Subscribe to beta-specific changelogs separately**: Beta changelogs are often maintained separately from GA release notes; subscribe to both and treat beta changelog entries as higher-urgency since they carry no notice-period guarantee.
3. **Contract tests specifically for beta dependencies**: Run more frequent (e.g., daily rather than weekly) automated schema/behavior checks against beta endpoints specifically, since they're the most likely to drift silently.
4. **Graceful degradation to a GA fallback**: Where a GA equivalent exists (even if lower-quality), implement an automatic fallback path so a beta-feature break degrades output quality rather than breaking the pipeline outright.
5. **Avoid beta features on critical-path production dependencies**: Reserve beta features for non-critical or experimental workflows where an agent can afford to run without them temporarily, keeping GA capabilities on the critical path.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `beta_feature.response_shape_drift_count` | Count of responses from a tracked beta endpoint failing schema validation against the last known-good shape | Alert on any occurrence |
| `beta_feature.availability_pct` | Success rate of calls to a tracked beta endpoint | Alert below 95% over a rolling hour |
| `pipeline.fallback_route_rate` | Rate at which downstream logic falls through to a manual/default path due to unexpected beta-feature output | Alert on a sustained jump above baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Beta endpoint schema drift detected | `response_shape_drift_count` > 0 | High | Check beta changelog, switch to documented GA fallback if available |
| Beta feature availability drop | `availability_pct` < 90% for 15 minutes | High | Assume feature may be pulled or degraded; activate fallback path |

## Related Patterns
- [Feature Flag Disabled](./feature-flag-disabled.md) - both involve capability availability the agent cannot verify ahead of the call
- [Deprecated Endpoint Retirement](./deprecated-endpoint-retirement.md) - beta instability is often the precursor stage to eventual GA deprecation and retirement
- [Api Version Schema Mismatch](./api-version-schema-mismatch.md) - the schema-drift symptom is shared, but beta features carry no notice-period guarantee at all
