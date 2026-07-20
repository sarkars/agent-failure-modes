# Input Timezone Ambiguity

## Issue
An agent receives a timestamp or time-of-day value with no explicit timezone, or with a timezone abbreviation that is genuinely ambiguous (e.g. "CST" meaning Central Standard Time or China Standard Time), and interprets it using an assumed timezone — usually the server's local time, UTC, or the timezone of whichever user the agent most recently interacted with — that doesn't match what the source actually meant. The resulting timestamp is a valid, well-formed datetime that is simply wrong by however many hours separate the assumed and actual timezones.

**Frequency**: Common

**Symptoms**
- Scheduled actions (reminders, meeting invites, deadline enforcement) firing at the wrong wall-clock time for the affected user
- Off-by-several-hours discrepancies that are consistent in direction and magnitude (matching a specific timezone offset) rather than random
- Issues that cluster around users/systems in timezones other than the one the agent's infrastructure defaults to
- "CST", "IST", or other ambiguous abbreviations appearing in logs where the intended timezone can't be determined after the fact
- Daylight-saving transition dates producing a one-hour discrepancy that non-DST dates don't show

## Root Cause
A timestamp string without an explicit UTC offset or IANA timezone identifier (e.g. `2026-07-19T14:00:00` instead of `2026-07-19T14:00:00-05:00` or with a zone like `America/Chicago`) carries no self-contained information about which timezone it was authored in — any interpretation the agent applies is a guess informed by context that may or may not be available or correct. Ambiguous abbreviations compound this: "CST", "IST", and "EST" each map to multiple distinct real-world timezones depending on region, and there's no way to disambiguate from the abbreviation alone. Agents that default to UTC, to the server's local timezone, or to a hardcoded assumption (frequently baked in during development in one region and never revisited) will silently misinterpret any input authored in a different zone, and because the result is a syntactically valid timestamp, no parser error signals the mistake.

## Example
```
A scheduling agent processes a meeting request submitted via a form that
captures the time as free text: "Let's meet at 2pm CST on July 22."

The form's backend stores this as "2026-07-22T14:00:00" with no timezone
attached, because the frontend didn't capture one. The agent's calendar-
invite generator was built and tested by a team in India and defaults
unspecified times to IST (UTC+5:30) rather than the US Central time the
requester actually meant (UTC-5, or UTC-6 outside DST).

The agent creates a calendar invite for 2:00 PM IST, which is 3:30 AM US
Central time -- roughly 10.5 hours off from the requester's intent. The
requester and the three other invitees in US timezones receive a meeting
invite for the middle of the night. Because the invite is technically a
valid, successfully created calendar event, no error surfaces; the
mistake is only caught when a confused invitee replies asking whether the
3:30 AM meeting is real.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of user-facing scheduling incidents attributed to "the meeting was at the wrong time" trace back to a missing or ambiguous timezone at input, not a calendar-system bug | Typical range observed in scheduling-support ticket triage |
| Common timezone abbreviations like "CST", "IST", and "EST" each map to two or more distinct real-world UTC offsets in active use | Standard characteristic of civil timezone naming, not an estimate |
| Requiring explicit UTC-offset or IANA-zone timestamps at ingestion eliminates the large majority of timezone-ambiguity incidents | Estimated from the elimination of guesswork once the offset is explicit |

## Mitigations
1. **Mandate explicit offsets or IANA zone identifiers at ingestion**: Require every timestamp entering the system to carry an explicit UTC offset or IANA timezone name (`America/Chicago`, not "CST"), converting from free-text or ambiguous input immediately at the boundary rather than deep in business logic.
2. **Capture timezone context alongside the timestamp**: When time is captured via a form or conversational input, also capture (or infer from user profile/locale/IP) the timezone context explicitly, rather than parsing the time value in isolation.
3. **Never assume server-local or developer-region timezone as default**: Treat any missing-timezone timestamp as invalid input requiring clarification, rather than silently defaulting to UTC, server-local time, or the timezone the system happened to be built in.
4. **Disambiguate abbreviations against a maintained mapping with regional context**: If abbreviations must be accepted, maintain an explicit mapping disambiguated by the request's regional context (user locale, phone number country code, IP geolocation) rather than a single global default.
5. **Round-trip confirmation for user-facing scheduling**: For high-stakes scheduling actions, echo back the interpreted time in an unambiguous format (with both the origin timezone and UTC) for user confirmation before committing the action.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| missing_timezone_input_rate | Share of ingested timestamps with no explicit UTC offset or zone identifier | Alert if > 1% |
| ambiguous_abbreviation_rate | Share of ingested timestamps using an ambiguous zone abbreviation | Alert if > 0 for high-stakes scheduling flows |
| scheduled_action_time_correction_rate | Rate of scheduled actions manually rescheduled after being flagged as wrong-time | Alert on sustained upward trend |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Timestamp missing timezone in high-stakes flow | A scheduling or deadline-enforcement action is created from a timestamp with no explicit timezone | High | Block the action pending clarification, request explicit timezone from source |
| DST-transition discrepancy spike | Scheduled-action complaints cluster around a daylight-saving transition date | Medium | Audit timezone-conversion logic for DST handling correctness |

## Related Patterns
- [Input Locale Mismatch](./input-locale-mismatch.md) - a related temporal/numeric misinterpretation failure, often co-occurring with timezone ambiguity in the same input
- [Input Default Value Assumption](./input-default-value-assumption.md) - defaulting to a server-local or hardcoded timezone is a specific instance of the broader unsafe-default pattern
- [Output Inconsistency](./output-inconsistency.md) - inconsistent timezone handling across calls can produce differently-formatted timestamps for logically identical inputs
