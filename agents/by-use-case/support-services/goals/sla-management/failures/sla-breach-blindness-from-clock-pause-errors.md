# SLA Breach Blindness from Clock-Pause Errors

## Issue: Agent Incorrectly Pauses or Resumes the SLA Response-Time Clock When a Ticket Status Changes, Masking an Actual SLA Breach

**Frequency**: Common

**Symptoms**
- SLA clock is paused whenever a ticket moves to "waiting on customer" status, but the agent applies this pause even when the actual cause of delay is internal (waiting on engineering, waiting on a vendor) and has been mislabeled
- Clock pause is not resumed promptly when the customer responds, so elapsed time during which the ticket should be counting toward breach continues to be excluded
- Tickets reassigned between teams reset or incorrectly recalculate elapsed SLA time, understating true time-to-resolution
- SLA compliance dashboards report healthy compliance rates while actual customer-perceived response time, including agent-side delays hidden by clock-pause logic, is far worse

**Root Cause**
SLA clock-pause logic is typically implemented as a status-field trigger (pause on "waiting on customer," resume on "customer responded") rather than a verified causal check on who is actually responsible for the current delay. When status fields are used loosely or inconsistently by agents (e.g., marking a ticket "waiting on customer" to stop the clock while actually waiting on an internal team), or when status transitions are not promptly reflected, the clock-pause mechanism systematically miscounts elapsed time, producing SLA compliance metrics that are accurate to the recorded status history but not to actual customer-experienced wait time.

**Example**
```
Scenario: Ticket requires engineering investigation; agent sets status to "waiting on customer" to stop the SLA clock while actually waiting on an internal engineering ticket
SLA clock: Paused based on status field, regardless of actual wait cause
Engineering investigation: Takes 5 days
SLA dashboard: Reports this ticket as SLA-compliant because the clock was paused for those 5 days
Actual customer experience: 5-day wait with no agent action, indistinguishable from an SLA breach from the customer's perspective
Impact: SLA compliance metrics are systematically inflated relative to actual customer-experienced response time
```

**Key Statistics**
- Status-field-based SLA clock manipulation (intentional or inadvertent) is a recognized gaming/measurement-integrity risk in support operations metrics literature
- Discrepancy between reported SLA compliance and actual customer-perceived wait time is a commonly cited driver of customer satisfaction scores diverging from SLA compliance scores
- Verified-cause clock-pause logic (requiring an actual outbound customer-facing question before pausing) has been shown in support operations practice to produce SLA metrics that track customer-perceived experience more closely than status-field-only logic

---

## Mitigation Strategies

1. **Verified-Cause Pause Logic**: Only pause the SLA clock when there is a verifiable outbound question to the customer (e.g., an actual sent message awaiting reply), not merely a status field set to "waiting on customer"
2. **Immediate Resume on Customer Response**: Resume the SLA clock immediately and automatically when a customer response is received, with monitoring for any lag between response receipt and clock resumption
3. **Internal-Wait Visibility**: Track internal wait time (waiting on engineering, vendor, etc.) as a separate, visible metric rather than allowing it to be absorbed into customer-wait-pause time
4. **Dual Metric Reporting**: Report both status-based SLA compliance and an independently computed actual-elapsed-time metric, and investigate divergence between the two as a measurement integrity signal

### Metrics
- Divergence between status-based SLA compliance rate and actual-elapsed-time-based compliance rate
- Average internal wait time misattributed to "waiting on customer" status, where detectable
- Time lag between customer response receipt and SLA clock resumption

### Alerts
- Status-based and actual-elapsed-time SLA compliance rates diverge beyond a defined threshold for a team/queue → P2
- SLA clock remains paused more than a defined time after a customer response is received → P2

---

## References

- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
