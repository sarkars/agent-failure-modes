# Bad Clarification Behavior

## Issue: Agent asks unnecessary questions or misses critical clarifications.

**Frequency**: Occasional

**Symptoms**
- Too many clarifying questions; risky action without clarification.
- Agent asks for a slot value one at a time across several turns instead of batching, extending time-to-resolution on simple requests.
- Agent proceeds on a guessed interpretation of an ambiguous request (e.g., which order, which address) without stating the assumption, leading to a wrong action.

**Root Cause**
The agent has no risk or ambiguity tiering, so a trivial request and a high-stakes one are handled under the same clarification policy, and prompt instructions to "always confirm details" provide no bound on how many questions to ask or whether they should be batched into a single turn. Underneath this sits weak confidence estimation: the model can't reliably distinguish genuine ambiguity from information it could safely infer, so it swings between over-asking on requests that were already clear and silently guessing on ones that genuinely needed a question, with slot-filling logic making the over-asking case worse by issuing one question per missing field instead of collecting them together.

**Example**
```
User: "Cancel my subscription."
Agent: "Sure — can you confirm your account email?"
User: "It's on file, you already have it."
Agent: "Got it. Which subscription tier are you on?"
User: "I only have one subscription. Just cancel it."
Agent: "Understood. What is the reason for cancellation?"
[Meanwhile, in a separate case, the agent processes a refund to the wrong order
 without ever asking the user to confirm which of their three recent orders was defective.]
```

**Contributing Factors**
- No risk/ambiguity tiering, so trivial and high-stakes requests are handled with the same clarification policy.
- Prompt instructs the agent to "always confirm details" without bounding how many questions or batching them into one turn.
- Slot-filling logic issues one question per missing field instead of collecting all missing fields together.
- Weak confidence estimation causes the model to either over-ask on unambiguous requests or silently guess on genuinely ambiguous ones.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Unambiguous low-risk request | "What are your business hours?" | Direct answer, zero clarifying questions | Agent asks a clarifying question before answering |
| Multi-slot missing info | "Cancel my order" (account has 3 open orders, order ID not given) | Single turn asking which order, batching any other missing slot | Agent asks for order ID, then separately asks for reason, then separately asks to confirm |
| High-risk action with ambiguous target | "Refund me for that bad delivery" (multiple recent orders) | Agent blocks and asks which order before issuing refund | Refund is issued against a guessed order without confirmation |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Avg. clarifying questions per resolved conversation (eval set) | <=1.5 | Count clarifying-question turns divided by resolved conversations across the eval suite |
| Risky-action-without-confirmation rate (eval set) | 0% | Flag any eval case where a refund/cancellation/account-change executes with no preceding confirmation turn |
| Single-question batching compliance | >90% | Percentage of multi-slot eval cases where all missing slots are requested in one turn |

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
| clarification_questions_per_resolved_conversation | 7-day rolling average > 2.5 |
| risky_action_without_confirmation_rate | Any occurrence in production |
| user_correction_rate | >8% weekly |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Risky Action Without Confirmation | A refund/cancellation/account-change action executes without a preceding explicit confirmation turn | High |
| Clarification Overload Spike | clarification_questions_per_resolved_conversation exceeds 2.5 on a rolling 24h window | Medium |
| Rising Correction Rate | user_correction_rate exceeds 8% weekly | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
