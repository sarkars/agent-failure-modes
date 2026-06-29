# Multi-Agent Handoff Drops Mid-Term Endorsement Before Renewal-Pricing Agent Runs

## Issue: A Policy-Servicing Agent's Free-Text Confirmation of a Processed Mid-Term Endorsement (a Risk-Increasing Property Addition, a Removed Discount Condition) Is Not Captured in the Structured Risk-Profile Schema Passed to the Renewal-Pricing Agent, Which Prices the Renewal off the Stale, Pre-Endorsement Risk Profile

**Frequency**: Occasional

**Symptoms**
- A policy renews at a premium that does not reflect a mid-term endorsement processed earlier in the term, even though the policy-servicing agent's confirmation notes explicitly record the endorsement (e.g., a newly added detached structure increasing insured value, or a removed safety-discount condition) as processed and effective mid-term
- The structured risk-profile schema passed to the renewal-pricing agent includes fields for base coverage limit, prior-term premium, and claims history, but has no field for a mid-term endorsement that changed the risk profile after the original policy was bound
- Asking the renewal-pricing agent why the endorsement was not reflected shows it received only the structured risk-profile fields and had no input describing the mid-term change from the policy-servicing agent's confirmation notes
- The miss concentrates on endorsements processed outside the standard renewal-cycle risk-profile refresh, since those are exactly the changes least likely to have a corresponding field in the pricing schema
- The pricing gap is typically discovered only when a claim involving the endorsed risk occurs and a coverage-and-pricing review finds the renewal premium never reflected the endorsement

**Root Cause**
The handoff between the policy-servicing agent, which processes mid-term endorsements and confirms them in free-text notes, and the renewal-pricing agent, which prices the renewal from a fixed structured risk-profile schema, has no mechanism for surfacing an endorsement that does not map to one of the schema's predefined fields. The policy-servicing agent's notes confirm the endorsement was processed, but nothing in the handoff forces a check for "does this policy's mid-term servicing history contain a risk-profile change not represented in the structured renewal-pricing inputs" before the renewal-pricing agent proceeds, so a real, premium-affecting change is silently dropped at the agent-to-agent boundary.

**Example**
```
Policyholder adds a detached workshop structure to their property mid-term; policy-servicing agent processes the endorsement, increases the insured value accordingly, and confirms in free-text notes: "Endorsement processed -- detached workshop added, insured value increased $45,000 effective March 15"
Policy-servicing agent hands off renewal-pricing inputs to the renewal-pricing agent using the standard structured schema: base coverage limit, prior-term premium, claims history -- no field exists for "mid-term insured-value change from endorsement"
Renewal-pricing agent prices the renewal using the original, pre-endorsement insured value, since the endorsement was never represented in the structured fields it received
Policy renews underpriced relative to its actual current risk exposure, discovered only when a claim involving the detached workshop arises and a coverage review finds the renewal premium never reflected the added structure
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning or confirmation process is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Agentic AI applications in insurance decision-making are documented to be sensitive to gaps in structured data transfer between policy-servicing and pricing workflows, where free-text confirmations of mid-term changes are not reliably propagated into pricing inputs | [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110) |

**Contributing Factors**
- The renewal-pricing risk-profile schema has no field for a mid-term endorsement that changed the risk profile after the original policy was bound
- No check runs before renewal pricing to compare the policy's mid-term servicing history against the structured pricing inputs for an unrepresented endorsement
- Endorsements processed outside the standard renewal-cycle refresh are especially likely to fall outside the schema, since the schema was built around the standard renewal-cycle data refresh rather than mid-term events

---

## Mitigation Strategies

1. **Mid-Term Risk-Change Field in Pricing Schema**: Add a structured "mid-term risk-profile change" field to the policy-servicing-to-renewal-pricing handoff schema that the policy-servicing agent is required to populate whenever it processes an endorsement that changes the insured risk profile
2. **Pre-Pricing Endorsement Reconciliation Check**: Before pricing the renewal, require a check that compares the policy's mid-term servicing history against the structured pricing inputs and flags any endorsement not represented in the schema
3. **Human Underwriter Review Gate for Flagged Mid-Term Changes**: Route any renewal with a populated mid-term risk-change field to human underwriter review before the renewal premium is finalized, rather than allowing the renewal-pricing agent to resolve it automatically
4. **Servicing-to-Pricing Traceability Log**: Maintain a log linking each renewal-pricing calculation to the mid-term servicing history it was derived from, so a missing endorsement can be caught by audit before the renewal is issued

### Metrics
- Rate of renewal-pricing calculations later found, on review, to omit a mid-term endorsement present in the policy's servicing history
- Rate of pricing handoffs with a populated "mid-term risk-profile change" field versus handoffs where a downstream audit found an endorsement that should have been populated but wasn't
- Average time between renewal issuance and endorsement-gap detection, when gaps occur

### Alerts
- A renewal is priced and issued with a mid-term endorsement present in the servicing history but absent from the structured pricing inputs → P1
- A claim involves a risk that was added via a mid-term endorsement never reflected in the policy's renewal pricing → P1
- Rate of renewals requiring post-issuance correction for missed mid-term endorsements exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110)
