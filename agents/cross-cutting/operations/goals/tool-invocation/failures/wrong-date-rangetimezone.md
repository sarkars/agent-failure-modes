# Wrong Date Range/Timezone

## Issue: Agent queries or schedules using incorrect date/time boundaries.

**Frequency**: Common

**Symptoms**
- Missing events/data; user sees wrong relative date.
- [Add more specific symptoms]

**Root Cause**
Agent queries or schedules using incorrect date/time boundaries.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Canonical Timezone Normalization at the Boundary**: All date/time inputs (user-stated, agent-inferred) are normalized to an explicit canonical form (UTC plus IANA timezone tag) immediately at the point of parsing, before being passed to any tool; tools never receive ambiguous local-time strings without an accompanying timezone.
2. **Relative-Date Resolution with Explicit "Now" Anchor**: Phrases like "next Monday" or "end of quarter" are resolved against an explicit, injected current-datetime-plus-timezone context (not the model's internal notion of "now"), and the resolved absolute date range is echoed back for the agent to sanity-check before use.
3. **Timezone-Aware Test Suite Across DST Boundaries**: Date-handling logic is covered by tests that specifically exercise daylight-saving transitions, month/year boundaries, and cross-timezone user/tool combinations, since these are where naive date arithmetic silently breaks.

### Detection & Response
1. **Boundary Sanity Assertions**: Constructed date ranges are checked against sanity rules (start < end, range within a plausible span for the query type, not spanning an unintended DST jump) before the tool call fires; violations block the call and prompt re-derivation.
2. **User-Facing Date Echo**: When a date range is inferred from relative language, the resolved absolute range (with timezone) is surfaced back to the user or logged prominently, so silently wrong resolutions are visible and correctable early rather than buried in a tool call.
3. **Missing-Event Complaint Correlation**: User reports of missing calendar events/data are cross-referenced against the date range and timezone actually used in the underlying tool call for that session, quickly confirming or ruling out a timezone/boundary bug versus a data issue.

### Architecture Patterns
1. **Central Date-Resolution Service**: A single shared service handles all relative-date and timezone resolution (given user locale/timezone plus reference "now"), returning canonical UTC plus tz-tagged ranges; individual tools and agent prompts never implement their own ad hoc date parsing.
2. **User-Timezone-Aware Context Injection**: Session context always carries the user's resolved timezone (from profile, browser, or explicit statement) and injects it automatically into any date-related tool call, rather than relying on the agent to remember to ask or infer it each time.
3. **Immutable Absolute-Time Storage**: All scheduled/stored times are persisted in UTC with an explicit source timezone annotation, with local-time conversion happening only at display/query time, preventing DST-related drift from corrupting stored schedules over time.

### Metrics
1. **timezone_missing_on_datetime_input_percent**: Target: 0%; Alert threshold: > 1%
2. **date_boundary_sanity_check_failure_rate_percent**: Target: < 1%; Alert threshold: > 3%
3. **dst_transition_test_pass_rate_percent**: Target: 100%; Alert threshold: < 100%
4. **missing_event_user_reports_per_week**: Target: < 2; Alert threshold: >= 5

### Alerts
1. **Ambiguous Datetime Reached Tool Call** (P1 - Critical): Condition - a tool call was made with a datetime lacking explicit timezone/UTC offset. Action: Block call, force re-resolution through the canonical date service, audit how it bypassed normalization.
2. **Sanity Check Failure Spike** (P2 - Warning): Condition - date_boundary_sanity_check_failure_rate_percent exceeds threshold. Action: Review recent relative-date parsing changes, check for a DST-transition-triggered regression.
3. **Missing-Event Reports Rising** (P3 - Info): Condition - missing_event_user_reports_per_week exceeds threshold. Action: Sample affected sessions, correlate against timezone/date-range used, file a fix if the pattern is confirmed.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
