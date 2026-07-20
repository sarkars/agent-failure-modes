# License Expiration Not Checked

## Issue
An agent keeps calling a tool whose license, API key, or subscription has expired, because nothing in the agent's control flow proactively tracks the license's validity period — it only finds out when a call fails. Between expiration and detection, the agent may continue attempting calls (wasting retries on a failure that cannot succeed), silently fall back to degraded behavior, or, in the worst case, keep reporting task success by misinterpreting a licensing rejection as some other recoverable condition.

**Frequency**: Occasional

**Symptoms**
- A tool that worked reliably for weeks or months suddenly fails on every call starting at a specific date, with error text referencing "expired," "subscription lapsed," or "key no longer valid"
- No advance warning generated internally despite the license having a known, fixed expiration date that was set at provisioning time
- Retry logic cycling through identical failed attempts against an expired credential with no escalation
- Renewal was handled manually and off-system (a calendar reminder, an email from the vendor) with no automated linkage to the agent's runtime configuration

## Root Cause
Licenses and API keys are usually provisioned once, during initial setup, and then treated as a static configuration value thereafter — stored in an environment variable or secrets manager and referenced by the agent without any accompanying expiration metadata the agent's own logic can check. The expiration date, if tracked at all, typically lives in a billing system or the vendor's account dashboard, not in the agent's runtime environment, so there's no natural place for the agent to look up "is this credential still valid" before using it. The failure is only discovered reactively, through a failed call, because nothing connects the passage of time to the credential's known validity window in a way the agent's own monitoring can observe in advance.

## Example
```
A market-intelligence agent uses a "NewsFeed Premium" API key,
provisioned under a 12-month subscription that was never set to
auto-renew because procurement preferred a manual renewal process to
review pricing each year.

The subscription lapses at midnight on its anniversary date. The
agent, running its normal hourly news-ingestion job, calls the
NewsFeed API and receives a 401 with body: {"error": "subscription_
expired", "message": "Your NewsFeed Premium subscription ended on
2026-07-19. Renew to continue."}

The agent's error handler, tuned primarily for transient network
errors, retries the call three times with exponential backoff, fails
identically each time, and then logs a generic "ingestion job failed"
error that gets bundled with dozens of other routine job-failure log
lines. No one notices for 6 days, during which the agent's downstream
market-summary reports silently stop including any news-sourced
content, and a stakeholder only notices when a report is missing an
expected story about a competitor's product launch.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-15% of manually-renewed (non-auto-renewing) tool subscriptions used by production agents lapse at least once due to missed renewal | Typical range observed in operations reviews of tool-credential lifecycle management |
| Median time-to-detection for a lapsed license with no proactive monitoring is measured in days, especially for tools whose failure degrades output quality rather than causing an obvious hard crash | Estimated from incident postmortems involving expired credentials |
| Adding expiration-date tracking with advance-warning alerts (30/7/1 day) largely eliminates unplanned lapses in credential validity | Reported range across teams instituting credential lifecycle monitoring |

## Mitigations
1. **Expiration metadata alongside credentials**: Store each tool credential's known expiration date in the same system as the credential itself (secrets manager, config), so it can be programmatically checked rather than living only in a vendor dashboard.
2. **Proactive expiration alerts**: Set up automated alerts at multiple lead times before expiration (30 days, 7 days, 1 day) so renewal happens before the credential lapses, not after a failure is noticed.
3. **Non-retryable error classification for auth/licensing failures**: Explicitly classify 401/403 responses referencing subscription or license status as non-retryable and escalate immediately, rather than cycling through a generic retry policy.
4. **Auto-renewal by default where available**: Prefer auto-renewing subscriptions for tools critical to agent operation, reserving manual renewal review for lower-stakes or cost-sensitive tools where a controlled lapse window is acceptable.
5. **Periodic credential health check**: Run a scheduled, low-cost validation call against each critical tool credential (independent of normal task traffic) specifically to surface expiration or revocation early, rather than relying on task failures to surface it.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| days_to_credential_expiration | Time remaining before a tracked credential's known expiration date | Alert if < 30 days |
| auth_failure_rate_by_tool | Rate of authentication/authorization failures per tool | Alert if > 0% sustained for a previously stable tool |
| expired_credential_retry_count | Count of retries attempted against a call that failed due to expired licensing | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Credential nearing expiration | days_to_credential_expiration falls below the 30/7/1-day thresholds | Medium/High (increasing as expiration nears) | Notify credential owner to initiate renewal |
| Tool failing on licensing error | A previously healthy tool begins failing all calls with an expiration/subscription-lapsed error | High | Escalate immediately, halt retries, initiate emergency renewal or switch to fallback tool |

## Related Patterns
- [Feature Entitlement Limit](./feature-entitlement-limit.md) - a related failure where the account is still valid but lacks entitlement to a specific feature, versus the whole credential being invalid here
- [Concurrent Session Not Licensed](./concurrent-session-not-licensed.md) - both involve licensing constraints the agent has no proactive visibility into until a call fails
