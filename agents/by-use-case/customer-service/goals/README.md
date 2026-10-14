# Customer Service AI Agent Failures by Goal: 15 Patterns, Causes, and Fixes

**Customer Service AI agents fail in 3 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 15 documented patterns across 3 goals; the most documented is [Conversation Resolution](conversation-resolution/) with 12.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Customer Service Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Conversation Resolution](conversation-resolution/) | When a support agent selects a canned response matching the customer's topic but wrong for their account state, asks repeated questions the customer already answered | 12 |
| [Proactive Retention Outreach](proactive-retention-outreach/) | When a retention agent reaches out to an at-risk customer with a fabricated usage-decline narrative to justify the outreach, because a tool call to fetch actual usage data returned empty or errored. | 1 |
| [Refund and Billing Disputes](refund-and-billing-disputes/) | When an agent retrieves a billing-dispute template or policy article that is embedding-similar but legally or contractually distinct from the customer's actual account tier or dispute category | 2 |

**Total: 15 patterns**

## Frequently Asked Questions

### How do you select the correct canned response when multiple responses are topically similar?

[Embedding retrieval selects similar-but-wrong canned response](conversation-resolution/failures/embedding-retrieval-selects-similar-but-wrong-canned-response.md) shows pure text-similarity ranking can fail when the canned-response library contains responses for similar-but-distinct scenarios. See [Conversation Resolution](conversation-resolution/).

### If the knowledge base has multiple billing-dispute articles for different tiers, how should retrieval be done?

[Document-level retrieval mismatch](refund-and-billing-disputes/failures/document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template.md) argues for a two-step retrieval: (1) pre-filter candidate articles by account tier/region/product metadata, narrowing to articles actually applicable to the customer's account, (2) rank the filtered set by embedding similarity. See [Refund and Billing Disputes](refund-and-billing-disputes/).

### Should outreach use generic non-personalized save messages if usage data is unavailable?

[Fabricated usage-decline justification](proactive-retention-outreach/failures/fabricated-usage-decline-justification-when-analytics-tool-returns-empty.md) argues for exactly that: a non-usage-specific check-in template when the analytics tool fails, rather than fabricating a usage narrative. See [Proactive Retention Outreach](proactive-retention-outreach/).

## Related

- [Customer Service overview](../)
- [All agent failure patterns](../../../)
