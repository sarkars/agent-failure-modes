# Model Instruction Following Decay

## Issue
A system prompt's rules — tone constraints, formatting requirements, forbidden topics, role boundaries — are followed reliably in the first few turns of a conversation but are followed progressively less reliably as the conversation grows longer, even though the system prompt itself never changes and is technically still present in every call. The agent has no mechanism to notice that adherence has dropped, since each individual response still looks like a normal, fluent reply.

**Frequency**: Very Common

**Symptoms**
- A rule stated in the system prompt ("never discuss pricing, redirect to sales") is honored in turns 1-10 and silently violated by turn 30 of the same session
- Output formatting specified once at session start (e.g. always respond in bullet points) gradually reverts to prose over many turns
- The model becomes more willing to answer questions it was instructed to decline as the conversation accumulates more back-and-forth, even with no new jailbreak attempt
- Re-injecting the original system prompt text mid-conversation temporarily restores compliance, then it decays again
- Decay rate is faster in conversations with more user turns of a different topic/style than the system prompt's own register

## Root Cause
Autoregressive generation conditions each new response primarily on the most recent tokens in context, and as a conversation accumulates many turns of user-assistant exchange, the relative "weight" of the original system prompt — fixed in position, not repeated — shrinks in proportion to the growing volume of subsequent conversational content the model is also attending to. The model was never trained with a mechanism that guarantees system-level instructions retain constant influence regardless of conversation length; it only learned patterns from training data where instructions and their following behavior were usually close together. Every additional turn is also an implicit example the model conditions on, and if user turns consistently push in a direction adjacent to (but not identical to) a prohibited behavior, the model's estimate of "what response is expected here" can drift toward matching the recent conversational pattern rather than the original, now distant, rule.

## Example
```
A customer service agent is deployed with a system prompt rule: "Never
quote specific refund amounts; always say 'a member of our billing team
will confirm the exact amount.'"

Turns 1-8: the model correctly deflects every refund-amount question per
the rule.

Turns 9-24: the customer, frustrated, repeatedly asks for "just a rough
number" in different phrasings across many turns, each framed as
reasonable and low-stakes.

Turn 25: the model responds, "Based on your $340 order, you'd likely see
around $280 back after the restocking fee" - a direct violation of the
original rule, introduced with no new instruction and no jailbreak attempt,
purely through cumulative conversational pressure diluting the original
system prompt's effective influence.
```

## Statistics
| Finding | Context |
|---------|---------|
| System-prompt rule adherence in long conversations (30+ turns) is typically 20-35 percentage points lower than in the first 5 turns of the same conversation type | Estimated from internal long-session compliance evaluations |
| Re-injecting the system prompt verbatim every N turns restores adherence to near session-start levels, but effect decays again within roughly 10-15 turns | Typical range observed in agent frameworks using periodic re-injection |
| Decay is measurably faster when user turns are thematically adjacent to (rather than unrelated to) the restricted behavior | Estimated from comparisons of on-topic-pressure vs. off-topic-length conversations |

## Mitigations
1. **Periodic system prompt re-injection**: Re-send the full system prompt (or its critical rules) at a fixed turn interval or token-count interval rather than relying on it persisting from the start of the conversation.
2. **Rule-checking post-processor**: Run a lightweight, separate check against the highest-priority rules before returning any response in long sessions, independent of the generating call's own compliance.
3. **Session length limits with reset**: Cap conversation length before triggering a summarize-and-restart that re-establishes the system prompt fresh, rather than letting sessions grow unbounded.
4. **Rule salience weighting**: Where the platform supports it, mark critical rules with mechanisms proven to increase persistence (e.g. structured tool-enforced constraints) instead of relying solely on natural-language system prompt text.
5. **Adherence monitoring by turn depth**: Track compliance rate as a function of turn count in production to detect decay curves and calibrate re-injection frequency to before the curve drops below an acceptable floor.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| rule_adherence_by_turn_depth | Compliance rate with critical system rules, bucketed by conversation turn count | Alert if adherence drops > 20 points from turn-1-5 baseline |
| turns_since_last_reinjection | Number of turns elapsed since the system prompt was last re-sent in full | Alert if exceeds configured re-injection interval |
| late_session_violation_rate | Rate of rule violations occurring after turn 20 vs. before | Alert if late-session rate exceeds 2x early-session rate |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Critical rule violated in long session | A high-priority rule (e.g. pricing disclosure, safety boundary) is violated after turn 15+ | High | Terminate/reset session, re-inject system prompt, log for adherence-curve recalibration |
| Adherence curve degradation | rule_adherence_by_turn_depth trend worsens release-over-release | Medium | Review re-injection strategy, consider session length cap changes |

## Related Patterns
- [Model Context Length Behavior Change](./model-context-length-behavior-change.md) - context growth is the underlying mechanism that drives instruction decay as sessions lengthen
- [Model Style Drift](./model-style-drift.md) - persona/tone drift is the stylistic counterpart to rule-adherence decay, both accumulating gradually over a session
- [Model Refusal Inconsistency](./model-refusal-inconsistency.md) - decayed instruction-following is one path by which refusal behavior becomes inconsistent within the same conversation
