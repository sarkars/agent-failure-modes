# Bad Clarification Behavior

## Issue: Agent asks unnecessary questions or misses critical clarifications.

**Frequency**: Occasional

**Symptoms**
- Too many clarifying questions; risky action without clarification.
- [Add more specific symptoms]

**Root Cause**
Agent asks unnecessary questions or misses critical clarifications.

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
1. **Risk-tiered clarification policy**: classify each request by ambiguity level and action risk/reversibility, and only require clarification when both are above threshold, since the failure stems from clarification behavior not being calibrated to how ambiguous or risky the request actually is. Trade-off: requires maintaining and tuning a risk taxonomy per action type, which adds engineering overhead and can go stale as new actions are added.
2. **Confidence-gated slot-filling**: only ask for a slot if the model's confidence in inferring it from context/history falls below a threshold, otherwise proceed with the inferred value and state the assumption explicitly. Trade-off: an overconfident model will silently proceed on wrong assumptions, trading fewer questions for more silent errors.
3. **Single-question batching**: when clarification is genuinely warranted, collapse all needed clarifications into one turn instead of serial single-item questions, since the symptom of "too many clarifying questions" is often several separate single-slot questions rather than genuinely excessive need for clarification. Trade-off: batched questions are harder for users to answer completely, increasing partial-answer follow-up turns.

### Detection & Response
1. **Clarification-to-resolution ratio tracking**: monitor clarifying questions per resolved conversation; conversations with 3+ clarifying turns are the population most likely to include unnecessary questions. Response: sample and hand-label whether the added questions were justified by actual ambiguity.
2. **Zero-clarification risky-action audit**: flag any conversation where a high-risk action (refund, cancellation, account change) executed with zero clarifying turns. Response: audit whether required information was actually confirmed before the action ran.
3. **User-initiated correction detection**: detect user turns that contradict an earlier agent assumption ("no, I said..."), the direct behavioral signature of a missed clarification. Response: route to a review queue as a candidate missed-clarification case.

### Architecture Patterns
1. **Ambiguity/risk matrix router**: a pre-response classifier scores (ambiguity, risk) and routes to one of three paths — proceed silently, proceed with stated assumption, or block-and-ask — making clarification behavior a structural decision rather than an emergent model choice.
2. **Clarification budget per conversation**: cap the number of clarifying turns allowed before the agent must proceed with best-effort assumptions or escalate, preventing the "too many questions" failure from compounding turn over turn.
3. **Mandatory-confirmation gate for irreversible actions**: architecturally require an explicit confirmation step before actions like refunds or cancellations execute, regardless of what the general clarification policy would otherwise decide.

### Metrics
1. **clarification_questions_per_resolved_conversation**: Target: <=1.5 average; Alert on 7-day rolling average > 2.5
2. **risky_action_without_confirmation_rate**: Target: 0%; Alert on any occurrence in production
3. **user_correction_rate**: Target: <5% of conversations; Alert on >8% weekly
4. **over_clarification_abandonment_rate**: Target: <3%; Alert on >5% (users abandoning after 2+ clarifying questions)

### Alerts
1. **Risky Action Without Confirmation** (P1): Condition - a refund/cancellation/account-change action executes without a preceding explicit confirmation turn in the transcript. Action: page on-call, pull transcript for compliance review, disable auto-execution for that action type pending review.
2. **Clarification Overload Spike** (P2): Condition - clarification-questions-per-conversation exceeds 2.5 on a rolling 24h window. Action: review recent prompt/policy changes and sample flagged transcripts for unnecessary questions.
3. **Rising Correction Rate** (P3): Condition - user_correction_rate exceeds 8% weekly. Action: add flagged transcripts to the eval set as missed-clarification regression cases.

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
