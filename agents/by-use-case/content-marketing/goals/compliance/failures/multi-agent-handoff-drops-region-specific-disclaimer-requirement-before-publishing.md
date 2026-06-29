# Multi-Agent Handoff Drops Region-Specific Disclaimer Requirement Before Publishing

## Issue: A Legal-Review Agent's Free-Text Note Flagging That a Specific Claim Requires a Region-Specific Disclaimer for One Market Is Not Captured in the Structured Approve/Reject Handoff Schema Passed to the Publishing Agent, Which Publishes the Claim Globally Without the Required Disclaimer

**Frequency**: Occasional

**Symptoms**
- Content containing a comparative performance claim is published in a region where local regulation requires an accompanying substantiation disclaimer, even though a legal-review agent's notes show the claim was approved specifically "with the EU disclaimer required," not approved outright
- The legal-review agent's structured handoff to the publishing agent contains only an "approved" or "rejected" status field, with no field for a conditional requirement attached to the approval
- Asking the publishing agent why the disclaimer was omitted shows it received only the binary approve/reject status and had no input describing the region-specific condition attached to that approval
- The miss concentrates on claims approved conditionally rather than outright, since the binary handoff schema has no representation for "approved, but only if X accompanies it"
- The regulator, a regional compliance reviewer, or a customer complaint catches the missing disclaimer only after the content has already been published in the affected region

**Root Cause**
The handoff between the legal-review agent and the publishing agent passes only a binary structured status (approved/rejected), with no mechanism for attaching a conditional requirement to an approval. The legal-review agent's free-text reasoning notes the region-specific disclaimer condition, but nothing in the handoff forces a check for "does this approval carry a condition not represented in the binary status field" before the publishing agent treats the content as cleared, so a real regulatory requirement is silently dropped at the agent-to-agent boundary.

**Example**
```
Legal-review agent evaluates a comparative performance claim and notes in its reasoning: "Approved, but requires the standard EU substantiation disclaimer to accompany this claim in EU markets"
Legal-review agent's structured handoff to the publishing agent sets status: "approved" -- no field exists for "conditional on accompanying disclaimer"
Publishing agent treats the approved status as a clean go-ahead and publishes the claim across all regions, including the EU, with no disclaimer attached
EU regulatory requirement for a substantiation disclaimer on this category of claim is not met
Compliance team discovers the gap during a routine regional content audit, after the content has been live for several weeks
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The legal-review-to-publishing handoff schema uses a binary approve/reject status field with no field for conditional requirements attached to an approval
- No check runs before publishing to compare the legal-review agent's free-text reasoning against the structured approval status for unrepresented conditions
- Region-specific conditional requirements are especially likely to fall outside the binary schema, since by definition they qualify rather than simply grant or deny approval

---

## Mitigation Strategies

1. **Conditional-Requirement Field in Handoff Schema**: Add a structured "conditions on approval" field to the legal-review-to-publishing handoff schema that the legal-review agent is required to populate whenever its reasoning attaches a condition to an approval
2. **Pre-Publish Reasoning Reconciliation Check**: Before publishing, require a check that compares the legal-review agent's free-text reasoning against the structured approval status and flags any condition not represented in the schema
3. **Human Review Gate for Conditional Approvals**: Route any content with a populated conditions field to human compliance review before publishing, rather than allowing the publishing agent to resolve the condition automatically
4. **Region-Aware Publishing Gate**: Require the publishing agent to confirm, per target region, that any region-specific condition attached to the approval has been satisfied before that region's version goes live

### Metrics
- Rate of published content later found, on regional compliance audit, to omit a disclaimer or condition present in the legal-review agent's reasoning notes
- Rate of approvals with a populated "conditions on approval" field versus approvals where a downstream audit found a condition that should have been populated but wasn't
- Average time between publishing and conditional-requirement-gap detection, when gaps occur

### Alerts
- Content is published with a condition present in the legal-review reasoning but absent from the structured approval status → P1
- A regional compliance reviewer or regulator flags a missing region-specific disclaimer on published content → P1
- Rate of content requiring post-publish correction for missed conditional requirements exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
