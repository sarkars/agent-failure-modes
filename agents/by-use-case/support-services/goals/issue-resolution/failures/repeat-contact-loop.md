# Repeat Contact Loop

## Issue: Agent Resolves Each Support Contact From a Customer in Isolation, Failing to Recognize That the Same Underlying Issue Has Been "Resolved" Multiple Times Without Actually Being Fixed

**Frequency**: Very Common

**Symptoms**
- A customer contacts support multiple times over days or weeks for what the agent classifies as separate, unrelated issues, when they are actually repeated symptoms of one unresolved root problem
- Each contact is closed as "resolved" based on the immediate workaround applied, without checking the customer's contact history for prior occurrences of the same symptom
- Customer satisfaction and effort scores degrade with each repeat contact, but the agent's per-ticket resolution metric looks healthy because each individual ticket is closed
- Root-cause fix (e.g., a backend bug, a billing system defect) is never escalated for permanent resolution because each surface-level contact is treated as a one-off

**Root Cause**
Support agents optimized to resolve the immediate, presenting issue in front of them — and measured on per-contact resolution rate — have no built-in incentive or mechanism to look backward across a customer's contact history for recurrence patterns. Without an explicit cross-contact pattern-matching step, repeated workarounds for the same underlying defect each look like an independent successful resolution, masking a root cause that is actually generating ongoing customer harm and repeat support cost.

**Example**
```
Scenario: Customer contacts support 4 times in 3 weeks, each time reporting a failed payment on the same recurring subscription
Each contact: Agent applies a manual workaround (re-processes the payment), closes ticket as "resolved"
Pattern not checked: Customer's contact history shows this is the 4th occurrence of the identical symptom
Root cause: A billing system defect causing intermittent payment processing failures for this subscription type — never escalated
Impact: Customer experiences repeated friction; root cause continues affecting other customers with the same subscription type
```

**Key Statistics**
- Repeat contact rate is a widely used customer experience metric specifically because it captures the gap between "ticket closed" and "issue actually resolved" that per-ticket resolution metrics miss
- Platform-orchestrated agentic workflow failure research identifies lack of cross-session/cross-contact state awareness as a recurring lifecycle failure pattern in automated support systems
- Root-cause escalation triggered by repeat-contact pattern detection has been shown in customer experience operations research to reduce both repeat contact volume and overall support cost compared to per-ticket-only resolution metrics

---

## Mitigation Strategies

1. **Mandatory Contact History Check**: Before closing any ticket, require the agent to check the customer's recent contact history for matching or similar symptoms, not just resolve the presenting issue in isolation
2. **Repeat-Contact Pattern Escalation**: Automatically escalate to root-cause investigation when the same customer (or a cluster of customers) reports the same symptom more than a defined number of times within a window
3. **Resolution Quality Metric, Not Just Closure Rate**: Track repeat contact rate alongside ticket closure rate as a primary support quality metric, so workaround-only resolutions are visible as a cost, not a pure success
4. **Workaround vs. Permanent Fix Tagging**: Require agents (or the resolution agent) to explicitly tag whether a resolution is a workaround or a permanent fix, and route workaround-tagged repeat issues to engineering/root-cause review

### Metrics
- Repeat contact rate (same customer, same/similar symptom, within a defined window)
- % of resolutions tagged as workaround vs. permanent fix
- Time from first occurrence of a recurring symptom pattern to root-cause escalation

### Alerts
- Same customer contacts support for the same symptom more than a defined threshold within a window without root-cause escalation → P2
- Workaround-tagged resolution rate for a given symptom category exceeds a defined threshold across multiple customers → P1

---

## References

- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
