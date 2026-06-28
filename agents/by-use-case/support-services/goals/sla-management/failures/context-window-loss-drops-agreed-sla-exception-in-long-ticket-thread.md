# Context-Window Loss Drops Agreed SLA Exception in Long Ticket Thread

## Issue: On a Long-Running Support Ticket Thread, an Earlier Message Records an Explicitly Agreed SLA Exception (an Extended Resolution Window Because of a Customer-Side Blocker), but as the Thread Grows and Earlier Turns Fall Out of the Agent's Effective Context, a Later SLA-Monitoring Pass Flags or Escalates the Ticket as a Breach Despite the Exception Still Being in Effect

**Frequency**: Common

**Symptoms**
- An SLA-breach escalation fires on a ticket whose own thread history contains an earlier message explicitly recording an agreed extension, with the escalation showing no awareness that the exception exists
- Asking the agent, at escalation time, "was an SLA exception agreed for this ticket?" produces a negative or uncertain answer, even though the exception is stated plainly earlier in the same thread
- Re-running the same SLA check with the exception explicitly re-stated in the prompt (rather than relying on it persisting from earlier in the thread) correctly suppresses the escalation, isolating context loss as the cause
- The dropped exception concentrates on tickets with unusually long threads -- many back-and-forth messages with the customer or internal notes -- where the exception-granting message is furthest from the current point in the conversation
- Support manager has to manually re-confirm and re-document the exception every time the thread grows past a certain length, because the system's own SLA monitoring keeps losing track of it

**Root Cause**
SLA monitoring that re-evaluates a long ticket thread's compliance status by reasoning over the full conversational history can lose track of an earlier-stated exception once the thread grows long enough that the granting message falls outside the portion of the conversation the model effectively attends to, even within nominal context-window limits. When the exception exists only as a natural-language statement in an earlier message, rather than as a persistent, structured ticket attribute the SLA-monitoring step explicitly checks on every evaluation, the monitoring pass has no reliable way to know the exception was ever granted.

**Example**
```
Message 4 of a support ticket thread: Support rep writes, "Customer confirmed they need until the 20th to provide the required network logs before we can proceed -- extending resolution SLA to the 22nd per policy, agreed with customer"
Messages 5 through 38: Thirty-four more messages cover troubleshooting steps, customer follow-ups, and internal notes over the following two weeks
Message 39: Automated SLA-monitoring pass re-evaluates the ticket against its original resolution deadline (predating the extension) and fires a breach escalation to the support manager
The extension recorded in message 4 is not reflected anywhere in the structured ticket record the monitoring pass actually checks, only in the conversational thread, which the monitoring pass does not fully re-read
Support manager has to manually trace back through the thread to find the original extension agreement and suppress the escalation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts and constraints as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established facts to be dropped in long-running interactions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Business-scenario evaluation of LLM agents in CRM and support contexts identifies SLA- and policy-state tracking across long interaction histories as a recurring evaluation gap | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |

**Contributing Factors**
- SLA exceptions are recorded only as natural-language statements within the ticket thread, with no structured `sla_exception` field that persists independently of thread length
- SLA-monitoring passes evaluate compliance against the ticket's structured deadline field without re-reading the full conversational thread for exception language
- No automated check flags when a thread contains exception-granting language with no corresponding structured field before an escalation fires

---

## Mitigation Strategies

1. **Structured SLA-Exception Field**: Require any agreed SLA exception to be recorded as a structured field on the ticket (new deadline, reason, approver) at the moment it is granted, rather than only as a message in the thread, and have SLA monitoring check this field directly
2. **Pre-Escalation Exception Check**: Before an SLA-breach escalation fires, automatically check the ticket's structured exception field, and additionally scan the thread for exception-granting language with no corresponding structured field, surfacing a warning rather than auto-escalating if a mismatch is found
3. **Exception Confirmation at Thread-Length Threshold**: Once a ticket thread exceeds a defined length, require any active SLA exception to be explicitly re-confirmed and re-recorded as a structured field, rather than relying on the original message remaining discoverable
4. **Periodic SLA-State Summary in Long Threads**: At regular intervals in a long-running ticket, surface a structured summary of the current SLA deadline and any active exceptions, making the state visible to both agents and support staff without requiring a full thread re-read

### Metrics
- Rate of SLA-breach escalations later found to have an agreed exception recorded earlier in the same thread
- Percentage of agreed SLA exceptions recorded as a structured field at grant time versus thread-message-only
- Average ticket thread length (message count) at the point an exception is lost from SLA monitoring

### Alerts
- An SLA-breach escalation fires for a ticket whose thread contains an earlier exception-granting message with no corresponding structured field → P1
- A ticket thread exceeds the length threshold with an active exception that has not been re-confirmed as a structured field → P3
- Exception-loss rate across long-running tickets exceeds baseline for two consecutive reporting periods → P3

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
