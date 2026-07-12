# Over-Apology Loop

## Issue: Agent apologizes repeatedly without solving.

**Frequency**: Rare

**Symptoms**
- Repeated apology phrases; no resolution step.
- [Add more specific symptoms]

**Root Cause**
Agent apologizes repeatedly without solving.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
