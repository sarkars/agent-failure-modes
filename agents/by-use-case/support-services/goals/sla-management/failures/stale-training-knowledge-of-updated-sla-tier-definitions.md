# Stale Training Knowledge of Updated SLA-Tier Definitions

## Issue: An SLA-Management Agent Applies an SLA Response- or Resolution-Time Threshold for a Customer's Service Tier That It Recalls From Pretraining, Even Though the Tier's Definition Has Since Been Updated, Despite a Live SLA-Policy Lookup Tool Being Available That Would Surface the Current Threshold

**Frequency**: Occasional

**Symptoms**
- The agent flags a ticket as breaching, or clears it as compliant, against a response- or resolution-time threshold that does not match the tier's current, live SLA-policy definition
- Querying the agent's available SLA-policy lookup tool directly, for the same tier, surfaces a threshold that has since been tightened, loosened, or restructured (e.g., split into separate response and resolution sub-thresholds) relative to what the agent applied
- The agent's stated rationale, when asked why it applied a given threshold, cites a specific number without referencing a dated policy-document source, consistent with recalling a memorized threshold rather than confirming a current one
- The gap is most visible for tiers whose definition has been revised after the agent's training cutoff, since those are the only cases where the stale and current thresholds produce different breach determinations
- The error is caught only when an operations reviewer manually checks the applied threshold against the current SLA-policy document, since the agent's determination is presented as a confident, complete evaluation

**Root Cause**
The agent's parametric knowledge of an SLA tier's threshold reflects whatever definition was in effect up to its training cutoff, and absent an explicit instruction to verify the threshold against the SLA-policy lookup tool before finalizing a breach or compliance determination, the model defaults to the more fluent path of evaluating from a memorized number. Because the lookup tool is available but not invoked, the determination is produced with no contradiction surfaced, leaving a stale threshold driving an SLA compliance decision with direct downstream consequences for breach reporting and customer-facing commitments.

**Example**
```
SLA-management agent evaluates a Gold-tier ticket's response time against a 4-hour threshold it recalls from training
Agent flags the ticket as compliant at the 3-hour-50-minute mark without invoking the SLA-policy lookup tool it has access to
Querying that same tool, after the fact, shows the Gold tier's response-time threshold was tightened to 2 hours as part of a policy revision finalized after the agent's training cutoff
Correct determination is that the ticket already breached its current SLA at the 2-hour mark, over an hour and a half before the agent's compliant determination
Breach goes unreported and uncompensated until a customer's account manager separately escalates the discrepancy
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Information-freshness research on chatbot-delivered guidance identifies reliance on a model's training-time knowledge over a live, current source as a distinct and measurable cause of outdated responses in support and policy contexts | [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771) |
| Surveys of LLM-based agents identify failure to invoke an available tool when parametric knowledge suffices for a fluent answer as a distinct hallucination-adjacent failure mode | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on parametric or cached knowledge alone causes policy or threshold updates to go unincorporated in long-running deployments | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- No SLA-management workflow rule requires a policy lookup specifically for threshold-dependent breach or compliance determinations before the determination is finalized
- The agent's parametric knowledge of the tier's threshold is fluent and confident enough to produce a complete, well-formed determination without surfacing any uncertainty that would prompt a lookup
- The SLA-policy lookup tool is available but optional, with no enforcement distinguishing "threshold was checked and confirmed current" from "threshold was never verified"

---

## Mitigation Strategies

1. **Mandatory Policy Lookup for Threshold-Dependent Determinations**: Require any breach or compliance determination based on a tier's response- or resolution-time threshold to trigger an SLA-policy lookup before the determination is finalized, regardless of the agent's parametric confidence
2. **Date-Stamped Threshold Citation Requirement**: Require any threshold used in a breach or compliance determination to cite the specific, dated policy-document source it relies on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Compliance Determinations**: Automatically flag any finalized determination involving a tier threshold where the session log shows no policy-lookup tool call, routing it to human SLA-operations review
4. **Periodic Re-Validation of Cached Tier Thresholds**: Re-check any cached or commonly referenced tier thresholds used across SLA-management workflows against the policy lookup tool on a recurring schedule, independent of any single determination

### Metrics
- Rate of finalized breach or compliance determinations involving a tier threshold with no corresponding policy-lookup tool call in the session log
- Rate of discrepancies found when re-checking cached tier thresholds against current policy documentation
- Time between an SLA tier-definition revision and its incorporation into active compliance-determination logic

### Alerts
- A finalized compliance determination relies on a tier threshold with no policy-lookup call in the session → P1
- A policy lookup, when invoked, returns a threshold that contradicts a cached threshold still in active use → P1
- Tool-invocation audit finds threshold-dependent determinations finalized without a lookup at a rate exceeding the defined threshold → P2

---

## References

- [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
