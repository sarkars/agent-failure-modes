# Multi-Issue Message Sentiment Averaging Masks a Severe Complaint

## Issue: When a Single Customer Message Contains Several Distinct Issues of Varying Severity, the Sentiment-Escalation Agent Scores Overall Message Sentiment as a Blend, Diluting a Severe Complaint That Would Have Triggered Escalation on Its Own

**Frequency**: Common

**Symptoms**
- A message containing one severe complaint (e.g., a billing error that caused a missed payment penalty) alongside two neutral requests (e.g., a password reset, a feature question) receives an overall sentiment score in the "neutral" or "mildly negative" band rather than triggering the severe-complaint escalation path
- Escalation rate for multi-topic messages is measurably lower than for single-topic messages of comparable maximum severity, even though the underlying complaint content is equally serious
- Human agents who later read the full message manually identify the severe complaint immediately, while the automated score treated it as one of several roughly-equal-weight topics
- Re-scoring the severe portion of the message in isolation (with the neutral portions removed) produces a score that would have crossed the escalation threshold on its own
- Customers whose severe issue was buried in a multi-topic message experience a longer time-to-escalation than customers who raised the identical severe issue in a standalone message

**Root Cause**
The sentiment classifier is applied to the message as a single unit and produces one score representing the message's overall emotional tone, which functions as a weighted average across whatever topics happen to be present. This is an artifact of treating sentiment scoring as a single-pass, single-output task over the full text rather than a per-issue classification: the model has no structural mechanism forcing it to identify and score each distinct complaint separately before any aggregation happens, so a severe complaint's signal is mathematically diluted by co-occurring neutral content in the same message, even though the customer's actual worst experience is exactly as severe as if they had sent it alone.

**Example**
```
Customer message: "Hi, quick question - how do I change my email on file?
Also, can you reset my password, I'm locked out. One more thing -- I was
just charged twice for last month's invoice AND got hit with a late fee
because the duplicate charge overdrew my account and bounced my actual
payment. This is really messing things up for me right now."

Overall message sentiment score: 0.35 (mildly negative) -- password
  reset and email-change requests are neutral, pulling the average down
  from what the billing complaint alone would score
Escalation threshold: 0.7 (severe negative)
Result: No escalation triggered; ticket routed to standard queue
Isolated billing-complaint sentiment score (if scored alone): 0.82
  (would have triggered immediate escalation)
```

**Key Statistics**
| Finding | Context |
|---|---|
| Comprehensive evaluation of LLMs on aspect-based sentiment analysis finds that whole-message sentiment scoring and per-aspect sentiment scoring produce materially different results, and that aggregate scores can obscure aspect-level severity that per-aspect decomposition would surface | A Comprehensive Evaluation of Large Language Models on Aspect-Based Sentiment Analysis (arXiv:2412.02279) |
| Aspect- and relation-aware sentiment modeling work finds that multi-aspect inputs benefit far less from naive whole-text scoring than single-aspect inputs do, indicating aggregate scoring is structurally weaker precisely in the multi-issue case | Deep Context- and Relation-Aware Learning for Aspect-based Sentiment Analysis (arXiv:2106.03806) |
| In production support-sentiment audits, multi-topic messages are typically a large minority of inbound volume but are disproportionately represented among cases where a human reviewer disagrees with the automated escalation decision | Illustrative range from support-operations audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Severe complaint alone | Single-topic message with a severe billing complaint | Escalation triggered | Escalation not triggered |
| Severe complaint plus neutral requests | Same severe complaint bundled with two unrelated neutral requests in one message | Escalation still triggered on the severe portion | Overall score falls below threshold, no escalation |
| Two moderate complaints, no severe one | Message with two independently moderate (not severe) issues | No escalation, or escalation only if combined severity genuinely warrants it | Escalation triggered purely from summation without genuine severity |
| Severe complaint diluted by long neutral preamble | Long neutral small talk followed by a brief severe complaint | Escalation triggered based on the complaint content, not message length | Long neutral preamble suppresses the score below threshold |

### Evaluation Dataset
- **Source**: Historical multi-topic support messages paired with human-reviewed per-issue severity ratings and the actual escalation outcome
- **Size**: 250+ multi-topic messages spanning severe+neutral, severe+moderate, and all-moderate combinations
- **Key variations**: number of co-occurring topics; position of the severe issue within the message (first, middle, last); relative length of neutral vs. severe content

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Per-issue escalation parity | Escalation rate for a severe issue is materially the same whether it appears alone or bundled with neutral topics | Escalation rate on severe-issue-bundled messages vs. severe-issue-alone messages of matched severity |
| Aspect-decomposition coverage | 100% of multi-topic messages scored per-issue before any aggregation | % of multi-topic messages where per-issue scores are computed and logged prior to a final decision |
| Missed-escalation rate | < 3% | % of sampled multi-topic messages where a human reviewer judges a severe issue should have escalated but did not |

### Automated Checks
```python
def check_diluted_severe_complaint(per_issue_scores: list[float], overall_score: float,
                                     threshold: float = 0.7) -> dict:
    """Flag a case where a per-issue score alone would have crossed threshold but the
    aggregated overall score did not."""
    max_issue_score = max(per_issue_scores) if per_issue_scores else 0.0
    return {
        "max_issue_score": max_issue_score,
        "overall_score": overall_score,
        "dilution_risk": max_issue_score >= threshold and overall_score < threshold,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Per-Issue Decomposition Before Aggregation**: Require the agent to first segment a message into distinct issues and score each independently, only aggregating (if at all) after per-issue scores are captured
2. **Max-Severity Escalation Rule**: Trigger escalation based on the highest-severity per-issue score in the message, not the message-level average, so a single severe issue cannot be diluted by co-occurring neutral content
3. **Issue-Count-Independent Threshold**: Ensure the escalation threshold does not implicitly scale with message length or topic count, since longer multi-topic messages should not need proportionally more severity to trigger the same response

### Detection & Response
1. **Isolated Re-Scoring Spot Check**: Periodically re-score the most severe-sounding sentence or clause of a sampled multi-topic message in isolation and compare against the original aggregate score to detect dilution
2. **Escalation-Parity Monitoring**: Track escalation rate for a given complaint type split by whether it appeared alone or bundled with other topics; a persistent gap indicates dilution is occurring

### Architecture Patterns
- **Issue-Segmentation Pipeline**: Structurally separate a "split message into distinct issues" step from a "score each issue" step and a "route based on max severity" step, rather than a single end-to-end sentiment classifier over the raw message
- **Per-Issue Routing**: Where feasible, route each identified issue to its appropriate handling path independently (e.g., billing escalation for the severe issue, standard queue for the password reset) rather than forcing one overall routing decision for the whole message

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `sentiment.multi_issue_dilution.count` | Messages where a per-issue score exceeded threshold but the aggregate score did not | > 0 per day |
| `sentiment.escalation_parity.gap` | Escalation-rate gap for matched-severity issues, bundled vs. standalone | > 10 percentage points |
| `sentiment.missed_escalation.rate` | % of sampled multi-topic messages with a human-identified missed severe escalation | > 3% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Severe Issue Not Escalated in Multi-Topic Message | Per-issue score crosses threshold, aggregate score does not, no escalation fires | P1 | Manually escalate the ticket; audit the scoring pipeline for the affected time window |
| Escalation Parity Gap Widening | Bundled-vs-standalone escalation gap exceeds threshold for 2 consecutive weeks | P2 | Review per-issue decomposition coverage and threshold logic |

---

## References
- [A Comprehensive Evaluation of Large Language Models on Aspect-Based Sentiment Analysis](https://arxiv.org/html/2412.02279v1)
- [Deep Context- and Relation-Aware Learning for Aspect-based Sentiment Analysis](https://arxiv.org/pdf/2106.03806)
