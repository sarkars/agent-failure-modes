# Model Switching Mid-Session

## Issue
A router changes which underlying model serves a conversation partway through, either because of a routing rule that re-evaluates per-turn (cost tiering by turn complexity, load-based reassignment, a canary rollout without session affinity) or a failover event, and the new model doesn't share the exact conversational habits, persona adherence, or implicit context-handling of the one that served earlier turns. The user experiences a jarring discontinuity — a change in tone, a re-asked question, a forgotten instruction — that looks like the agent "forgetting" something, when actually a different model picked up the conversation.

**Frequency**: Occasional

**Symptoms**
- A persona, tone, or formatting convention established in earlier turns disappears abruptly at a specific turn, correlated with a routing/model change rather than gradual drift
- The agent re-asks for information the user already provided earlier in the same session, because the new model's handling of the existing transcript context differs subtly from the model that generated it
- Users report the assistant "feels like a different assistant" partway through a conversation, with no corresponding change in system prompt
- A tool-calling pattern or response format that worked reliably in earlier turns starts failing after a mid-session model switch, because the new model supports the feature slightly differently
- Failover events (one model instance going down, traffic shifting to a backup) produce this same discontinuity as an unintended side effect of an availability fix

## Root Cause
Routers that re-evaluate model selection on a per-turn or per-request basis (rather than pinning a model for the duration of a session) treat each turn as an independent routing decision, optimizing for that turn's estimated cost, complexity, or current load without any concept of conversational continuity as a constraint. Different model versions, even from the same family, differ in subtle ways — how they weight earlier context, what conventions they default to for ambiguous formatting, how reliably they honor an instruction given several turns back — so a mid-conversation switch effectively hands the transcript to a reader with a different set of habits than the one who was "in" the conversation so far. Failover and load-based rerouting make this worse because they're triggered by infrastructure conditions unrelated to the conversation's content, so the switch happens at an arbitrary point with no consideration of whether that turn is a safe place for a different model to take over.

## Example
```
A user has a 20-turn conversation with a trip-planning agent, having
established in turn 3: "I'm vegetarian, please only suggest restaurants
that work for that," and the agent has correctly filtered every
restaurant suggestion for turns 4-14 accordingly.

At turn 15, the router - reassessing per-turn based on query complexity -
routes a "simple" follow-up question to a smaller, cheaper model in the
same family, without session affinity.

The smaller model, now generating turn 15's response, has the full
transcript as context but weights the turn-3 constraint less reliably
than the model that had been "carrying" the conversation, and suggests a
steakhouse. The user has to repeat "I told you I'm vegetarian" - not
because the system forgot in a memory sense, but because a different
model, with different context-handling characteristics, took over mid-
conversation without any signal to the user that a switch occurred.
```

## Statistics
| Finding | Context |
|---------|---------|
| Session-affinity-free, per-turn routing shows a measurably higher rate of continuity complaints (repeated questions, dropped constraints) than session-pinned routing in comparable deployments | Typical range reported by teams comparing the two routing strategies |
| Mid-session model switches account for a meaningful minority of "agent forgot something" support complaints in multi-model routed systems, once investigated | Estimated from postmortems correlating complaints with routing logs |
| Pinning model selection for the duration of a session (re-evaluating only at session boundaries) eliminates the large majority of switch-induced continuity complaints | Typical range reported by teams that added session pinning |

## Mitigations
1. **Session-pinned routing**: Select a model once at session start and hold that selection for the duration of the conversation (or until an explicit session boundary), rather than re-evaluating routing on every turn.
2. **Continuity-aware failover**: When infrastructure failover is unavoidable mid-session, carry forward a compact summary of established constraints/persona explicitly into the new model's context rather than relying on it to infer continuity from raw transcript alone.
3. **Switch transparency logging**: Record every mid-session model switch (cause, turn number, models involved) so continuity complaints can be quickly attributed to a switch rather than investigated as a generic quality issue.
4. **Canary/A/B scoping at session boundaries**: Assign experiment cohorts at session start and hold them for the session, rather than reassigning per-request, so a single conversation is never split across experiment arms.
5. **Constraint re-anchoring after any switch**: When a switch is unavoidable, have the system explicitly re-inject key established facts/constraints into the new model's context at the switch point, rather than trusting silent transcript continuity.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| mid_session_model_switch_rate | Rate of sessions experiencing at least one model switch between turns | Alert if > 1% outside of intentional failover events |
| post_switch_continuity_failure_rate | Rate of repeated-question or dropped-constraint incidents in the turns immediately following a detected switch | Alert if significantly higher than baseline |
| session_affinity_violation_count | Count of sessions where cohort/routing assignment changed mid-session unintentionally | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unintended mid-session switch | A session's routing assignment changes without an explicit session-boundary trigger | High | Investigate routing config, consider reverting to session-pinned routing |
| Continuity failure following switch | post_switch_continuity_failure_rate spikes after a detected switch | Medium | Re-anchor constraints for affected session, review switch cause |

## Related Patterns
- [Model Selection Nondeterminism](./model-selection-nondeterminism.md) - unscoped cohort/routing reassignment is the general mechanism that produces mid-session switching as a specific symptom
- [Model Load Balancing Failure](./model-load-balancing-failure.md) - load-triggered failover is one legitimate cause of mid-session switching when session affinity isn't preserved through the failover path
- [Model Version Incompatibility](./model-version-incompatibility.md) - a switch to a different model version mid-session can also break feature assumptions the calling code made about the original version
