# Stale Training Knowledge Overrides Live Escalation Policy Lookup

## Issue: An Alert-Routing Agent With a Live Escalation-Policy Lookup Tool Available Defaults to the Generic or Outdated Ownership Convention It Recalls From Pretraining or an Earlier Session -- e.g., "Database Alerts Page the DBA Team" -- Instead of Calling or Trusting the Live Tool's Output Reflecting a Recent Reorg That Moved That Ownership to a Platform Team, Paging the Wrong Team Even Though the Correct Answer Was One Tool Call Away

**Frequency**: Occasional

**Symptoms**
- Agent pages a team whose ownership of the alerting service was reassigned weeks or months earlier, even though a live escalation-policy lookup tool exists and was available for this routing decision
- The agent's own reasoning trace cites a generic or remembered convention ("database alerts typically route to the DBA team") rather than a specific, freshly retrieved policy record
- When the same alert is re-routed manually with the lookup tool explicitly forced into the decision path, the agent (or a human) reaches the current, correct team
- The mis-routed team reports they have not owned this alert class "in months," indicating the gap is not a one-off data error but a standing staleness between the agent's default assumption and current policy
- Frequency of this misroute spikes immediately after a team reorg or ownership transfer and tapers off over subsequent weeks as the agent's session-level cache or recent context accumulates corrected examples

**Root Cause**
The model's parametric knowledge encodes generic, frequently-seen ownership conventions from its training corpus (e.g., "DB issues go to DBAs"), and absent an explicit instruction to treat the live policy-lookup tool's result as authoritative over its own recalled convention, the agent treats a confident internal prior as sufficient grounds to skip or discount the tool call. Even when the tool is called, the agent can pattern-match the live result against its stronger prior and silently prefer the prior when the two seem to conflict, rather than flagging the discrepancy for review.

**Example**
```
Service "billing-db" alert fires: "connection pool exhausted"
Escalation-policy lookup tool is available and, if called, would return: "billing-db owned by platform-data team as of last quarter's reorg"
Agent's routing decision: pages "DBA-oncall" team, citing in its reasoning "database connection issues route to the DBA team"
DBA-oncall has not owned billing-db since the reorg three months prior; they have no current runbook or access for this service
Platform-data team (the actual current owner) is not paged; resolution is delayed 40 minutes until DBA-oncall manually re-routes the page
Post-incident review finds the escalation-policy lookup tool was available and functioning the entire time but its output was never weighted into the final routing decision
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented agents frequently underweight retrieved evidence in favor of parametric priors when the two conflict, especially for high-frequency conventional associations seen heavily in training data | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Tool-use miscalibration research finds agents do not reliably treat a successfully retrieved tool result as overriding their own prior belief, producing decisions inconsistent with available evidence | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Memory and tool-grounding research for autonomous LLM agents identifies stale parametric knowledge competing with live retrieval as a distinct, recurring failure class separate from retrieval failure itself | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- No explicit policy requiring the live escalation-policy tool's result to be treated as authoritative over the agent's own recalled convention when the two diverge
- No discrepancy-detection step that flags when the agent's chosen team differs from what the lookup tool would return, even when the tool was called
- Recent reorgs and ownership transfers are not surfaced to the agent as a heightened-staleness-risk window requiring extra verification
- The agent's reasoning trace is not required to cite the specific lookup-tool record it used, making silent reliance on a generic prior hard to detect after the fact

---

## Mitigation Strategies

1. **Mandatory Tool-Result Citation**: Require the agent's routing decision to cite the specific record returned by the escalation-policy lookup tool, not a generic convention, before a page is sent
2. **Discrepancy Flag on Divergence**: Automatically flag and hold for human review any routing decision where the agent's chosen team differs from what the live lookup tool's most recent record would indicate
3. **Reorg Cooldown Window**: For a configurable period after a known ownership transfer, require double confirmation (lookup tool plus a secondary ownership source) before auto-paging
4. **Tool-Result Precedence Rule**: Explicitly instruct the agent that a successfully returned live policy record always takes precedence over any remembered or pattern-matched convention

### Metrics
- Rate of routing decisions where the paged team differs from the most recent escalation-policy lookup record
- Mean time between an ownership-transfer event and the agent's routing decisions consistently reflecting the new owner
- Number of incidents requiring manual re-routing after an initial agent-routed page

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Routing/policy mismatch | Agent pages a team that differs from the live lookup tool's current record | P1 | Re-route immediately to the lookup tool's indicated owner; audit decision trace |
| Post-reorg misroute cluster | Multiple misroutes to a pre-reorg owning team within the cooldown window | P2 | Force secondary-source confirmation for affected services |
| Stale-convention recurrence | Same generic convention cited in routing reasoning across multiple incidents post-reorg | P3 | Review and patch agent's escalation-routing instructions |

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
