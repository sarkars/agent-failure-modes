# Multi-Agent Handoff Drops Mid-Term Endorsement Before Renewal-Pricing Agent Runs

## Issue: A Policy-Servicing Agent's Free-Text Confirmation of a Processed Mid-Term Endorsement (a Risk-Increasing Property Addition, a Removed Discount Condition) Is Not Captured in the Structured Risk-Profile Schema Passed to the Renewal-Pricing Agent, Which Prices the Renewal off the Stale, Pre-Endorsement Risk Profile

**Frequency**: Occasional

**Symptoms**
- The renewal prices off the insured value as it stood before a policyholder added a $45,000 detached workshop mid-term, even though the servicing agent's own confirmation notes record the endorsement, the dollar increase, and the effective date
- Base coverage limit, prior-term premium, and claims history -- the inputs the risk-profile schema was designed around -- flow into the renewal-pricing agent correctly every time; a mid-term insured-value bump fails specifically because that schema was built to refresh at renewal, not to absorb events that happen between renewals
- The renewal-pricing agent computes a mathematically consistent premium from what it received -- it isn't miscalculating, it's calculating against a risk profile that stopped being current the day the workshop was added
- The gap is invisible at renewal time because nothing looks wrong: the policy simply renews, at a premium that happens to be lower than the risk it now covers actually warrants
- The mismatch only becomes visible when a claim touches the endorsed risk directly -- at which point the underpriced exposure has already been carried for a full renewal term

**Root Cause**
The policy-servicing agent's endorsement confirmation is written as a narrative update to the policy file -- what changed, by how much, effective when -- while the renewal-pricing agent consumes a risk-profile schema designed around the standard renewal-cycle refresh, not around mid-cycle events. Because the pricing schema has no field representing "risk profile as of an interim endorsement date," the renewal-pricing agent has no way to distinguish a policy that was endorsed mid-term from one that wasn't; both look identical from inside the schema it's actually reading.

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
