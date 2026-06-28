# Hallucinated Entitlement Tier When Account Lookup Returns Null

## Issue: When a Ticket-Routing Agent's Call to the Account/CRM Lookup Tool for an Incoming Ticket's Customer Fails or Returns No Record (a New Account, a Lookup Timeout, a Sync Delay), the Agent's Priority and Queue-Assignment Decision Asserts a Specific Entitlement Tier Presented as Looked-Up Data, Fabricated to Complete the Routing Decision Rather Than Reflecting Any Actual Account Record

**Frequency**: Occasional

**Symptoms**
- A ticket is routed to (or away from) a priority queue based on a stated entitlement tier ("Enterprise SLA," "Premium Support") that does not match the customer's actual account record when independently checked
- The account-lookup tool call immediately preceding the routing decision, visible in the agent's trace, shows a null result, timeout, or error response rather than a successful record return
- Re-running the same routing decision after the account-lookup call succeeds produces a routing decision citing the customer's genuinely correct entitlement tier, isolating the fabrication to the prior lookup failure
- The fabricated tier is plausible given contextual cues in the ticket text (company size mentioned, tone of the request), making it indistinguishable from a real looked-up value without independently checking the account system
- A ticket from an actual Enterprise-tier customer is routed to a standard queue (or vice versa) because the fabricated tier did not match reality, and the misroute is discovered only after an SLA complaint

**Root Cause**
When the account-lookup tool fails or returns no record, the model can complete its expected routing decision by generating a plausible entitlement tier consistent with contextual cues in the ticket (company name, language suggesting account size), rather than explicitly reporting that the lookup failed and no entitlement data is available. This produces a routing decision that is stylistically indistinguishable from one grounded in a real account lookup, because nothing in the default workflow forces the agent to treat a failed account-lookup call as a hard stop rather than a gap to fill with a plausible completion.

**Example**
```
Ticket-routing agent receives a new ticket from a customer at "Northfield Manufacturing" and calls the account-lookup tool to determine entitlement tier for routing
Account-lookup tool returns a null result because the customer's account was created minutes earlier and has not yet propagated to the lookup system due to a sync delay
Agent's routing decision nonetheless states: "Customer account shows Enterprise SLA tier; routing to priority queue," presenting "Enterprise SLA" as a looked-up fact
The customer's actual account, once synced, shows a standard-tier subscription; the "Enterprise SLA" tier was fabricated based on the company name sounding like a larger organization
Ticket is routed to the priority queue ahead of genuinely Enterprise-tier tickets, consuming priority-queue capacity based on an entitlement tier that was never actually looked up
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by failed or incomplete tool calls, a well-characterized hallucination subtype distinct from a reasoning error over real data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently do not surface a failed or degraded tool call as a hard stop, instead proceeding to generate output as if the call had succeeded | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Business-scenario evaluation of LLM agents in CRM contexts finds that routing and prioritization decisions grounded in unverified or fabricated account attributes are a recurring source of misrouting | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |

**Contributing Factors**
- Routing-decision prompt implicitly rewards a complete, confident-sounding decision, with no explicit instruction that reporting a failed account-lookup call as a hard stop is an acceptable output
- No automated step verifies that the entitlement tier cited in a routing decision matches the value actually returned by the account-lookup tool call in the same session
- Account-lookup failures (null results, timeouts, sync delays) are not surfaced prominently in the agent's output, so a reviewer has no visible signal that the underlying lookup did not succeed

---

## Mitigation Strategies

1. **Mandatory Value Resolution Check**: Before a routing decision is finalized, automatically verify that the cited entitlement tier matches the value actually returned by the account-lookup tool call logged in the same session, flagging any mismatch
2. **Hard Stop on Lookup Failure**: Require the agent to explicitly report a failed, null, or timed-out account-lookup response as a blocking condition, routing to a default neutral-priority queue pending manual verification rather than fabricating a tier
3. **Retry-and-Escalate Policy for New or Unsynced Accounts**: Require a failed account-lookup call to be retried at least once, and if it continues to fail (e.g., due to known sync delay for new accounts), route to a holding queue with an explicit "entitlement pending verification" flag rather than a fabricated tier
4. **Tool-Call Provenance Logging**: Log which specific tool call produced the entitlement tier cited in each routing decision, so any cited tier with no corresponding successful tool-call log entry is automatically flagged as a likely fabrication

### Metrics
- Rate of routing decisions whose cited entitlement tier does not match the logged account-lookup tool-call result
- Number of tickets routed to a priority queue following a routing decision generated despite a logged account-lookup failure
- Mean time-to-detection for fabricated entitlement tiers, measured from routing decision to SLA-complaint-driven correction

### Alerts
- A ticket is routed to a priority queue based on a routing decision whose cited entitlement tier fails value-resolution check against the logged tool-call result → P1
- A routing decision is generated despite a logged account-lookup failure with no retry or holding-queue fallback → P2
- Fabricated-entitlement rate across routing decisions exceeds baseline for two consecutive reporting periods → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
