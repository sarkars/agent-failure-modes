# Output Length Not Enforced

## Issue
An agent generates output without any hard cap on its length, and a downstream consumer with an actual limit — a database column with a fixed `VARCHAR` size, a UI element with a character budget, an SMS/notification channel with a payload cap, a third-party API with a field-length restriction — receives output that exceeds it. Depending on the consumer, this either causes a hard rejection (a database `INSERT` failing, an API returning a 400) or, worse, a silent truncation somewhere in the chain that the agent itself has no visibility into and cannot compensate for.

**Frequency**: Common

**Symptoms**
- Database write failures for a specific field, correlated with agent-generated content rather than user input
- Notifications/SMS/push messages that are silently cut off mid-sentence when delivered
- Third-party API integrations rejecting requests with "field exceeds maximum length" errors on a subset of calls
- UI elements that overflow, wrap unpredictably, or get clipped by CSS `overflow: hidden` because the agent's text was never bounded to fit the space
- Length-related failures that correlate with more complex/detailed input, since verbose input tends to elicit correspondingly longer generated output

## Root Cause
Generative models don't inherently know the byte or character budget of whatever system will eventually receive their output — that constraint lives in a downstream schema or UI spec that the agent's prompt or generation configuration may not encode at all. Unless the calling code explicitly instructs the model to stay within a specific length and then verifies the actual output against that bound (rather than trusting the instruction alone), there's nothing structurally preventing the model from producing a response that's accurate and well-formed but simply longer than what the consumer can accept — especially for open-ended generation tasks like summaries or descriptions, where "longer and more thorough" and "correct" often pull in the same direction from the model's perspective.

## Example
```
An agent generates SMS appointment-reminder text from a structured
appointment record, aiming to include the provider name, date, time, and
a rescheduling link. The downstream SMS gateway silently truncates any
payload over 160 characters into a second message segment, and the
receiving carrier on some networks drops the second segment if it
arrives out of order.

For a straightforward appointment, the agent's generated text fits
comfortably in 160 characters. For an appointment with a provider whose
name is unusually long and a rescheduling link that includes an
appointment-specific query parameter, the generated text runs to 214
characters:

    "Reminder: your appointment with Dr. Alexandra Whitmore-Fitzgerald,
    Advanced Dermatology & Cosmetic Surgery Associates, is scheduled for
    July 22 at 2:30 PM. To reschedule, visit: https://booking.example.
    com/reschedule?apt=88214471&t=a8f3e91c"

The SMS gateway splits it into two segments; the second segment
(containing the actual reschedule link) arrives out of order on one
carrier and is dropped. The patient receives a reminder with no working
link and no indication a link was ever supposed to be included.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of downstream field-length rejection errors in agent-generated-content pipelines correlate with above-median output length, not with erroneous content | Typical range observed in integration error logs |
| SMS/notification channels are disproportionately represented in length-related delivery failures due to hard per-segment character limits | Common pattern in messaging-integration incident data |
| Enforcing a generation-time length instruction plus a post-generation hard truncation/rejection check substantially reduces downstream length failures | Estimated from the layered nature of the fix relative to relying on prompting alone |

## Mitigations
1. **Enforce length as a post-generation check, not just a prompt instruction**: Treat any length constraint mentioned in the prompt as a soft preference, not a guarantee, and add an explicit post-generation check that measures actual output length against the real downstream limit.
2. **Fail or regenerate on overflow, don't blind-truncate downstream**: When generated output exceeds the limit, either regenerate with an explicit "must fit in N characters" retry (ideally with the overflow amount specified) or route to a review queue, rather than letting a downstream system's own truncation behavior decide what gets cut.
3. **Model the actual downstream budget, including overhead**: Account for any fixed prefix/suffix, encoding overhead (multi-byte characters counting as more than one unit in some SMS/Unicode contexts), or template wrapper text when computing the available budget for agent-generated content.
4. **Prefer channels with generous or no hard limits for variable-length content**: Where content length is inherently unpredictable (descriptions, summaries), route to a channel without a hard truncation risk (e.g. a web link instead of inline SMS text) rather than forcing variable content into a fixed-size channel.
5. **Length-distribution monitoring by content type**: Track the length distribution of agent-generated content feeding each downstream channel, and set alerts before the distribution's tail starts exceeding known channel limits.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| output_length_overflow_rate | Share of agent-generated outputs exceeding the known downstream length limit | Alert if > 1% |
| downstream_length_rejection_count | Count of downstream systems rejecting content specifically for exceeding a length constraint | Alert if > 0 sustained |
| multi_segment_delivery_rate | Share of message-channel deliveries requiring multi-segment splitting | Informational; correlate with delivery-failure rate |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Generated output exceeds hard downstream limit | Agent output measured against the actual consumer's length limit exceeds it | High | Block delivery, trigger regeneration or truncation-with-signal, log for prompt tuning |
| Length overflow rate trending upward | output_length_overflow_rate for a given content type rises above historical baseline | Medium | Review recent prompt or model changes affecting verbosity |

## Related Patterns
- [Output Truncation Silent](./output-truncation-silent.md) - the frequent downstream consequence when unenforced length overflow meets a consumer that truncates without signaling
- [Input Size Not Validated](./input-size-not-validated.md) - the mirror-image failure on the input side, where an oversized payload isn't rejected before processing
- [Output Format Not Validated](./output-format-not-validated.md) - length is one specific dimension of the broader problem of not validating output against a downstream contract
