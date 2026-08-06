# Premature Ticket Closure from Politeness-Cue Misread as Resolution Confirmation

## Issue: Agent Closes a Support Ticket as Resolved Because the Customer's Reply Contains a Polite Closing Phrase ("Thanks," "OK," "Got it"), Without Verifying the Underlying Problem Was Actually Fixed

**Frequency**: Very Common

**Symptoms**
- Tickets are auto-closed immediately after a customer message containing "thanks," "ok," "got it," "will try that," or similar social-closing language, even when the preceding agent turn did not confirm the fix worked
- Customers who used a polite acknowledgment as a conversational reflex (common across many cultures and support contexts) reopen the same issue within days, often with added frustration at having to re-explain
- Reopen rate for auto-closed tickets is elevated specifically in the subset closed on a politeness-phrase trigger, compared to tickets closed on an explicit confirmation phrase ("that fixed it," "working now")
- Csat scores for reopened tickets are measurably lower than for tickets that were never prematurely closed, since the customer experienced both the original problem and the closure/reopen friction
- Agents trained or prompted to detect "conversation is ending" signals treat politeness markers and genuine resolution confirmation as the same signal class

**Root Cause**
The agent's turn-ending or resolution-detection logic is built on a general-purpose read of conversational closing signals rather than a specific check for affirmative resolution language tied to the actual reported problem. Politeness phrases are extremely frequent as a conversational reflex regardless of whether the underlying issue is fixed, so a classifier or prompt that treats "customer seems done talking" as equivalent to "customer confirms the fix worked" will systematically over-trigger closure. The failure is agent-specific because it substitutes a fluent read of social register for the narrower, harder task of verifying that the specific symptom described earlier in the thread was actually addressed.

**Example**
```
Turn 1 (Customer): My export to CSV keeps failing with a timeout error.
Turn 2 (Agent): Try re-running the export with a smaller date range — that
  usually avoids the timeout.
Turn 3 (Customer): Ok thanks, I'll give that a try.
Agent action: Marks ticket "Resolved" immediately after Turn 3, because the
  reply contains "thanks" and no further question.
Actual outcome: The customer tries the suggestion two days later, it still
  times out, and has to open a new ticket and re-explain the original
  export failure from scratch, now marked as a repeat/unresolved case.
```

**Key Statistics**
| Finding | Context |
|---|---|
| Failure-detection frameworks for task-oriented dialogue distinguish "task-success impairment" from surface-level conversational closure signals, finding that closure language alone is an unreliable proxy for whether the underlying task actually succeeded | TRACER: Early Failure Detection for Task-Oriented Dialogue (arXiv:2607.03974) |
| Non-cooperative user-simulation testing of dialogue systems finds that systems frequently misclassify a user's socially-motivated turn as a task-completion signal, inflating apparent success rates relative to independently verified outcomes | ChatChecker: A Framework for Dialogue System Testing and Evaluation Through Non-cooperative User Simulation (arXiv:2507.16792) |
| In production support-ticket audits, tickets auto-closed on a generic closing-phrase trigger typically show a meaningfully higher reopen rate within the following week than tickets closed on an explicit fix-confirmation phrase | Illustrative range from support-operations audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Politeness without confirmation | Customer replies "thanks, I'll try that" after a suggested fix, no follow-up | Ticket stays open pending a confirmation check-in, not auto-closed | Ticket closed immediately on the politeness phrase |
| Explicit confirmation | Customer replies "that fixed it, thank you" | Ticket closes as resolved | Ticket left open despite clear confirmation |
| Polite deflection of an unhelpful answer | Customer replies "ok" after an answer that did not address their stated symptom | Agent does not close; flags for a resolution check | Ticket closed, symptom never actually addressed |
| Silence after suggestion | Customer does not reply at all within the timeout window | Ticket is closed on a distinct "no-reply timeout" path, tracked separately from confirmed resolutions | Silence-closure and confirmed-closure are logged identically, masking the difference in the metric |

### Evaluation Dataset
- **Source**: Historical support threads where the ticket was later reopened, paired with the exact customer message and agent action that triggered the original closure
- **Size**: 300+ closure decisions spanning politeness-only, explicit-confirmation, and silence-timeout closures
- **Key variations**: politeness phrase with unaddressed symptom; politeness phrase with addressed symptom; explicit confirmation; ambiguous short replies ("ok", "sure", "noted")

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Confirmation-grounded closure rate | 100% of auto-closures preceded by an explicit fix-confirmation match, not a generic politeness match | % of auto-closed tickets where the triggering message matches a confirmation-specific pattern versus a generic closing-phrase pattern |
| Reopen rate on politeness-triggered closures | Within 1 percentage point of the reopen rate on confirmation-triggered closures | % of tickets reopened within 7 days, segmented by closure-trigger type |
| False-closure rate | < 2% | % of sampled auto-closed tickets where a human reviewer judges the original symptom was not actually resolved |

### Automated Checks
```python
def check_closure_trigger(message: str) -> dict:
    """Distinguish a generic politeness close from an explicit resolution confirmation."""
    politeness_only = ["thanks", "thank you", "ok", "okay", "got it", "noted", "will try"]
    confirmation_phrases = ["that fixed it", "working now", "resolved", "that worked",
                             "issue is gone", "confirmed fixed"]
    text = message.lower()
    has_confirmation = any(p in text for p in confirmation_phrases)
    has_politeness_only = (any(p in text for p in politeness_only) and not has_confirmation)
    return {
        "has_confirmation": has_confirmation,
        "politeness_only_risk": has_politeness_only,
        "safe_to_auto_close": has_confirmation,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Confirmation-Specific Trigger List**: Restrict auto-closure to a narrow set of phrases that explicitly reference resolution ("fixed," "working now," "resolved"), excluding generic politeness or acknowledgment language from the trigger set
2. **Symptom-Match Requirement**: Before closing, require the agent to state which specific symptom from earlier in the thread was resolved, making a closure without symptom-grounding structurally distinguishable from one with it
3. **Delayed Confirmation Check-In**: For ambiguous replies (politeness phrase with no explicit confirmation), send one follow-up check-in after a delay rather than closing immediately, and only close on an affirmative or on a second timeout

### Detection & Response
1. **Reopen-Rate Segmentation**: Track reopen rate separately for politeness-triggered vs. explicitly-confirmed closures; a persistent gap indicates the closure trigger is over-broad
2. **Sampled Human Review of Auto-Closures**: Periodically sample auto-closed tickets and have a human reviewer judge whether the original symptom was actually addressed, independent of the closure trigger

### Architecture Patterns
- **Two-Stage Closure Pipeline**: Separate "customer appears done talking" detection from "issue confirmed resolved" detection as two distinct classifiers, requiring both before an auto-close action fires
- **Symptom-Tracking State**: Maintain the originally reported symptom as an explicit state field through the conversation, and require closure logic to reference it rather than operating on the latest message in isolation

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `ticket_closure.politeness_trigger.count` | Auto-closures triggered by a generic politeness phrase rather than explicit confirmation | > 5% of all auto-closures per week |
| `ticket_closure.reopen_rate.politeness_vs_confirmed` | Gap in 7-day reopen rate between politeness-triggered and confirmation-triggered closures | > 3 percentage point gap |
| `ticket_closure.false_closure.rate` | % of sampled auto-closures judged unresolved by human review | > 2% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Elevated Politeness-Trigger Closures | Weekly politeness-triggered closure share exceeds threshold | P2 | Review and tighten the confirmation-phrase trigger list |
| Reopen-Rate Gap Widening | Politeness-vs-confirmed reopen gap exceeds threshold for 2 consecutive weeks | P2 | Audit closure logic; consider disabling auto-close on ambiguous replies pending fix |

---

## References
- [TRACER: Early Failure Detection for Task-Oriented Dialogue](https://arxiv.org/pdf/2607.03974)
- [ChatChecker: A Framework for Dialogue System Testing and Evaluation Through Non-cooperative User Simulation](https://arxiv.org/pdf/2507.16792)
