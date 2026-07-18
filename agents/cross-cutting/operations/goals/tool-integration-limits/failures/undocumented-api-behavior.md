# Undocumented Api Behavior

## Issue
A tool's actual runtime behavior diverges from what its published documentation describes — an undocumented rate limit far stricter than any documented one, a required field the reference doesn't mention, an implicit ordering constraint, or a response value the docs never enumerate. An agent built strictly against the documentation has no way to anticipate this gap, so it fails against the tool's real behavior in ways that look like a bug in the agent rather than a documentation gap in the tool.

**Frequency**: Very Common

**Symptoms**
- Requests that exactly match the documented schema and examples are rejected with an error that doesn't correspond to any documented validation rule
- The tool enforces a rate limit, size limit, or ordering constraint never mentioned in the published docs, discovered only via trial and error or a 429/400 response
- Two seemingly identical requests produce different results depending on an undocumented factor (account age, data volume, a hidden default)
- Community forums, Stack Overflow, or the vendor's own support tickets contain workarounds for behavior the official docs don't acknowledge
- Behavior changes after a vendor deploy with no corresponding documentation update, so the docs describe old behavior indefinitely

## Root Cause
API documentation is written and maintained separately from the actual server implementation, and the two drift apart over time as the implementation evolves faster than the docs are updated, or as edge-case behavior (internal rate limiting, defensive validation added after an incident, legacy quirks) is never documented in the first place because it wasn't considered part of the "public contract." Agents are typically built by reading documentation and testing against common-case inputs, which rarely exercises the specific edge conditions where undocumented behavior diverges from the documented contract, so the gap remains invisible until a production input happens to trigger it.

## Example
```
1. An agent integrates with a marketing-automation tool's "create-contact" endpoint,
   whose documentation states email is the only required field and that duplicate
   emails are automatically merged.
2. In practice, the endpoint also enforces an undocumented internal rate limit of
   5 requests/second per account (separate from and stricter than the documented
   100 requests/minute limit), applied specifically to write operations during a
   nightly maintenance window the vendor never publicly documents.
3. Agent runs a nightly batch import of 2,000 new contacts starting at 1:00 AM,
   issuing requests at roughly 10/second based on the documented limit.
4. Roughly 40% of requests during the maintenance window silently fail with a generic
   500 error rather than the documented 429 rate-limit response, since the undocumented
   limit is enforced differently than the documented one.
5. The agent's retry logic treats 500 as a generic transient error and retries with
   exponential backoff, eventually succeeding for most contacts but taking 3x longer
   than expected and triggering an on-call page for the extended runtime.
6. A vendor support ticket eventually reveals the undocumented nightly rate-limit
   window, which isn't mentioned anywhere in the public API reference.
```

## Statistics
| Finding | Context |
|---------|---------|
| Undocumented rate limits and validation rules are a frequently cited source of integration friction in developer surveys and support-ticket analyses, often ranking among the top few causes of "the API doesn't behave as documented" complaints | Consistent with docs and implementation being maintained on independent timelines |
| Edge-case and undocumented behavior is disproportionately discovered in production rather than in testing, since test suites rarely exercise the specific rare conditions (unusual data volume, timing windows, account states) where divergence appears | Reflects the gap between common-case testing and full production traffic diversity |
| Teams that maintain an internal "known undocumented behaviors" log for each vendor integration report meaningfully faster resolution of recurring quirks, since the same undocumented gotcha is often rediscovered repeatedly without one | By converting tribal knowledge into a searchable, shared record |

## Mitigations
1. **Maintain an internal "known quirks" log per integration**: Document every undocumented behavior discovered in production (rate limits, hidden required fields, ordering constraints) in a shared, searchable location so it isn't rediscovered from scratch by the next engineer.
2. **Defensive validation and conservative defaults**: Where documentation is ambiguous or thin, code defensively (stricter rate limiting, retries with jitter, explicit field population) rather than assuming the documented minimum is the actual behavior.
3. **Monitor error responses that don't map to documented error codes**: Treat any error code or message not listed in the tool's documented error reference as a signal of undocumented behavior worth investigating and logging, not just retrying blindly.
4. **Cross-check community and support-ticket sources**: Before or during integration, search the vendor's community forum, support-ticket archive, and third-party discussions for known undocumented behaviors others have already hit.
5. **Canary testing against edge-case inputs**: Deliberately test integration behavior against unusual conditions (high volume, boundary values, off-peak timing) during development, not just the documented happy-path examples, to surface divergence before production.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool_call.undocumented_error_rate` | Rate of error responses whose code/message doesn't map to any documented error in the tool's reference | Alert on any sustained occurrence |
| `tool_call.time_window_failure_correlation` | Failure rate segmented by time-of-day/day-of-week, to detect undocumented time-based behavior (e.g., maintenance windows) | Alert when a specific time window shows disproportionate failure rate |
| `integration.known_quirks_log_staleness_days` | Days since the internal undocumented-behavior log was last reviewed or updated for a given integration | Alert above 180 days for actively used integrations |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unrecognized error code pattern emerges | `undocumented_error_rate` rises for a specific error code not in the documented reference | Medium | Investigate and log as a new known quirk; adjust handling logic |
| Time-window-correlated failure spike | Failures cluster in a specific recurring time window with no documented cause | Medium | Suspect an undocumented maintenance window or rate limit; contact vendor support to confirm |

## Related Patterns
- [Api Version Schema Mismatch](../../tool-capability-limits/failures/api-version-schema-mismatch.md) - a specific case of documented-versus-actual divergence, focused on schema rather than behavior generally
- [Webhook Order Not Guaranteed](./webhook-order-not-guaranteed.md) - a common specific instance of undocumented (or under-emphasized) behavior around delivery ordering
- [Plugin Compatibility Matrix](./plugin-compatibility-matrix.md) - undocumented behavior often emerges specifically at unsupported version combinations
