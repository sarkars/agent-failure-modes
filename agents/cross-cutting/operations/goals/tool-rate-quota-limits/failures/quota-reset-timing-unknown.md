# Quota Reset Timing Unknown

## Issue
A tool enforces a quota (daily, hourly, or otherwise) but the vendor does not precisely document when the window resets — the docs might say "resets daily" without specifying a time zone, or "rolling window" without specifying the exact rolling mechanism. Without a precise reset time, the agent cannot safely schedule retries or backoff near the boundary: it either retries too early (wasting an attempt against a still-exhausted quota) or waits too conservatively long (leaving the tool idle for extra time after it actually became available again).

**Frequency**: Common

**Symptoms**
- Retries scheduled for "midnight" or "the top of the hour" based on an assumption sometimes succeed and sometimes still get rejected, with no consistent pattern
- The agent's calculated wait-until time and the tool's actual reset time drift apart over days/weeks, even though nothing in the agent's config changed
- Support documentation says only "quota resets every 24 hours" with no stated time zone or anchor point (account creation time? UTC midnight? first-request time?)
- Empirically observed reset times shift depending on which region/data-center serves the request, suggesting the reset isn't globally synchronized
- The agent's operators have resorted to trial-and-error logging to reverse-engineer the actual reset schedule

## Root Cause
Vendors are inconsistent about publishing exact quota reset semantics — some reset at a fixed UTC time, some at an account-relative anchor (e.g., "24 hours after account creation" or "24 hours after first use each cycle"), some use a genuinely rolling window with no fixed reset moment at all. When documentation is silent or vague on this, agent developers are forced to guess, and that guess is baked into scheduling logic as if it were a documented fact rather than an inference — so any mismatch between the guess and the vendor's actual behavior surfaces as unpredictable retry failures that look like bugs in the agent rather than a fundamentally under-specified external contract.

## Example
```
An agent integrates the "LeadGenAPI" tool, whose documentation states only: "Free tier: 500 requests per day." No time zone, no reset anchor, no rolling-vs-fixed clarification.

The integration team assumes UTC midnight reset (the most common convention) and configures the agent to resume quota-limited work at 00:05 UTC as a small safety buffer.
For the first two weeks, this works perfectly — requests resume cleanly at 00:05 UTC every day.
In week three, LeadGenAPI's actual reset is discovered (via a vendor support ticket) to be anchored to each account's *first request timestamp after signup*, not UTC midnight — it happened to align with UTC midnight only because the account was originally provisioned and first used near that time.
When a maintenance change causes the very first request of a new day to fire slightly earlier one day, the "anchor" quietly shifts, and the agent's 00:05 UTC resume time now lands about 40 minutes before the real reset, causing every retry attempt in that window to fail against the still-exhausted prior day's quota.
The team has no way to detect this shift proactively since the vendor never documents or exposes the actual per-account reset timestamp.
```

## Statistics
| Finding | Context |
|---------|---------|
| A substantial share of third-party API providers — commonly estimated around a third to half of smaller or less mature SaaS APIs — document quota periods ("daily," "per month") without specifying an exact reset time or anchor | Common in API documentation across SaaS tooling |
| Agents that hardcode an assumed reset time without vendor confirmation see periodic retry failures that recur unpredictably, often traced back weeks later to an incorrect boundary assumption | Observed pattern in production integrations |
| Empirically discovering and periodically re-validating the actual reset time (via response headers or repeated probing) rather than relying solely on documentation eliminates the majority of boundary-guess-driven failures | Typical outcome of empirical-discovery remediation |

## Mitigations
1. **Prefer vendor-provided reset headers over documentation guesses**: If the API returns any `X-RateLimit-Reset`, `Retry-After`, or similar header on responses (even non-error ones), parse and use that value as the authoritative reset time rather than a hardcoded assumption from prose documentation.
2. **Empirically probe and log the actual reset time**: When no reliable header exists, instrument the agent to record the exact timestamp quota becomes available again after each exhaustion event, building an observed-reset-time history that's more trustworthy than vague docs.
3. **Add a conservative safety buffer, and revisit it periodically**: Whatever reset time is assumed, add a buffer (start retrying a few minutes after the assumed boundary, not exactly at it) and periodically re-validate the assumption against actual observed behavior, since vendor-side reset anchors can drift or change without notice.
4. **Escalate ambiguous documentation to the vendor directly**: File a support request asking for the precise reset mechanism (fixed UTC time vs rolling vs account-anchored) and record the answer in integration notes — treat vendor-confirmed timing as more reliable than either public docs or inference.
5. **Design retry logic to be reset-time-agnostic where possible**: Use exponential backoff with a capped maximum interval instead of a single precisely-timed retry-at-reset attempt, so that even without knowing the exact reset time, the agent converges on resuming shortly after quota actually becomes available rather than depending on a single correctly-timed guess.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.observed_reset_time_variance` | Variance in empirically observed reset timestamps over a rolling 14-day window | Alert if variance exceeds 15 minutes, indicating the assumed anchor is unstable |
| `tool.premature_retry_rejection_count` | Count of retries scheduled at the assumed reset time that were still rejected | Alert if greater than 0 in any reset cycle |
| `tool.post_reset_idle_time_s` | Time between actual quota availability (first successful post-reset call) and the agent's first retry attempt | Alert if consistently over 5 minutes, indicating an overly conservative buffer |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Reset time assumption invalidated | A retry at the assumed reset time is rejected while a later retry succeeds | Warning | Re-probe and update the assumed reset time/anchor; consider filing a vendor support request |
| Reset anchor drift detected | `observed_reset_time_variance` exceeds threshold across multiple cycles | Warning | Investigate whether the vendor's reset is account-anchored and has shifted; adjust scheduling buffer |

## Related Patterns
- [Quota Reset During Operation](./quota-reset-during-operation.md) - not knowing the exact reset time makes it harder to detect when a long operation is about to straddle one
- [Quota Reset Boundary Race](./quota-reset-boundary-race.md) - imprecise reset timing knowledge compounds the inconsistency multiple agent instances see when racing a boundary
- [Rolling Window Quota Misunderstanding](./rolling-window-quota-misunderstanding.md) - one specific and common form of "unknown reset timing" is mistaking a rolling window for a fixed one
