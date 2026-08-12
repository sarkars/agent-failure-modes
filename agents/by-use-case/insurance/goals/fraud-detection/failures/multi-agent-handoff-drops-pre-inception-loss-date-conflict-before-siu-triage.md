# Multi-Agent Handoff Drops Pre-Inception Loss-Date Conflict Before SIU Triage

## Issue: An Initial-Review Agent's Free-Text Note Flagging That a Claimant's Reported Loss Date Appears to Predate the Policy's Effective Date Is Not Captured in the Structured SIU-Referral Schema, So the SIU-Triage Agent Processes the Referral Under a Generic High-Claim-Amount Category and Never Investigates the Actual Pre-Inception Loss Suspicion

**Frequency**: Rare

**Symptoms**
- A claim referred to SIU gets worked as a routine large-loss review, even though the initial-review agent's own notes named a specific reason for suspicion: the claimant's reported loss date falls before the policy's effective date
- The referral schema has fields for claim amount, claim type, and a generic reason code, but nothing for the specific fact pattern -- a date conflict -- that actually drove the initial reviewer to refer the claim in the first place
- Asked why it didn't chase the date discrepancy, the SIU-triage agent points to the only input it got: a "high claim amount" code, with no trace of the date-conflict reasoning behind it
- Referrals built on a specific factual inconsistency -- a date conflict, a mismatched incident location -- fall into this gap far more often than referrals built on a simple dollar threshold, since only the threshold has a code to match against
- Absent a human investigator independently re-reading the original claim notes, the date conflict is never revisited, and the claim proceeds to payment on the strength of a referral that never actually reflected why it was made

**Root Cause**
SIU referral-reason codes were built around the volume driver of most referrals -- claim amount crossing a threshold -- so the code set covers dollar-based risk tiers well but has nothing for a referral triggered by a specific factual inconsistency the initial-review agent noticed while reading the claimant's own account. When the initial-review agent hits a case like a pre-inception date conflict, it has to force that finding into the nearest available code (here, "high claim amount"), and that forced mapping is where the actual reason for suspicion gets lost -- not because the initial-review agent reasoned incorrectly, but because the code it's required to select was never built to carry a fact pattern instead of a dollar figure.

**Example**
```
Initial-review agent processing a claim notes: "Reported loss date is 14 days before the policy's effective date based on the claimant's own incident description -- recommend SIU referral for possible pre-inception loss"
Initial-review agent generates the SIU referral using the standard structured schema: claim amount, claim type, referral-reason code -- selects the closest available code, "high claim amount," since no code exists for "pre-inception date conflict"
SIU-triage agent receives the referral with reason code "high claim amount" and triages it as a routine large-loss review, requesting standard documentation rather than investigating the loss-date discrepancy
The actual pre-inception-loss fraud indicator is never investigated, and the claim is eventually paid
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The SIU-referral schema's referral-reason codes are built around generic risk thresholds (claim amount, claim type) with no field for a specific factual inconsistency that triggered the referral
- No check runs before SIU triage to compare the initial-review agent's free-text reasoning against the structured referral reason for an unrepresented evidentiary basis
- Specific factual-conflict suspicions (date conflicts, location mismatches) are especially likely to fall outside the generic schema, since they are qualitatively different from the threshold-based codes the schema was built around

---

## Mitigation Strategies

1. **Evidentiary-Basis Field in SIU-Referral Schema**: Add a structured free-text or categorized "specific evidentiary basis" field to the SIU-referral schema that the initial-review agent is required to populate whenever its reasoning identifies a specific factual inconsistency, separate from the generic referral-reason code
2. **Pre-Triage Reasoning Reconciliation Check**: Before SIU triage proceeds, require a check that compares the initial-review agent's free-text reasoning against the structured referral reason and flags any specific evidentiary basis not represented in the schema
3. **Mandatory Investigation of Flagged Date/Fact Conflicts**: Route any referral with a populated evidentiary-basis field describing a date or fact conflict to a dedicated investigation step targeting that specific conflict, rather than allowing generic high-claim-amount triage to subsume it
4. **Referral Traceability Log**: Maintain a log linking each SIU triage action to the initial-review agent's original reasoning notes, so a triage analyst can verify the structured referral reason actually reflects the original suspicion

### Metrics
- Rate of SIU referrals later found, on review, to have a specific evidentiary basis in the initial-review reasoning that was not represented in the structured referral reason
- Rate of referrals investigated according to their actual underlying evidentiary basis versus their generic referral-reason code
- Average time between SIU referral and detection of an unaddressed specific evidentiary flag, when gaps occur

### Alerts
- An SIU referral is triaged using only a generic referral-reason code while the initial-review reasoning contains an unrepresented specific evidentiary flag → P1
- A claim is paid following SIU triage that did not address a flagged date or fact conflict from the initial review → P1
- Rate of referrals requiring re-triage for an originally unaddressed evidentiary basis exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
