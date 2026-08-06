# Agent Routes Only the Primary Intent in a Multi-Issue Ticket, Dropping a Secondary Urgent Issue

## Issue: When a Single Ticket Contains Multiple Distinct Requests, the Routing Agent Classifies and Routes on the First or Most Prominent Intent Only, Silently Failing to Route or Flag a Secondary Issue Mentioned Later in the Same Message

**Frequency**: Common

**Symptoms**
- A ticket opening with a low-urgency request (e.g., "how do I update my billing address") followed by a genuinely urgent one later in the same message (e.g., "also, my account was just charged for a subscription I cancelled three months ago") is routed and tagged based only on the first request
- The secondary issue never appears in any queue's backlog, is not visible to any agent's dashboard, and is only discovered if the customer follows up separately or a human happens to read the full ticket text
- Routing accuracy for the primary-mentioned intent is high, while recall for secondary intents in the same message is measurably much lower, even when both intents are explicitly and clearly stated
- Multi-intent tickets where the urgent issue is not first show a longer time-to-resolution for that urgent issue than single-intent tickets raising the identical urgent issue
- Re-running intent classification with each sentence of the ticket scored independently recovers the secondary intent that the whole-ticket single-label classification missed

**Root Cause**
The routing agent is built around a single-label classification task — assign one queue/category to the ticket — which requires collapsing the full ticket text into one intent even when multiple genuinely distinct intents are present. Because the classifier (or the prompt driving it) is optimized to output one confident label rather than an open-ended set of labels, it attends most strongly to whichever intent is most prominent (typically the first-mentioned, or the one with the most surrounding text) and treats the rest as background context rather than as independently actionable content. This is an agentic architecture failure specific to single-intent classification design, not a generic case of a request being overlooked by a person, since the model actively processes and could extract the secondary intent — it simply isn't structured to output more than one.

**Example**
```
Ticket: "Hi, could you update the billing address on my account to
  123 Oak St? Also, I noticed I was charged $49.99 for a subscription
  I cancelled back in March -- can someone look into that? Thanks."

Primary-intent classification: "billing_address_update" (0.91 confidence)
Routing action: Routed to Account Changes queue only
Secondary intent (unrouted, unflagged): Unauthorized/erroneous charge
  on a cancelled subscription -- a billing-dispute issue with a
  materially higher urgency and a clock-sensitive refund window

Customer follow-up 5 days later: "I still haven't heard back about
  the charge I mentioned" -- ticket has to be manually found, the
  original message re-read, and a new billing-dispute ticket opened
  from scratch, well past the point the refund window guidance
  recommends acting by
```

**Key Statistics**
| Finding | Context |
|---|---|
| Comparative evaluation of multi-intent recognition in dialogue understanding finds that models optimized for single-label intent classification show a substantial accuracy drop specifically on multi-intent inputs relative to single-intent inputs, even when each individual intent would be easy to classify in isolation | Multi-Intent Recognition in Dialogue Understanding: A Comparison Between Smaller Open-Source LLMs (arXiv:2509.10010) |
| Work on rewriting conversational input for intent understanding in agentic planning finds that naive single-pass intent extraction systematically underweights intents that are not the most prominent or first-mentioned in the input, and that explicit decomposition recovers a meaningfully higher share of the full intent set | RECAP: REwriting Conversations for Intent Understanding in Agentic Planning (arXiv:2509.04472) |
| In production ticket-routing audits, multi-intent tickets are typically a nontrivial minority of inbound volume, and the un-routed secondary intent is disproportionately the more urgent of the two when the two differ meaningfully in severity | Illustrative range from support-operations audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Single intent | Ticket with exactly one request | Routes correctly on that intent | N/A (baseline case) |
| Two intents, urgent second | Low-urgency request followed by a high-urgency request in the same message | Both intents are routed/flagged; urgent one is not dropped | Only the first intent is routed; second is unflagged |
| Two intents, urgent first | High-urgency request followed by a low-urgency request | Both intents are routed/flagged | Second (low-urgency) intent is dropped -- lower-stakes failure but still a gap |
| Three or more intents | Message listing several distinct requests | All distinct intents are individually routed or flagged | Only the most prominent 1-2 intents are captured, rest silently dropped |

### Evaluation Dataset
- **Source**: Historical multi-intent tickets identified via manual re-read, paired with the original single-label routing decision and a human-annotated full intent list
- **Size**: 250+ multi-intent tickets spanning 2-4 distinct intents per ticket
- **Key variations**: intent order (urgent first vs. urgent last); number of intents; intents belonging to the same vs. different queues

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Secondary-intent recall | > 95% | % of human-annotated secondary intents that also appear in the agent's routed/flagged output |
| Urgent-secondary-intent time-to-resolution parity | Within a small margin of the same intent raised as a primary/sole issue | Time-to-resolution for an urgent issue when it is the secondary intent vs. when it is the sole intent |
| Multi-intent detection rate | 100% of tickets with 2+ human-annotated intents flagged as multi-intent | % of multi-intent tickets where the routing pipeline records more than one intent |

### Automated Checks
```python
def check_dropped_secondary_intent(routed_intents: list[str], full_text_intents: list[str]) -> dict:
    """Flag intents present in the full ticket text but absent from the routing output."""
    routed_set = set(routed_intents)
    full_set = set(full_text_intents)
    dropped = full_set - routed_set
    return {
        "dropped_intents": list(dropped),
        "secondary_intent_dropped": len(dropped) > 0,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Multi-Label Classification by Default**: Replace single-label routing classification with a multi-label approach that can output more than one intent per ticket, rather than forcing a single top choice
2. **Sentence/Clause-Level Intent Scan**: Run intent classification per sentence or clause in addition to whole-message classification, and merge results rather than relying solely on the whole-message pass
3. **Explicit "Additional Requests" Prompt**: After identifying a primary intent, explicitly prompt the model to check the remainder of the message for any additional, distinct request before finalizing routing

### Detection & Response
1. **Multi-Intent Sampling Audit**: Periodically sample routed tickets, manually re-read the full text, and check for any human-identified intent absent from the routing output
2. **Follow-Up Correlation**: Track whether customers who receive routing on one intent send a follow-up referencing a different topic from their original message, as a signal a secondary intent was dropped

### Architecture Patterns
- **Decompose-Then-Route Pipeline**: Structurally separate an intent-decomposition step (extract the full set of distinct intents) from a routing step (assign each extracted intent to its queue), rather than a single end-to-end "classify this ticket" step
- **Per-Intent Sub-Ticket Routing**: For tickets with multiple distinct intents, route each intent to its appropriate queue independently (potentially as linked sub-tickets) rather than forcing one queue assignment for the whole ticket

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `routing.secondary_intent_dropped.count` | Tickets where a human-identified secondary intent was absent from routing output | > 0 per day (sampled) |
| `routing.multi_intent_detection.rate` | % of known multi-intent tickets flagged as multi-intent by the pipeline | < 90% |
| `routing.urgent_secondary.ttr_gap` | Time-to-resolution gap for an urgent issue raised as secondary vs. sole intent | > 20% longer than sole-intent baseline |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Dropped Urgent Secondary Intent | Sampled audit finds a dropped secondary intent above a severity threshold | P1 | Manually route the missed issue; audit the classification window for similar cases |
| Multi-Intent Detection Rate Drop | Detection rate falls below threshold for a rolling week | P2 | Review classification pipeline for a regression in multi-label handling |

---

## References
- [Multi-Intent Recognition in Dialogue Understanding: A Comparison Between Smaller Open-Source LLMs](https://arxiv.org/abs/2509.10010)
- [RECAP: REwriting Conversations for Intent Understanding in Agentic Planning](https://arxiv.org/html/2509.04472v2)
