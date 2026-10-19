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

## Chat assistant examples

### Boilerplate steps that don't match the user's setup
```
Before:
User: How do I export my Dropbox files to my external drive? (signed in on a MacBook, Basic plan)
Bot:  Right-click the Dropbox icon in the Windows taskbar, open Preferences, then choose Sync > Advanced.

After:
User: How do I export my Dropbox files to my external drive? (signed in on a MacBook, Basic plan)
Bot:  I see you're on a Mac. Click the Dropbox icon in the menu bar at the top of the screen, then your profile picture, then Preferences. I'll skip Windows-only options like the taskbar.
```
**What the user experiences:** a Windows menu that does not exist on their Mac, so they conclude the bot did not look at their setup.
**Fix:** before sending steps, read the operating system, app version, and plan from the session and pick the matching instructions; if a step depends on something the session does not show, ask once. See the [re-asks for known information](../../../../../by-capability/human-machine-interface/goals/embedded-copilots/failures/re-asks-for-known-information.md) pattern.

### Keyword-matched documentation instead of an answer
```
Before:
User: My Verizon bill jumped $30 this month. I added a line on the 3rd but the rep said it was free.
Bot:  Here's an article that may help: "Understanding your Verizon bill" (link)

After:
User: My Verizon bill jumped $30 this month. I added a line on the 3rd but the rep said it was free.
Bot:  A $30 increase after adding a line on the 3rd is often a device or activation charge. I can check your invoice for that line now. The article has the full list of charges: (link)
```
**What the user experiences:** a link to a general article that does not mention their line or the $30, so they must read it and still ask the question again.
**Fix:** answer the user's stated situation first, using account data where the bot has access, and attach the article as support for the answer rather than as the answer. See the [generic first response](../../../../../by-capability/human-machine-interface/goals/embedded-copilots/failures/generic-first-response.md) pattern.

---

## References

- [Ticket Routing with ML](https://arxiv.org/abs/1912.08634)
- [Knowledge Base Maintenance & QA](https://arxiv.org/abs/2104.04535)
