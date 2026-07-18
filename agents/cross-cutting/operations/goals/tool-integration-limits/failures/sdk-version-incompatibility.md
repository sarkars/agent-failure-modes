# Sdk Version Incompatibility

## Issue
The client SDK an agent uses to call a tool falls out of sync with the tool's current server-side API version — because the SDK wasn't updated after a server-side change, or because a dependency pin locked the agent to an old SDK release. Requests and responses that used to serialize and authenticate correctly begin failing in ways that look like network or auth problems (malformed request errors, signature mismatches, unexpected field types) rather than clearly indicating "your client library is out of date."

**Frequency**: Common

**Symptoms**
- Authentication failures or signature-verification errors appear with no change to credentials or secrets
- Serialization errors (unexpected type, unrecognized field, malformed body) on requests that previously worked
- The exact same request succeeds when issued via the vendor's latest SDK or a raw HTTP client, but fails via the agent's pinned SDK version
- Vendor support identifies the issue as "please upgrade to SDK version X.Y" during a support ticket
- The failure onset coincides with a server-side deployment on the vendor's end, not any change to the agent's own code

## Root Cause
Tool vendors evolve their server-side API and expect client SDKs to track it — updating request signing algorithms, adding required headers, or changing serialization conventions — but they don't always maintain strict backward compatibility for old SDK major versions indefinitely. Dependency management practices that pin an SDK to a specific version (for stability) mean the agent doesn't automatically pick up vendor-side compatibility fixes, so a server-side change can silently break an old, pinned SDK without any signal reaching the pinned version's changelog. Because SDKs abstract away the wire protocol, developers debugging the resulting failure often look at their own request-construction logic first, not realizing the SDK itself is the layer that's out of date.

## Example
```
1. An agent uses payment-processor vendor's official Python SDK, pinned at v3.4.0 in
   the project's lockfile for stability, to submit refund requests.
2. The vendor rolls out a server-side security change requiring a new HMAC-based request
   signing scheme, with SDK v4.0.0 released to support it; v3.x SDKs are given a
   6-month compatibility grace period before the old signing scheme is retired.
3. The lockfile is never revisited during the grace period since refunds have been
   working reliably.
4. On the day the old signing scheme is retired server-side, every refund request via
   the pinned v3.4.0 SDK starts failing with "401 Unauthorized: invalid signature."
5. The on-call engineer, seeing a 401, assumes the API key was rotated or revoked and
   spends 40 minutes regenerating and redeploying credentials, which doesn't fix anything
   since the credentials were never the problem.
6. A vendor support ticket eventually surfaces the actual cause: SDK v3.x's signing
   scheme was retired, and upgrading to v4.x resolves the issue immediately.
```

## Statistics
| Finding | Context |
|---------|---------|
| SDK-version incompatibility is a frequent root cause behind authentication failures initially misdiagnosed as credential issues, commonly cited in a meaningful share (15-25%) of such support tickets | Because signature/auth errors look identical regardless of underlying cause |
| Pinned SDK dependencies that go 12+ months without a review are disproportionately represented in incompatibility incidents | Consistent with vendor compatibility grace periods commonly running 6-12 months |
| Automated dependency-freshness checks (flagging SDKs more than N major versions or M months behind latest) have been observed to catch the majority of impending incompatibilities before a vendor-side retirement date | By surfacing staleness proactively instead of reactively |

## Mitigations
1. **Automated SDK freshness monitoring**: Track how far behind the pinned SDK version is from the vendor's latest release, and flag it for review once it crosses a staleness threshold (e.g., 2 major versions or 9 months).
2. **Subscribe to vendor SDK changelogs and compatibility grace-period notices**: Vendor release notes for SDKs often explicitly call out compatibility deadlines for older versions; route these to a monitored channel, not an individual inbox.
3. **Distinguish auth failures from SDK incompatibility during triage**: When an auth-shaped error appears with no corresponding credential change, check SDK version against the vendor's current supported-version list before assuming credentials are the cause.
4. **Regular scheduled SDK upgrade cadence**: Treat SDK upgrades as routine maintenance on a fixed schedule (e.g., quarterly) rather than only upgrading reactively after something breaks.
5. **Test against a raw HTTP call as a diagnostic fallback**: When an SDK-mediated call fails mysteriously, issue the equivalent request via a raw HTTP client to determine whether the failure is in the SDK layer or the underlying API/credentials.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `sdk.version_lag_major_versions` | Number of major versions the pinned SDK is behind the vendor's current release | Alert when lag exceeds 2 major versions |
| `tool_call.auth_error_rate_post_deploy` | Auth/signature error rate correlated with vendor-side deployment windows (from vendor status page, if available) | Alert on any spike coinciding with a known vendor release |
| `sdk.last_upgrade_review_days` | Days since the pinned SDK version was last reviewed for currency | Alert above 270 days (9 months) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| SDK approaching known compatibility deadline | Vendor-announced sunset date for current SDK major version within 60 days | High | Schedule and prioritize SDK upgrade before the deadline |
| Unexplained auth/signature failures after vendor deploy | `auth_error_rate_post_deploy` spikes with no credential change on the agent's side | High | Check SDK version against vendor's current supported list before investigating credentials |

## Related Patterns
- [Plugin Compatibility Matrix](./plugin-compatibility-matrix.md) - closely related: SDK-to-server mismatch versus plugin-to-platform mismatch
- [Api Version Schema Mismatch](../../tool-capability-limits/failures/api-version-schema-mismatch.md) - overlapping cause: an outdated SDK often means an outdated understanding of the wire schema too
- [Deprecated Endpoint Retirement](../../tool-capability-limits/failures/deprecated-endpoint-retirement.md) - SDK incompatibility is frequently the mechanism by which an endpoint's retirement actually manifests as a client failure
