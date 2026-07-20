# Over-Clarification

## Issue
The agent asks a clarifying question for a request that was already clear enough to act on, forcing the user through an unnecessary extra round-trip before getting the actual work done. Unlike clarification-loop-infinite, which is about a non-terminating sequence of questions, over-clarification can be a single instance: one avoidable question inserted into an otherwise straightforward request, driven by excessive caution rather than genuine ambiguity.

**Frequency**: Very Common

**Symptoms**
- Agent asks about a detail that was already stated, implied unambiguously by context, or has one obviously correct default
- User's reply to the clarifying question is effectively "yes, obviously" or restates something already clear
- Requests with a single reasonable interpretation still trigger a confirmation question before execution
- Users begin over-specifying requests preemptively to avoid the predictable follow-up question
- Time-to-first-output is inflated for a meaningful share of requests that had no real ambiguity

## Root Cause
A model tuned to avoid the cost of a wrong assumption will, absent a calibrated sense of when confidence is already high enough to act, treat any residual uncertainty — however small — as justification to ask rather than proceed. This is often reinforced by training or prompting that rewards asking as a safe, cautious default, without an offsetting penalty for the friction cost of unnecessary questions. Because "is this actually ambiguous enough to need a question" is a probabilistic judgment call rather than a binary check, a model biased toward caution will over-trigger on cases that are clear to a human but not perfectly certain to the model.

## Example
```
User: "Convert this CSV to JSON."

The file has one obvious structure: a header row and consistent
columns, no nested fields, no ambiguity about what "convert to JSON"
means here.

Agent: "Before I convert this, could you clarify: would you like each
row as an object in an array, or as a single object keyed by row
index? And should numeric-looking strings be parsed as numbers or kept
as strings?"

Both questions have an obvious default that would satisfy the vast
majority of users (array of objects, numbers parsed as numbers) and
neither was hinted at as contentious by anything in the request.

User: "...just do the normal thing, whatever that is."
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of clarifying questions asked by conversational agents are judged unnecessary by users when surveyed after the fact | Typical range across support/task agent deployments |
| Requests answered with an unnecessary clarifying question show measurably higher abandonment before task completion than requests acted on directly | Estimated from production funnel analysis |
| Calibrating confidence thresholds for when to ask (rather than defaulting to always-ask on any uncertainty) reduces unnecessary questions substantially without a proportional rise in wrong-assumption errors | Reported range across teams that tuned ask-thresholds |

## Mitigations
1. **Confidence-threshold calibration**: Only trigger a clarifying question when the agent's confidence in the most likely interpretation falls below an explicit threshold, rather than whenever any alternative interpretation is theoretically possible.
2. **Default-with-visible-assumption**: For low-stakes ambiguities with an obvious majority-case default, proceed using that default and state it plainly, letting the user correct it if wrong, rather than blocking on a question first.
3. **Stakes-weighted asking**: Reserve pre-execution clarifying questions for cases where a wrong guess would be costly or hard to reverse; for cheap-to-correct outputs, prefer act-then-confirm.
4. **Unnecessary-question feedback loop**: Track cases where a clarifying question's answer simply confirms the obvious default, and use these to recalibrate the ask-threshold for that request pattern.
5. **Single-question consolidation**: When some clarification genuinely is warranted, bundle only the truly ambiguous elements into one question rather than padding it with already-obvious ones.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unnecessary_clarification_rate | Share of clarifying questions whose answer just confirms the obvious default | Alert if > 25% |
| pre_execution_question_rate | Share of requests that trigger a clarifying question before any output is attempted | Alert if trending above category baseline |
| time_to_first_output | Elapsed turns/time before the agent produces substantive output | Alert if rising for low-ambiguity request categories |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Spike in unnecessary clarification | unnecessary_clarification_rate exceeds threshold for a request category | Medium | Review and recalibrate ask-confidence threshold |
| User friction signal on clarification | User response pattern ("just do it," "obviously") detected following a clarifying question | Low | Log for threshold tuning |

## Related Patterns
- [Under-Clarification](./under-clarification.md) - the opposite miscalibration: proceeding without asking when ambiguity genuinely warranted a question
- [Clarification Loop Infinite](./clarification-loop-infinite.md) - repeated over-clarification without a terminating condition escalates into this more severe non-terminating pattern
- [Disambiguation Strategy Ineffective](./disambiguation-strategy-ineffective.md) - over-clarification is one specific mismatch case within the broader set of poorly-fitted disambiguation strategies
