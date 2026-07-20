# Deprecated Endpoint Retirement

## Issue
A tool endpoint the agent depends on is formally deprecated by the vendor and, after a notice window, retired outright — returning 404s or 410s instead of the expected response. The agent has no fallback path coded because the endpoint "always worked" during development, so once the retirement date passes, every call fails outright with no graceful degradation, and the failure often isn't noticed until the retirement is already in effect.

**Frequency**: Occasional

**Symptoms**
- Calls that worked reliably for months suddenly start failing with 404 Not Found or 410 Gone on the exact retirement date
- Vendor deprecation emails or changelog entries exist but were sent to an inbox or channel the on-call team doesn't monitor
- The failure is total and immediate rather than gradual — no partial degradation period
- Vendor documentation for the old endpoint has been removed or redirects to a new endpoint with a different request/response shape
- Multiple unrelated agent workflows that happened to use the same deprecated endpoint fail simultaneously

## Root Cause
Vendors typically announce deprecations through channels (email to account owners, changelog pages, developer newsletters) that don't reliably reach the engineers actually operating the agent, especially in larger organizations where the account owner and the integration maintainer are different people. Deprecation notice periods (commonly 6-18 months) create a long gap between the announcement and the actual failure, long enough that the notice is forgotten or the original recipient has moved teams by the time retirement happens. Agents rarely implement a "dead man's switch" that checks whether a dependency is nearing its documented retirement date, so there's no proactive signal until the endpoint simply stops responding.

## Example
```
1. An agent uses a mapping vendor's "/v1/geocode" endpoint to resolve addresses to
   coordinates, integrated three years ago.
2. The vendor announces deprecation of v1 in favor of v2 via an email to the account's
   billing contact and a changelog post, with an 12-month sunset window.
3. The billing contact who received the email left the company 8 months into the window;
   no one else saw the notice.
4. On the sunset date, "/v1/geocode" starts returning 410 Gone for all requests.
5. The agent's address-resolution step, which has no error handling beyond a generic
   retry-with-backoff, retries the 410 repeatedly (each attempt failing identically),
   then surfaces "unable to process order" to end users placing delivery orders.
6. Order processing is down for 90 minutes before an engineer traces the 410 responses
   back to the endpoint retirement and begins an emergency migration to v2.
```

## Statistics
| Finding | Context |
|---------|---------|
| A notable share of production incidents tied to third-party API changes are attributable to deprecated-endpoint retirements rather than unannounced breaking changes, commonly estimated around 25-40% | Consistent with retirements being scheduled but poorly propagated internally |
| Typical vendor deprecation notice windows range from 6 to 18 months, but internal awareness of the notice frequently lapses well before the retirement date | Due to staff turnover and notice channels not reaching operational owners |
| Teams that maintain an internal dependency-and-deprecation calendar report retirement-related incidents at a fraction of the rate of teams without one, often cited as an 80%+ reduction | By converting a vendor-side notice into an internally tracked deadline with an owner |

**Note on scope**: this pattern generalizes beyond a single tool endpoint returning 404/410 — the identical mechanism (notice received, never converted to an owned/dated task, hard failure or silent behavior change on the vendor's schedule) applies equally to library major-version EOL, platform-component sunsets, and model/API version deprecations. Those are domain variants of the same root cause and mitigation set, not separate patterns; track them in the same internal deprecation calendar described above rather than building parallel tracking per dependency type.

## Mitigations
1. **Maintain an internal deprecation calendar**: Track every third-party endpoint dependency with its known deprecation/retirement date (where announced) in a system the operations team actually monitors, not just the vendor's own notification channel.
2. **Route vendor deprecation notices to a monitored channel**: Ensure vendor account settings point deprecation/changelog emails to a team distribution list or ticketing system, not an individual's personal inbox.
3. **Migrate proactively, not reactively**: Treat a deprecation announcement as a scheduled migration task with an owner and a deadline well before the actual sunset date, rather than waiting for the retirement to force the issue.
4. **Automated canary checks against deprecated endpoints**: Run a low-frequency scheduled probe against known-deprecated endpoints to detect early warning signs (elevated latency, intermittent errors) that often precede a hard retirement.
5. **Graceful fallback or circuit breaker on 404/410**: Implement explicit handling for "endpoint gone" responses that fails fast with a clear alert, rather than retrying indefinitely as if it were a transient error.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `endpoint.deprecation_notice_days_remaining` | Days remaining until a tracked endpoint's known deprecation date | Alert at 90 days, 30 days, and 7 days remaining |
| `endpoint.404_410_rate` | Rate of Not Found / Gone responses from any tracked third-party endpoint | Alert on any sustained occurrence above 1% of calls |
| `dependency.unmigrated_deprecated_endpoints_count` | Count of known-deprecated endpoints still in active use past their announced sunset date | Alert on any nonzero count |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Endpoint retirement deadline approaching | `deprecation_notice_days_remaining` crosses 30 days with migration not yet complete | High | Escalate migration task priority, assign owner if unassigned |
| Sudden 404/410 spike on production dependency | `404_410_rate` exceeds 1% for a previously stable endpoint | Critical | Halt retries, check vendor status page/changelog for retirement, execute fallback plan |

## Related Patterns
- [Beta Feature Instability](./beta-feature-instability.md) - deprecation and retirement is often the final stage of the same lifecycle beta instability represents early on
- [Api Version Schema Mismatch](./api-version-schema-mismatch.md) - schema drift frequently precedes and signals an eventual retirement
- [Feature Flag Disabled](./feature-flag-disabled.md) - both leave the agent with no advance detection of a capability disappearing
