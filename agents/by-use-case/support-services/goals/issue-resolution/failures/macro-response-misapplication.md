# Macro Response Misapplication

## Issue: Agent Selects a Pre-Written Macro/Canned Response Based on Surface Keyword Match Without Verifying It Actually Addresses the Customer's Specific Situation

**Frequency**: Very Common

**Symptoms**
- Customer's message contains a keyword that matches a macro's trigger pattern, but the macro's content addresses a different scenario than the one the customer actually described
- Agent sends the macro response with minimal or no customization, even when the customer's message contains details that materially change which guidance applies
- Customer replies expressing confusion or repeats their original question, indicating the macro did not actually address their situation, but this signal is not fed back into macro-selection quality tracking
- High macro-usage rate is reported as an efficiency win without corresponding tracking of whether macro-resolved tickets have higher repeat-contact or escalation rates than fully custom-written responses

**Root Cause**
Macro-selection logic commonly operates on keyword or intent-classification similarity between the customer's message and a macro's trigger conditions, which captures topical relevance but not situational fit — a macro written for "refund request, standard return window" can keyword-match a message about "refund request, item damaged in shipping" while being substantively wrong for that specific scenario. Without a verification step that checks the customer's stated specifics against the macro's actual applicability conditions, surface-level topical matching is treated as sufficient grounds for sending a fixed response.

**Example**
```
Scenario: Customer message: "I want a refund, the item arrived damaged"
Macro selected: "Standard Return Window Refund Policy" (matched on "refund" keyword)
Macro content: Describes the standard 30-day return policy and return shipping process
Actual applicable policy: Damaged-in-shipping items qualify for an immediate refund/replacement without standard return shipping, under a different policy
Customer: Confused, replies asking why they need to pay for return shipping on a damaged item
Impact: Incorrect guidance sent, requiring a follow-up exchange to correct
```

**Key Statistics**
- Template/macro misapplication due to surface keyword matching rather than situational verification is a recurring theme in support automation quality research
- Tickets resolved via misapplied macros show measurably higher rates of follow-up contact and customer-expressed confusion compared to situationally-verified responses, per support operations quality studies
- Macro-usage-rate-only efficiency tracking (without paired quality/repeat-contact tracking) is identified as a metric design gap that can mask declining resolution quality

---

## Mitigation Strategies

1. **Applicability Condition Verification**: Before sending a macro, require the agent to check the customer's stated specifics against the macro's actual applicability conditions, not just its trigger keywords
2. **Macro Quality Pairing with Repeat-Contact Tracking**: Track repeat-contact and customer-confusion-signal rates specifically for macro-resolved tickets, broken out by which macro was used, to identify misapplication-prone macros
3. **Mandatory Customization for Edge-Case Indicators**: When the customer's message contains specifics outside the macro's standard applicability conditions (e.g., "damaged," "wrong item," "fraud"), require custom handling rather than macro auto-send
4. **Macro Library Curation**: Regularly review and retire or refine macros with above-average repeat-contact rates following their use

### Metrics
- Repeat-contact rate for macro-resolved tickets, broken out by macro
- % of macro selections that passed an applicability-condition verification check vs. keyword match alone
- Customer-confusion-signal rate (explicit "that doesn't answer my question" type replies) following macro use

### Alerts
- A specific macro's repeat-contact rate exceeds the support team's average by a defined margin → P2
- Macro auto-sent for a message containing an edge-case indicator (damaged, wrong item, fraud) without custom handling → P2

---

## References

- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
