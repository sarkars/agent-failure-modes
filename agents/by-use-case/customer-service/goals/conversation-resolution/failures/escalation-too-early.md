# Escalation Too Early

## Issue: Agent gives up despite solvable request.

**Frequency**: Occasional

**Symptoms**
- High handoff rate on routine tasks.
- [Add more specific symptoms]

**Root Cause**
Agent gives up despite solvable request.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
