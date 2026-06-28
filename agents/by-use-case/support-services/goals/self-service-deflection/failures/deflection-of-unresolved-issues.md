# Deflection of Unresolved Issues

## Issue: Self-Service Agent Marks a Conversation as "Deflected" (Resolved Without Human Agent) Based on the Customer Not Replying, Rather Than the Issue Actually Being Resolved

**Frequency**: Very Common

**Symptoms**
- Conversation is logged as successfully self-service-resolved whenever the customer does not send a follow-up message within a timeout window, regardless of whether the bot's last response actually answered the question
- Deflection rate (a key cost-saving metric for self-service tooling) looks strong while actual issue resolution, measured independently, is lower
- Customers who give up due to frustration (bot loop, unhelpful answer) are counted identically to customers whose issue was genuinely resolved, since both produce the same "no further reply" signal
- Customers who abandon self-service and contact support through a different channel shortly after are not linked back to the "deflected" conversation, so the false deflection is never corrected in the metric

**Root Cause**
Deflection is operationally defined and measured as "conversation ended without escalation to a human agent," which is a behavioral proxy for resolution, not a direct measurement of it. Silence after a bot's response is consistent with both successful resolution and customer abandonment from frustration, and without an explicit confirmation signal or downstream tracking to detect re-contact through another channel, the metric cannot distinguish between the two — it structurally rewards driving customers away as much as it rewards actually helping them.

**Example**
```
Scenario: Customer asks self-service bot about a billing discrepancy
Bot: Provides a generic FAQ answer that does not address the specific discrepancy
Customer: Does not reply further (gives up, frustrated), closes the chat window
System: Logs conversation as "deflected" (successful self-service resolution)
Customer: Contacts support via phone the next day about the same unresolved billing issue
Linkage: Phone contact not connected back to the original "deflected" chat in metrics
Impact: Deflection rate is overstated; actual resolution rate and customer effort are misrepresented
```

**Key Statistics**
- Industry research on self-service and chatbot deflection metrics consistently flags the gap between "deflected" and "actually resolved" as a major measurement validity concern
- Cross-channel re-contact within a short window after a "deflected" self-service conversation is a recommended proxy for detecting false deflections, per customer experience measurement practice
- Explicit resolution confirmation (asking the customer to confirm their issue was resolved) has been shown to produce meaningfully lower apparent deflection rates than silence-based deflection counting, revealing the gap between the two measures

---

## Mitigation Strategies

1. **Explicit Resolution Confirmation**: Require an explicit "was this resolved?" confirmation step before counting a conversation as deflected, rather than inferring resolution from the absence of a follow-up message
2. **Cross-Channel Re-Contact Linking**: Track whether a customer re-contacts through any channel within a defined window after a "deflected" conversation on the same topic, and retroactively reclassify linked conversations as false deflections
3. **Resolution Rate as the Primary Metric, Deflection as Secondary**: Report actual confirmed-resolution rate alongside deflection rate, and treat deflection-without-confirmation as a lower-confidence, secondary signal
4. **Bot-Loop and Abandonment Detection**: Detect behavioral signals of frustration (repeated rephrasing of the same question, abrupt mid-flow exit) and exclude those conversations from the deflected/resolved count by default

### Metrics
- Confirmed resolution rate vs. silence-based deflection rate (the gap between them)
- Cross-channel re-contact rate within a defined window after a "deflected" conversation
- Bot-loop/abandonment-pattern detection rate among conversations counted as deflected

### Alerts
- Cross-channel re-contact rate for "deflected" conversations on the same topic exceeds a defined threshold → P2
- Gap between confirmed-resolution rate and silence-based deflection rate widens beyond a defined margin → P2

---

## References

- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519)
