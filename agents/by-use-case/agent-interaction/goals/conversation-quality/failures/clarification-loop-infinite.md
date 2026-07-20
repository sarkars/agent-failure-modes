# Clarification Loop Infinite

## Issue
The agent keeps asking clarifying questions turn after turn without ever committing to an interpretation and proceeding, even after the user has provided enough information to act, or has explicitly said to just make a decision. Each answer the user gives triggers a further question rather than progress, and the conversation never converges on output. This differs from clarification-irrelevant (a wrong single question) in that the loop never terminates at all — the failure is in the stopping condition, not the question content.

**Frequency**: Occasional

**Symptoms**
- Three or more consecutive agent turns are all questions, with no attempted output in between
- User explicitly says "just pick one" or "use your best judgment" and the agent asks another question anyway
- Each new question is only marginally different from the previous one, re-litigating settled points
- Session ends in user abandonment rather than task completion
- Confidence in the agent's stated understanding does not visibly increase across the loop despite additional answers being provided

## Root Cause
An agent whose "ask vs. act" decision is re-evaluated independently at every turn, with no memory of how many clarification rounds have already occurred or how much residual ambiguity actually remains, will treat every turn as reason enough to ask if any uncertainty exists at all — and near-total certainty is rarely achievable. Without an explicit budget on clarification rounds or a decreasing threshold that eventually forces a best-effort attempt, the model's bias toward avoiding a wrong answer dominates indefinitely, because asking one more question always looks locally safer than committing, even when it is globally worse for the user.

## Example
```
User: "Set up a recurring reminder for my team meeting."

Agent: "What day of the week is the meeting?"
User: "Tuesdays."

Agent: "What time on Tuesdays?"
User: "10am."

Agent: "Is that 10am in your local timezone or UTC?"
User: "Local, obviously. Just set it up."

Agent: "Should the reminder fire the same day or the day before?"
User: "I don't care, just pick something reasonable."

Agent: "Would you like the reminder to repeat weekly indefinitely, or
should it have an end date?"

User: "I already told you to use your best judgment. Forget it."
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-10% of clarification-initiating sessions exceed 3 rounds without producing output | Typical range across conversational agent deployments |
| Sessions with 4+ consecutive clarifying questions show abandonment rates several times higher than single-question sessions | Estimated from production session logs |
| Enforcing a hard clarification-round cap with forced best-effort fallback eliminates the large majority of infinite-loop sessions | Reported range across teams that added round budgets |

## Mitigations
1. **Clarification round budget**: Cap the number of consecutive clarifying questions (e.g. 2) before the agent must proceed with its best current interpretation, explicitly flagging any remaining uncertainty in the output instead of asking again.
2. **Explicit override detection**: Recognize phrases like "just pick one," "use your judgment," or "I don't know, you decide" as an instruction to stop asking and proceed immediately, overriding any pending uncertainty check.
3. **Diminishing-returns tracking**: Track how much each answer actually reduced ambiguity; stop asking once additional questions yield negligible narrowing of the interpretation space.
4. **Default-with-caveat fallback**: When the budget is reached, have the agent choose reasonable defaults for remaining unknowns and state them plainly, rather than silently guessing or asking indefinitely.
5. **Loop detection on question similarity**: Compare each new candidate question against previously asked ones; block near-duplicate questions from being sent and force a decision instead.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| consecutive_clarification_turns | Max consecutive agent turns that are questions within a session | Alert if > 3 |
| clarification_abandonment_rate | Share of sessions ending without output after 2+ clarifying questions | Alert if > 15% |
| override_ignored_rate | Rate at which explicit "just decide" user statements are followed by another question | Alert if > 0% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Clarification loop exceeds budget | consecutive_clarification_turns exceeds cap without output | High | Force fallback-with-defaults path, log session for prompt review |
| User override ignored | Agent asks another question immediately after an explicit "just decide" statement | Medium | Flag for override-detection logic review |

## Related Patterns
- [Clarification Irrelevant](./clarification-irrelevant.md) - a wrong-question failure that can compound into a loop when each wrong question triggers another
- [Over-Clarification](./over-clarification.md) - shares the root cause of excessive question-asking, but over-clarification can occur as a single unneeded question rather than a non-terminating loop
- [User Frustration Escalation](./user-frustration-escalation.md) - infinite clarification loops are a common concrete trigger of escalating user frustration
