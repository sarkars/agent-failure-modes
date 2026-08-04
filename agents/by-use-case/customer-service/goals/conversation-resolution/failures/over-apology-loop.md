# Over-Apology Loop

## Issue: Agent apologizes repeatedly without solving.

**Frequency**: Rare

**Symptoms**
- Repeated apology phrases; no resolution step.
- Conversation turn count grows for several exchanges with no new tool call, retrieved information, or concrete next step introduced.
- User explicitly calls out the loop ("stop apologizing and just fix it") without the agent's behavior changing on the next turn.

**Root Cause**
Agent apologizes repeatedly without solving.

**Example**
```
User: "My package still hasn't arrived and it's been 2 weeks."
Agent: "I'm so sorry for the inconvenience this has caused you."
User: "Okay, but what are you going to do about it?"
Agent: "I sincerely apologize for the delay and any frustration this has caused."
User: "You keep apologizing. Can you just reship it or refund me?"
Agent: "I understand your frustration, and I apologize again for this experience."
```

**Contributing Factors**
- Prompt emphasizes empathetic/apologetic language without pairing it with a mandatory resolution or escalation step.
- No no-progress-turn detector, so the model can emit an apology-only response repeatedly without a validation check blocking it.
- Underlying resolution path (tool call, policy lookup) is genuinely stuck or erroring, and the model falls back to apology as filler instead of surfacing the failure and escalating.
- No cap on consecutive apology turns, so nothing forces a transition to action or human handoff.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Repeated complaint, no tool available | User repeats a delivery complaint 3 times in a row | Agent apologizes once, then takes a concrete action (reship/refund/escalate) | Agent apologizes again on turn 2 or 3 without a new action or escalation |
| User calls out the loop | User says "stop apologizing and just fix it" | Agent immediately drops apology language and states/attempts a concrete resolution | Agent responds with another apology phrase |
| Genuinely stuck resolution path | Underlying tool for the fix is erroring | Agent surfaces the failure plainly and escalates rather than apologizing repeatedly | Agent apologizes across multiple turns instead of escalating |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Consecutive apology-turn rate (eval set) | <1% | Percentage of eval conversations with 2+ consecutive no-progress apology turns |
| No-progress turn rate (eval set) | <5% | Percentage of eval agent turns with no new tool call, information, or next step |
| Loop-breaker trigger rate (eval set) | <1% | Percentage of eval conversations that require the escalation backstop to fire |

---

## Mitigation Strategies

### Prevention
1. **Resolution-first response ordering**: enforce a response template requiring a concrete next action or resolution attempt before, or in place of, any apology language, since the failure pattern is apology substituting for problem-solving rather than accompanying it. Trade-off: can feel abrupt or less empathetic in genuinely distressing situations where acknowledgment matters before action.
2. **Apology budget per conversation**: cap apology phrases to at most one per conversation (or one per newly introduced problem), forcing subsequent turns to contain only resolution content, since repeated apologizing is a low-effort filler the model defaults to when it lacks a concrete next step. Trade-off: a hard cap risks the agent sounding cold if a genuinely new issue arises later that needs acknowledgment.
3. **No-progress-turn detector in generation**: before finalizing a response, check whether it contains a new tool call, new information, or a concrete next step; if not, block sending an apology-only response and force a fallback (retry solve path or escalate). Trade-off: adds a validation step to every turn and can produce escalations that could have been avoided with one more apology-cushioned turn.

### Detection & Response
1. **Consecutive-apology-turn scanning**: scan transcripts for 2+ consecutive agent turns containing apology language without an intervening tool call or new resolution content, the direct signature of this failure. Response: flag for review and auto-escalate the live conversation to a human if detected in real time.
2. **No-progress conversation length correlation**: track conversations where turn count grows but no new tool calls/information are introduced, correlated with apology-phrase density. Response: surface these as candidates for resolution-first template enforcement.
3. **CSAT free-text mining for "not helpful"/"just apologizing" language**: mine post-conversation CSAT comments for language indicating the user noticed empty apologizing. Response: pull the matching transcript into the eval set as a labeled failure example.

### Architecture Patterns
1. **Resolution state machine with apology as a bounded sub-state**: model the conversation as a state machine where "apologize" is a transient sub-state that must transition to "attempt resolution" or "escalate" within one turn, structurally preventing indefinite apology loops.
2. **Real-time loop-breaker escalation gate**: a runtime guard that detects N consecutive no-progress turns and forces escalation to a human regardless of what the model would otherwise generate, acting as a backstop independent of prompt compliance.
3. **Template-constrained response composer**: separate "empathy" and "action" as distinct, independently required slots in a structured response composer, so a response literally cannot be emitted with an empathy slot filled and an action slot empty.

### Metrics
1. **consecutive_apology_turns_rate**: Target: <1% of conversations have 2+ consecutive no-progress apology turns; Alert on >3%
2. **no_progress_turn_rate**: Target: <5% of all agent turns; Alert on >10%
3. **apology_without_resolution_csat_mentions**: Target: <2% of negative CSAT comments; Alert on >5%
4. **loop_breaker_trigger_rate**: Target: <1% of conversations trigger the escalation backstop; Alert on >3% (indicates upstream prevention is failing)

### Alerts
1. **Apology Loop Detected Live** (P2): Condition - real-time detector finds 2+ consecutive no-progress apology turns in an active conversation. Action: auto-escalate to a human agent, attach a loop-detection flag to the handoff.
2. **No-Progress Turn Rate Spike** (P2): Condition - no_progress_turn_rate exceeds 10% over 24h. Action: check for a recent prompt regression removing resolution-first instructions.
3. **Loop-Breaker Overuse** (P3): Condition - loop_breaker_trigger_rate exceeds 3% weekly. Action: review the prevention layer (resolution-first template) for gaps, since the backstop is firing too often.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| consecutive_apology_turns_rate | >3% |
| no_progress_turn_rate | >10% |
| loop_breaker_trigger_rate | >3% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Apology Loop Detected Live | Real-time detector finds 2+ consecutive no-progress apology turns in an active conversation | Medium |
| No-Progress Turn Rate Spike | no_progress_turn_rate exceeds 10% over 24h | Medium |
| Loop-Breaker Overuse | loop_breaker_trigger_rate exceeds 3% weekly | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
