# Multi-Agent Handoff Drops Elevated-Risk Flag Before Purchase-Order Finalization

## Issue: A Supplier-Risk Agent Raises an Elevated-Risk Flag on a Supplier, but the Procurement Agent That Subsequently Finalizes a Purchase Order Against That Supplier Operates From a Task Description or Intermediate Summary That Does Not Carry the Flag Forward, Resulting in the Purchase Order Being Finalized as If No Risk Flag Existed

**Frequency**: Occasional

**Symptoms**
- A purchase order is finalized against a supplier that has an active, unresolved elevated-risk flag recorded in the supplier-risk system, with no indication in the procurement agent's reasoning that the flag was considered
- Inspecting the handoff between the supplier-risk agent and the procurement agent shows the flag was recorded in the risk system but not included in the summary or task description passed to the procurement agent
- Querying the supplier-risk system directly, after the purchase order is finalized, surfaces the flag as having been active and unresolved at the time the order was placed
- The gap is most visible for suppliers whose risk flag was raised in a separate workflow or session from the one in which the purchase order is generated, since same-session handoffs are more likely to carry the flag forward implicitly
- Procurement staff reviewing the finalized purchase order have no visible indication that a risk flag exists unless they separately and manually check the supplier-risk system

**Root Cause**
When two agents operate on different stages of the same workflow, the receiving agent's effective context is whatever is explicitly included in the task description, summary, or handoff payload it is given -- not the full state of every upstream system. If the procurement agent's task description is generated from a template or summary that does not query the supplier-risk system's current flag status as a required field, an elevated-risk flag raised by a separate agent simply does not appear in the procurement agent's input, and the purchase order proceeds as if the supplier were unflagged.

**Example**
```
Supplier-risk agent raises an elevated-risk flag on Supplier Y following a financial-distress signal detected during a routine monitoring run
Flag is recorded in the supplier-risk system as active and unresolved
Two weeks later, a procurement agent is tasked with finalizing a purchase order against Supplier Y for a routine reorder, working from a task description generated from the standard purchase-order template
Task description does not include a query to the supplier-risk system's current flag status, since that field is not part of the standard template
Procurement agent finalizes the purchase order with no consideration of the active risk flag
Supplier-risk system, queried separately during an unrelated audit, shows the flag was active and unresolved throughout the purchase-order process
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Failure-mode analysis of multi-agent LLM systems identifies information loss at agent handoffs as a leading failure category, distinct from either agent's individual reasoning errors, arising when a receiving agent's task framing does not carry forward state established by an upstream agent | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Failure-mode analysis of platform-orchestrated agentic workflows documents handoff-boundary information loss as a recurring root cause when downstream agents operate from templated task descriptions rather than a full upstream state query | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic LLMs in the supply chain identifies cross-agent state consistency, particularly for risk flags spanning separate monitoring and procurement workflows, as a distinct reliability requirement from either workflow's individual correctness | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- The procurement agent's task-description template does not include a required field querying the supplier-risk system's current flag status for the target supplier
- The supplier-risk flag and the purchase-order workflow are managed by separate agents operating in separate sessions, with no shared, automatically-checked state between them
- No automated gate blocks purchase-order finalization for a supplier with an active, unresolved elevated-risk flag

---

## Mitigation Strategies

1. **Mandatory Risk-Flag Query in Purchase-Order Task Description**: Require every procurement-agent task description to include a current query of the supplier-risk system's flag status for the target supplier as a required field, not an optional or templated-out one
2. **Automated Purchase-Order Block on Active Risk Flag**: Implement an automated gate that blocks purchase-order finalization for any supplier with an active, unresolved elevated-risk flag, requiring explicit override and justification to proceed
3. **Shared Structured State Between Risk and Procurement Workflows**: Maintain supplier-risk flags in a structured, shared state that both the supplier-risk agent and the procurement agent query directly, rather than relying on a handoff summary to carry the flag forward
4. **Handoff Completeness Audit**: Periodically audit a sample of agent-to-agent handoffs to verify that all currently-active flags or holds on the relevant entity were included in the downstream agent's task description

### Metrics
- Rate of finalized purchase orders against suppliers with an active, unresolved elevated-risk flag at time of order
- Rate of procurement-agent task descriptions missing a current supplier-risk flag-status query
- Mean time between a risk flag being raised and its absence being detected in a downstream purchase-order process

### Alerts
- A purchase order is finalized against a supplier with an active, unresolved elevated-risk flag and no override justification recorded → P1
- A procurement-agent task description is generated without a supplier-risk flag-status query for the target supplier → P2
- Handoff-completeness audit finds a missing active flag in a downstream task description → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
