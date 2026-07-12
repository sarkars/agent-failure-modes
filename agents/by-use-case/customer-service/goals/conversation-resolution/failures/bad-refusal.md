# Bad Refusal

## Issue: Agent refuses safe requests or gives unsafe help.

**Frequency**: Common

**Symptoms**
- False positive/negative safety classifications.
- [Add more specific symptoms]

**Root Cause**
Agent refuses safe requests or gives unsafe help.

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
1. **Calibrated refusal policy with graded responses**: replace binary allow/refuse with graded responses (full help, help-with-caveat, partial help, refuse) tied to specific policy categories, since the root failure is a binary classifier producing both false positives (over-refusal) and false negatives (unsafe help) rather than a calibrated risk response. Trade-off: graded policies are harder to specify precisely and increase prompt/policy complexity.
2. **Refusal eval suite covering adjacent safe/unsafe pairs**: build eval sets of near-miss pairs (a safe request that resembles an unsafe one, and vice versa) and regression-test every policy/prompt change against them. Trade-off: building and maintaining a high-quality near-miss eval set requires ongoing human red-teaming effort.
3. **Context-aware safety classification**: feed the safety classifier the full conversation context and stated business purpose, not just the isolated message, since many false-positive refusals come from single-message classification missing legitimate context. Trade-off: richer context increases the chance of a jailbreak using fabricated context to justify an unsafe request.

### Detection & Response
1. **Refusal-rate anomaly detection**: track refusal rate per intent category; a rate that jumps or sits far above historical baseline signals a false-positive spike. Response: sample refused transcripts from the anomalous category and re-classify by hand.
2. **Post-hoc unsafe-help audit sampling**: randomly sample "helped" conversations in risk-relevant categories (financial, medical, account security) for human safety review, since false negatives don't self-report the way user complaints do for over-refusal. Response: any confirmed unsafe-help case triggers immediate policy patch and eval-set addition.
3. **User pushback/appeal detection**: detect user language indicating a refusal was wrong ("I'm just asking about...", explicit complaints) and route to a refusal-appeals queue. Response: humans triage and correct the underlying policy or few-shot examples.

### Architecture Patterns
1. **Two-stage classify-then-respond pipeline**: separate the safety classification step from response generation so refusal decisions are auditable and independently testable, rather than an entangled judgment made inline during generation.
2. **Human-in-the-loop gate for borderline scores**: route requests near the classifier's decision boundary to a lightweight human or secondary-model review rather than forcing a binary auto-decision where most false positives/negatives cluster.
3. **Policy-as-config versioning**: keep refusal policy thresholds and category definitions in versioned config separate from the model prompt, so refusal behavior can be tuned and rolled back independently of broader prompt changes, with each change gated by the eval suite.

### Metrics
1. **false_positive_refusal_rate**: Target: <2% of safe requests; Alert on >4% weekly
2. **false_negative_unsafe_help_rate**: Target: <0.5% of risk-category conversations (from audit sampling); Alert on any confirmed case
3. **refusal_rate_by_category**: Target: within +/-20% of 90-day baseline per category; Alert on >50% deviation week over week
4. **refusal_appeal_rate**: Target: <3% of refusals appealed; Alert on >6%

### Alerts
1. **Unsafe Help Confirmed** (P1): Condition - human audit confirms an unsafe response was given. Action: immediate policy patch, add case to eval regression set, notify safety/compliance lead within 1 hour.
2. **Refusal Rate Spike** (P2): Condition - refusal rate in any intent category exceeds baseline by 50% over 24h. Action: pause the triggering prompt/policy change if recent, sample transcripts, roll back if false positives confirmed.
3. **Appeal Queue Backlog** (P3): Condition - refusal-appeals queue exceeds SLA (unresolved >48h). Action: reprioritize human review staffing.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
