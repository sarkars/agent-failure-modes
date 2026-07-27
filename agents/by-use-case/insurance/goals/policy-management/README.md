# What Are the Most Common Policy Management Failures in AI Agents?

**Policy-management agents fail when a renewal-pricing RAG step retrieves a similar-looking but territory-mismatched policy precedent, when a multi-agent handoff loses a mid-term endorsement that changed the risk profile, and when the agent answers a jurisdiction-specific cancellation notice requirement from memorized knowledge instead of calling the live regulatory tool.** The three failure mechanisms are indistinguishable from those in claim processing and fraud detection: retrieval without structural filtering, handoff without schema fields to carry task-relevant context, and parametric memory defeating tool-grounding. The result in every case is a policy priced incorrectly at renewal, a risk profile left unchanged after an endorsement, or a cancellation notice that violates a state's current legal requirement — failures that often go undetected until a loss-ratio review identifies the underpriced policy, a claim reveals an endorsed risk never reflected in the renewal, or a regulatory compliance review surfaces non-compliant notice wording.

## Key Takeaways

- 3 patterns are documented for policy management, one per failure mechanism: embedding-retrieval territory mismatch, multi-agent handoff loss, and stale-training-corpus override.
- The embedding-retrieval pattern shows a renewal priced using a precedent from a different rating territory with materially different loss experience, an error caught only during a loss-ratio audit months after the renewal issued.
- The multi-agent-handoff pattern documents a mid-term endorsement correctly noted by the policy-servicing agent, but never represented in the structured fields the renewal-pricing agent reads, resulting in an underpriced renewal reflecting the pre-endorsement risk.
- The stale-training-corpus pattern shows an agent issuing a non-renewal notice with a 30-day advance period, meeting the memorized generic standard but violating a state's actual current 60-day requirement for wildfire-risk-area properties, triggering a regulatory compliance finding.

## Scope

- **Retrieval mismatch** — [Embedding Retrieval Pulls Mismatched Rating-Territory Policy Precedent for Renewal](failures/embedding-retrieval-pulls-mismatched-rating-territory-policy-precedent-for-renewal.md). Renewal-pricing retrieval ranks precedent policies by embedding similarity without filtering by rating territory first, defaulting to the dominant territory in the corpus regardless of the actual policy's territory.
- **Handoff information loss** — [Multi-Agent Handoff Drops Mid-Term Endorsement Before Renewal-Pricing Agent Runs](failures/multi-agent-handoff-drops-mid-term-endorsement-before-renewal-pricing.md). A policy-servicing agent processes a mid-term endorsement and records it in free text, but the structured risk-profile schema passed to the renewal-pricing agent has no field for mid-term changes.
- **Stale parametric override** — [Stale Training-Corpus Cancellation-Notice Rule Overrides Live State-Lookup Tool](failures/stale-training-corpus-cancellation-notice-rule-overrides-live-state-lookup-tool.md). An agent generates a cancellation or non-renewal notice citing a memorized generic notice period instead of querying the live regulatory-requirements tool for the state's current requirement.

## When Policy Management Matters

- A renewal-pricing system applies rate adjustments based on precedent policies and the corpus contains policies across many rating territories
- A policy's servicing history includes mid-term endorsements that change the risk profile, processed outside the standard renewal-cycle refresh
- A policy-servicing workflow generates cancellation or non-renewal notices that must comply with jurisdiction-specific, independently amendable statutory requirements

## Cross-Pattern Insight

The same three structural failures that recur in claim processing and fraud detection reappear in policy management with identical mechanisms and identical fixes: pre-filter retrieval by structural attributes before similarity ranking, extend handoff schemas to carry task-relevant context the upstream stage identified, and force live-tool calls for any jurisdiction-specific or actively maintained regulatory data rather than defaulting to parametric memory. The business impact differs — a misprice at renewal affects loss ratios and margin rather than individual claim payments — but the failure pattern is indistinguishable from the other two insurance use cases.

## Frequently Asked Questions

### How does a renewal-pricing precedent lookup retrieve the wrong rating territory?
Renewal-pricing retrieval matches the query policy against a corpus of prior renewals by embedding similarity over shared attributes (construction type, coverage limits, property age), which look similar across all territories. Without a pre-filter on rating territory, the similarity-ranked result defaults to the most common territory in the corpus rather than the policy's actual territory. See [Embedding Retrieval Pulls Mismatched Rating-Territory Policy Precedent for Renewal](failures/embedding-retrieval-pulls-mismatched-rating-territory-policy-precedent-for-renewal.md).

### Can a mid-term endorsement be lost if the policy-servicing agent recorded it in free text?
Yes. If the structured schema the renewal-pricing agent reads has no field for mid-term endorsements, the finding remains invisible even though it was correctly noted earlier in the pipeline. The fix is adding a structured "mid-term risk change" field and reconciliation against upstream free text. See [Multi-Agent Handoff Drops Mid-Term Endorsement Before Renewal-Pricing Agent Runs](failures/multi-agent-handoff-drops-mid-term-endorsement-before-renewal-pricing.md).

### Should a policy-servicing agent know state cancellation notice requirements without looking them up?
No. State notice-period requirements are independently and frequently amended (especially post-catastrophe), and the agent's memorized sense of "typical" rules will not reflect a recent amendment. The fix is a forced regulatory-tool-call gate before any notice is generated. See [Stale Training-Corpus Cancellation-Notice Rule Overrides Live State-Lookup Tool](failures/stale-training-corpus-cancellation-notice-rule-overrides-live-state-lookup-tool.md).

### How do you catch a renewal mispriced due to the wrong territory precedent?
Audit renewal-pricing calculations specifically for less common rating territories (the population most likely to be overridden by the dominant territory's precedent), and compare the precedent's territory against the policy's actual territory for every priced renewal.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding Retrieval Pulls Mismatched Rating-Territory Policy Precedent for Renewal](failures/embedding-retrieval-pulls-mismatched-rating-territory-policy-precedent-for-renewal.md) | Renewal precedent retrieved by textual similarity across territories without filtering to territory match |
| [Multi-Agent Handoff Drops Mid-Term Endorsement Before Renewal-Pricing Agent Runs](failures/multi-agent-handoff-drops-mid-term-endorsement-before-renewal-pricing.md) | Policy-servicing agent notes mid-term endorsement in free text; renewal-pricing schema has no field for mid-term changes |
| [Stale Training-Corpus Cancellation-Notice Rule Overrides Live State-Lookup Tool](failures/stale-training-corpus-cancellation-notice-rule-overrides-live-state-lookup-tool.md) | Agent cites memorized notice period instead of calling live regulatory-requirements tool for state's current rule |

**Total: 3 patterns**

## Related Goals

- [Claim Processing](../claim-processing/) — the same three mechanism clusters (retrieval, handoff, stale-corpus) recur in claims adjudication
- [Fraud Detection](../fraud-detection/) — the same three mechanism clusters recur in SIU referral and fraud-screening workflows
- [Underwriting](../underwriting/) — distinct goal; underwriting focuses on risk classification and hazard identification at binding time rather than renewal or mid-term changes
