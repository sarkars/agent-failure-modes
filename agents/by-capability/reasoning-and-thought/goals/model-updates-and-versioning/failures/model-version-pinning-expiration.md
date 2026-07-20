# Model Version Pinning Expiration

## Issue
A team deliberately pins their agent to a specific, named model snapshot (e.g. an API model string like `gpt-x-2025-01` or a fixed checkpoint hash) to get reproducible, stable behavior — and then the provider deprecates or sunsets that exact snapshot on its own timeline, months later, forcing an unplanned migration. The pin was the right call at the time (it protected the agent from exactly the kind of silent behavior drift that floating model references cause), but the pin has an expiration date the team didn't track, and when the provider's sunset date arrives, every request against that model string starts failing or auto-redirects to a newer version the team never evaluated.

**Frequency**: Common

**Symptoms**
- Requests to a pinned model version start returning deprecation errors, or are silently auto-routed to a different version, on a date the team did not have on any calendar
- The team discovers the deprecation from a failed production request rather than from proactively tracking the provider's model lifecycle page
- The forced migration happens under incident pressure (production is down) rather than as a planned, evaluated cutover
- Multiple pinned snapshots across different agents/services in the same organization expire at different, untracked times, so migrations happen piecemeal and reactively rather than on a predictable cadence
- Provider communicates the deprecation via a changelog, email, or dashboard banner that the team's on-call process has no mechanism to ingest as an actionable alert

## Root Cause
Pinning to a specific model snapshot trades one risk (silent behavior drift from an unpinned/floating reference) for a different, deferred risk: the pinned snapshot is a resource the provider controls and will eventually retire, typically to reclaim serving capacity for older model generations. Because the pin was adopted specifically to avoid dealing with model changes, teams often treat the pinned reference as a fixed point requiring no further attention — the opposite of the truth, since a pin is a lease with an expiration date set by a party other than the team relying on it. Without an explicit process that tracks each pinned model's provider-published deprecation timeline as an operational input (the same way a TLS certificate expiration or a domain renewal would be tracked), the expiration is discovered only when it actively breaks production.

## Example
```
A contract-review agent pins to a specific model snapshot after an
earlier incident where a floating "latest" alias silently changed
behavior mid-quarter. The pin is treated as the fix and the incident
is closed; no one adds the snapshot to any tracked-expiration list.

Four months later, the provider announces (via a changelog entry and a
90-day-advance email to the account's billing contact, not the
engineering team) that the pinned snapshot will be retired.

Day 91: the pinned model string starts returning
"model_deprecated" errors on every request. The contract-review
agent's entire request path fails simultaneously, in production,
with no warning to the on-call engineer, who has no context on why a
model string that "never changes" suddenly stopped working.

The team scrambles to identify a replacement version, evaluate it
against their task-specific test set, and redeploy — compressing what
should have been a planned, tested migration into a same-day incident
response, while the agent is fully down for contract-review requests.
```

## Statistics
| Finding | Context |
|---|---|
| Pinned model snapshots are commonly retired by providers within a 6-18 month window of their original release | Typical range observed across major LLM API providers' published deprecation cadences |
| A large share of pinned-model deprecation incidents are discovered via a failed production request rather than proactive tracking | Estimated from postmortems of model-deprecation incidents |
| Teams that maintain an explicit inventory of pinned model versions with tracked expiration dates report substantially fewer reactive, incident-driven migrations | Reported range across teams comparing tracked vs. untracked pinning practices |

## Mitigations
1. **Treat pinned model versions as tracked, expiring resources**: Maintain an explicit inventory of every pinned model snapshot in use, each with its provider-published deprecation/sunset date, reviewed on the same cadence as certificate or credential expiration tracking.
2. **Subscribe engineering (not just billing) contacts to provider deprecation calendars**: Ensure the team that owns the agent — not just the account's billing or admin contact — receives and actionably tracks provider deprecation notices for every model version depended on.
3. **Eval-harness regression testing before any model swap**: Before migrating off a soon-to-expire pinned version, run the task-specific evaluation suite against the candidate replacement and compare results, so the forced migration doesn't also introduce an unvetted accuracy regression on top of the deadline pressure.
4. **Canary the replacement version ahead of the deadline**: Route a small percentage of traffic to the intended replacement version well before the pinned version's sunset date, so the migration is validated on live traffic while there is still time to choose a different replacement if needed.
5. **Build migration lead time into the pinning decision itself**: When first choosing to pin, record the provider's typical support window for that model family and schedule a re-evaluation checkpoint well before the expected sunset, rather than treating the pin as a one-time decision with no revisit date.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| pinned_model_days_to_deprecation | Days remaining before the provider's published sunset date for each pinned model version in use | Alert when remaining days drop below the team's minimum safe migration lead time |
| deprecated_model_error_rate | Rate of requests failing with a model-deprecation or model-not-found error | Alert on any nonzero rate in production |
| untracked_pinned_version_count | Count of model versions in use that do not appear in the tracked-pin inventory | Alert if greater than zero |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Pinned model nearing sunset | pinned_model_days_to_deprecation crosses the minimum lead-time threshold | High | Begin evaluation and canary of a replacement version immediately |
| Deprecated model error spike in production | deprecated_model_error_rate becomes nonzero | Critical | Treat as a production outage; expedite emergency migration to the tracked replacement candidate |

## Related Patterns
- [Silent Model Update](./silent-model-update.md) - the inverse failure: not pinning (or using a floating alias) leads to unannounced behavior drift, whereas this pattern is the deferred cost of pinning itself
- [Model Update Rollback Delay](./model-update-rollback-delay.md) - a rollback plan is only viable if the target version hasn't already expired, tying the two patterns together operationally
- [Version Pinning Expiration](../../../../../cross-cutting/operations/goals/version-management/failures/version-pinning-expiration.md) - the general software-dependency form of this pattern (npm/pip lockfiles, base image tags, CVEs going stale); this pattern is the ML model/provider-API-specific variant with model-specific mitigations (eval regression testing, canarying) instead of package-patching ones
