# Canned Response Context Mismatch

## Issue: Agent Selects a Templated/Canned Response That Matches Surface Keywords but Misses the Customer's Actual Situation

**Frequency**: Very Common

**Symptoms**
- Agent replies with a macro about "resetting your password" when the customer's message mentions "password" only in passing while describing a billing issue
- Canned response references account features, plan tiers, or product versions the customer does not actually have
- Customer has to reply "that's not my issue" before the actual problem is addressed, adding a full round-trip to resolution time
- High macro-usage rate correlates with lower first-contact-resolution rate for agents/queues that lean heavily on canned responses
- CSAT comments specifically mention feeling like they received a "form letter" or weren't read carefully

**Root Cause**
Canned-response selection is commonly driven by keyword or embedding similarity between the incoming message and a library of macro titles/triggers, optimized for retrieval speed rather than situational fit. This retrieval step does not verify that the customer's full context — account state, plan, prior ticket history, the specific clause of their complaint — matches the preconditions the macro assumes. Because canned responses are pre-written to be broadly applicable, a moderately-similar match still looks plausible enough to pass automated confidence thresholds, even when it does not address the specific situation.

**Example**
```
Customer message: "I tried to update my payment method but it says my password is wrong"
Top macro match (keyword "password"): "How to Reset Your Password" macro
Actual issue: Payment method update form, unrelated authentication bug
Agent sends: Password reset macro
Customer reply: "I'm not trying to log in, I'm trying to update my card and it broken at that step"
Impact: One extra round-trip, customer frustration, original payment-form bug remains unlogged
```

**Key Statistics**
- Ticket routing and response-suggestion systems using keyword/embedding similarity report measurable rates of top-1 retrieval mismatch when message intent is multi-topic or ambiguous, per ML-based ticket routing literature
- Macro/canned-response usage rate is inversely correlated with first-contact-resolution rate in support operations benchmarking when macro selection is not preceded by an intent-verification step
- Reopen and re-contact rates rise measurably when initial responses are templated without confirming applicability to account-specific context

---

## Mitigation Strategies

1. **Precondition Verification Before Send**: Require canned responses tied to account state (plan tier, feature availability, product version) to verify those preconditions against the actual account before sending, not just text similarity to the trigger phrase
2. **Multi-Topic Detection**: Flag messages that reference multiple potential topics (e.g., both "password" and "payment") for confidence-reduced macro matching or human review rather than auto-selecting the top keyword match
3. **Confirmation Framing**: When macro confidence is below a high threshold, prepend a confirming question ("It sounds like this might be about X — is that right?") rather than asserting the macro's content as the answer
4. **Macro Usage vs. FCR Correlation Tracking**: Monitor first-contact-resolution rate segmented by macro usage to detect macros or trigger rules producing systematically poor fit

### Metrics
- First-contact-resolution rate for macro-assisted responses vs. fully custom responses
- Re-contact rate within 24 hours of a canned response being sent
- Macro-match confidence score distribution at send time

### Alerts
- A specific macro's re-contact rate exceeds the queue baseline by a defined margin → P2
- Macro sent with below-threshold match confidence and no confirmation step → P3

---

## References

- [Ticket Routing with ML](https://arxiv.org/abs/1912.08634)
- [Knowledge Base Maintenance & QA](https://arxiv.org/abs/2104.04535)
