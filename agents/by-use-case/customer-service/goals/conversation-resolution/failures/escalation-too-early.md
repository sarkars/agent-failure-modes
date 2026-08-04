# Escalation Too Early

## Issue: Agent gives up despite solvable request.

**Frequency**: Occasional

**Symptoms**
- High handoff rate on routine tasks.
- Agent escalates after a single failed tool call or retrieval miss without retrying with a reformulated query or alternate approach.
- Escalation message gives a vague, generic reason ("I'm unable to help with this") rather than citing a specific missing capability or data gap.

**Root Cause**
Agent gives up despite solvable request.

**Example**
```
User: "Can you look up the tracking status for order #48213?"
Agent: [calls order-lookup tool; tool times out once]
Agent: "I'm not able to help with that. Let me transfer you to a human agent."
[No retry was attempted, and a simple re-query or alternate lookup tool would have succeeded.]
```

**Contributing Factors**
- No requirement to retry with a reformulated query or alternate tool before escalating, so a single transient failure (timeout, empty result) is treated as "unsolvable."
- Escalation confidence threshold set conservatively, so the model defaults to handing off rather than attempting a harder solve path.
- No structured justification requirement, so vague "can't help" escalations aren't distinguishable from genuine capability gaps until a human reviews the transcript.
- Capability registry (what tools/data the agent actually has access to) is incomplete or not consulted, so the model underestimates what it can solve.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Transient tool failure, routine task | Order lookup tool times out once, then succeeds on retry | Agent retries the lookup and resolves the request without escalating | Agent escalates immediately after the first timeout |
| Solvable via reformulation | Retrieval returns no result for exact wording; a paraphrase would match | Agent reformulates the query and finds the answer | Agent escalates citing "no information found" without reformulating |
| Escalation justification check | A genuinely unsolvable request (requires data the agent has no access to) | Agent escalates with a specific stated capability/data gap | Escalation message is generic ("I can't help with that") with no specific reason |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Single-attempt escalation rate on eval set | <10% | Percentage of eval escalations that occur after only one solve attempt |
| Routine-task solve rate before escalation | >90% | Percentage of eval tasks tagged "routine" resolved without escalation |
| Escalation justification specificity | >80% | Percentage of eval escalations citing a specific capability/data gap vs. a generic refusal |

---

## Mitigation Strategies

### Prevention
1. **Capability-confidence threshold calibration**: require the agent to attempt a structured solve path (tool calls, retrieval, retries) before escalating, and calibrate the "I can't solve this" confidence threshold against actual solve-rate data, since premature escalation stems from the threshold being set too conservatively relative to the agent's real capability. Trade-off: a lower threshold risks the opposite failure — the agent struggling too long before finally escalating.
2. **Retry-with-variation before escalate**: require at least one reformulation or alternate tool/approach attempt before the agent is allowed to hand off, since many early escalations occur after a single failed attempt rather than exhausting available solve paths. Trade-off: adds latency and token cost to every difficult conversation, including ones that were genuinely unsolvable.
3. **Escalation justification requirement**: force the agent to produce a structured reason citing which specific capability or data it lacks before it's allowed to escalate, since unstructured "I can't help with that" escalations are hard to distinguish from genuine capability gaps versus premature give-up. Trade-off: adds a generation step and can be gamed by the model producing plausible-sounding but inaccurate justifications.

### Detection & Response
1. **Routine-task handoff-rate monitoring**: track handoff rate specifically on tasks tagged as routine/previously-automatable, the most direct signature of escalating despite solvability. Response: sample handed-off routine-task transcripts to check whether a solve path existed.
2. **Post-handoff resolution-difficulty audit**: have human agents tag escalated tickets by actual difficulty after resolving them; tickets resolved in under N actions are candidates for premature escalation. Response: feed these back into the retry/threshold tuning loop.
3. **Escalation-reason clustering**: cluster the agent's stated escalation justifications; a large cluster of vague, low-specificity justifications indicates threshold miscalibration rather than genuine capability gaps. Response: retrain/re-prompt on the clustered failure category.

### Architecture Patterns
1. **Escalation state machine with attempt gates**: model escalation as a state machine requiring N distinct solve attempts (tool call, retrieval, reformulation) before transitioning to the "escalate" state, structurally preventing single-attempt give-ups.
2. **Capability registry with solve-path lookup**: maintain an explicit registry of what the agent can do (tools, data access, policy exceptions) so the escalation decision is a lookup against known capability rather than an implicit model judgment call.
3. **Confidence-threshold routing tied to outcome feedback**: route the escalate/continue decision through a threshold that is automatically retuned from labeled outcome data (was the routine task actually solvable) rather than a fixed static prompt instruction.

### Metrics
1. **routine_task_handoff_rate**: Target: <5%; Alert on >10% over 7-day window
2. **single_attempt_escalation_rate**: Target: <10% of escalations occur after only one solve attempt; Alert on >25%
3. **post_handoff_low_effort_resolution_rate**: Target: <15% of handoffs resolved by human in <2 actions; Alert on >25%
4. **escalation_justification_specificity_score**: Target: >80% of escalations cite a specific capability/data gap; Alert on <60%

### Alerts
1. **Routine Handoff Spike** (P2): Condition - routine_task_handoff_rate exceeds 10% over 24h. Action: sample transcripts, check for a recent threshold/prompt regression, roll back if confirmed.
2. **Single-Attempt Escalation Surge** (P2): Condition - single_attempt_escalation_rate exceeds 25% weekly. Action: raise the retry-before-escalate requirement, re-run the capability eval suite.
3. **Low-Effort Resolution Trend** (P3): Condition - post_handoff_low_effort_resolution_rate exceeds 25% for 2 consecutive weeks. Action: schedule a threshold recalibration review with support ops.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| routine_task_handoff_rate | >10% over 7-day window |
| single_attempt_escalation_rate | >25% |
| post_handoff_low_effort_resolution_rate | >25% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Routine Handoff Spike | routine_task_handoff_rate exceeds 10% over 24h | Medium |
| Single-Attempt Escalation Surge | single_attempt_escalation_rate exceeds 25% weekly | Medium |
| Low-Effort Resolution Trend | post_handoff_low_effort_resolution_rate exceeds 25% for 2 consecutive weeks | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
