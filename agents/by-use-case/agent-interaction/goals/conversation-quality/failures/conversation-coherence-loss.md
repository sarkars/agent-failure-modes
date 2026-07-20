# Conversation Coherence Loss

## Issue
Over an extended multi-turn conversation, the agent's responses stop tracking the accumulated state of the discussion — it loses track of decisions already made, entities already introduced, or the current sub-task within a larger goal, and later replies read as disconnected from what came before. Unlike relevance drift, where the topic itself gradually shifts, coherence loss can occur on the same topic: the agent simply can't hold the thread together, producing responses that are locally sensible but don't fit the conversation's actual state.

**Frequency**: Common

**Symptoms**
- Agent re-introduces or re-explains something already established earlier in the conversation as if it were new
- References to "it," "that," or "the one we discussed" resolve to the wrong entity
- Agent's response addresses a sub-question from several turns ago instead of the current one
- Internal state (e.g. a running list, a selected option, a constraint set earlier) is silently dropped or reset
- Users report needing to re-state context that was already given

## Root Cause
Long conversations push earlier turns toward or past the effective context window, and even within the window, models weight recent tokens more heavily than distant ones, so information established many turns back competes poorly against the current turn's content. Coherence loss is compounded when the agent has no explicit running summary or state object it updates each turn — it re-derives "what's going on" from raw transcript on every turn instead of maintaining a persistent representation, so subtle facts (a constraint mentioned once in turn 3, still binding in turn 40) are the first to be dropped.

## Example
```
Turn 3:  User: "I'm only considering vendors that support SSO, since our
         security team requires it."
Turn 4:  Agent: "Noted, I'll filter for SSO support."
...
Turn 28: User: "What about Vendor D, does it fit?"
Turn 29: Agent: "Vendor D looks like a strong option — good pricing,
         solid support tier." (Vendor D does not support SSO, a fact
         available in its spec sheet already discussed in turn 12, and
         the SSO requirement from turn 3 is never re-applied.)
Turn 30: User: "I told you 25 turns ago SSO was a hard requirement. Did
         you forget?"
Turn 31: Agent: "You're right, let me reconsider." (proceeds to
         re-derive the same incomplete comparison, again without
         consistently applying the SSO filter)
```

## Statistics
| Finding | Context |
|---------|---------|
| Response consistency with early-conversation constraints drops measurably once a session exceeds roughly 20-30 turns | Typical range observed across long-running agent sessions |
| An estimated 15-25% of long-session corrections are the user re-stating information already given earlier in the same conversation | Estimated from production conversation logs |
| Maintaining an explicit updated-each-turn state/constraint summary cuts coherence-related corrections substantially in long sessions | Reported range across teams that added running-state tracking |

## Mitigations
1. **Persistent constraint/state tracking**: Maintain an explicit, structured summary of established facts, constraints, and decisions that is updated (not regenerated) each turn and injected into context regardless of transcript length.
2. **Periodic self-recap**: Have the agent periodically restate its understanding of the current goal and active constraints, giving the user a checkpoint to catch drift before it compounds.
3. **Entity and reference resolution checks**: Explicitly resolve pronouns and vague references ("it," "that one") against the tracked state before generating a response, rather than relying on implicit attention.
4. **Context compression over truncation**: When approaching context limits, summarize older turns into a compact durable form instead of silently dropping them, preserving binding constraints even as verbatim history ages out.
5. **Constraint re-application audit**: Before finalizing an answer that touches an entity or decision established earlier, re-check it against all previously stated constraints rather than only the most recent turns.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| early_constraint_violation_rate | Rate at which responses in long sessions violate a constraint established in an earlier turn | Alert if > 10% |
| user_restatement_rate | Share of turns where the user re-provides information already given earlier in the session | Alert if > 15% |
| session_length_vs_correction_rate | Correlation between turn count and correction frequency | Alert if correction rate rises with length |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Constraint violated late in long session | An established hard constraint is violated after turn 20+ | High | Trigger state-recap, review context management for the session |
| Repeated user restatement | User restates the same fact 2+ times in one session | Medium | Flag session for coherence review |

## Related Patterns
- [Conversation Relevance Drift](./conversation-relevance-drift.md) - drift changes what's being discussed; coherence loss loses track of the same discussion's own state
- [Conversation Contradiction](./conversation-contradiction.md) - a frequent symptom of coherence loss, since forgotten state often leads directly to contradicting earlier statements
- [Conversation Repetition](./conversation-repetition.md) - re-explaining already-established information is a common surface symptom of underlying coherence loss
