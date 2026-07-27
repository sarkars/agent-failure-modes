# What Are the Most Common Refund and Billing Dispute Failures in AI Agents?

**Refund and billing-dispute resolution fails when an agent retrieves a billing-dispute template or policy article that is embedding-similar but legally or contractually distinct from the customer's actual account tier or dispute category, or when a triage agent records that a partial credit was already issued but that critical detail is dropped when the conversation is handed to a downstream billing-dispute agent.** Both failures involve incorrect financial determinations (wrong refund threshold, duplicated credits) with real money at stake, making them high-severity failures even at low frequency.

## Key Takeaways

- 2 patterns are documented, grouped into retrieval-mismatch failures (1 pattern) and multi-agent handoff failures (1 pattern).
- [Document-level retrieval mismatch pulls wrong billing-dispute template](failures/document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template.md) shows that a knowledge base containing multiple dispute articles differing by tier, region, or product can surface the wrong article via embedding similarity when the articles use overlapping dispute-category language and the retriever has no account-tier filter.
- [Multi-agent handoff drops partial-credit-already-issued flag](failures/multi-agent-handoff-drops-partial-credit-already-issued-between-triage-and-billing-agent.md) documents a specific, high-cost failure: a triage agent notes "customer already has $15 credit," but the structured billing-dispute handoff object has no field for prior credits, so the billing agent approves a full refund on top of the existing credit, creating an overpayment.

## Scope

- **Document and Template Selection** — [document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template](failures/document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template.md). The knowledge base contains near-duplicate articles for different tiers/regions; similarity-ranked retrieval surfaces the wrong one because tier metadata is not weighted in ranking.
- **Multi-Agent Handoff and State Loss** — [multi-agent-handoff-drops-partial-credit-already-issued-flag](failures/multi-agent-handoff-drops-partial-credit-already-issued-between-triage-and-billing-agent.md). A critical fact (prior credit issued) is present in triage's free-text notes but absent from the structured handoff object passed to the billing-dispute agent.

## When Refund and Billing-Dispute Matters

- Hybrid support models where triage agents handle initial intake and detect when a partial credit was already issued, and downstream billing-dispute agents execute the actual refund amount, requiring perfect context carryover
- Billing-dispute knowledge bases that contain multiple articles covering similar dispute categories but different tiers (consumer versus business), regions (US/EU/APAC with different consumer-protection laws), or products (different subscription tiers with different refund windows)
- Financial reconciliation systems that must detect overpayments (same charge disputed twice, partial credit issued twice) as they happen, not weeks later in audit

## Cross-Pattern Insight

Both patterns pivot on the same architectural gap: the downstream agent (billing-dispute resolver) operates on a structured data representation that was created upstream (by triage), and critical information present in the upstream reasoning is lost because the downstream schema has no field for it, or because retrieval-based decisions (which template to use) are made on similarity alone without account-state filtering. A refund that is calculated as $60 when $15 was already issued (creating a $15 overpayment) is not a reasoning error — it is a state-tracking failure. A billing-dispute determination made from the wrong template because embedding similarity outranked tier-applicability is not a knowledge gap — it is a retrieval-mechanism failure. Both require architectural fixes: explicit fields in handoff schemas for prior credits/partial resolutions, and metadata-filtered retrieval that pre-filters the candidate set by account tier before ranking by similarity.

## Frequently Asked Questions

### If the knowledge base has multiple billing-dispute articles for different tiers, how should retrieval be done?
[Document-level retrieval mismatch](failures/document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template.md) argues for a two-step retrieval: (1) pre-filter candidate articles by account tier/region/product metadata, narrowing to articles actually applicable to the customer's account, (2) rank the filtered set by embedding similarity. Pure similarity ranking on the full corpus will surface the wrong article whenever multiple near-duplicate articles use overlapping dispute-category language.

### If the triage agent discovers a prior credit was issued, how does that information reach the billing agent?
[Multi-agent handoff drops partial-credit-already-issued flag](failures/multi-agent-handoff-drops-partial-credit-already-issued-between-triage-and-billing-agent.md) shows the current approach loses that information at the handoff boundary. The fix requires: (1) adding a `prior_credits_issued` field to the structured dispute-case object, (2) requiring the billing agent to query the credit/refund ledger directly by charge ID (not relying on the handoff object alone), and (3) requiring refund-calculation logic to compute `disputed_amount - prior_credits_issued` before approving any refund.

### Is a ledger query sufficient to prevent duplicate credits, or does the handoff schema need to carry the prior-credit info?
Both are needed. Ledger queries catch cases where information was lost at handoff, but that is a defensive check, not the primary mitigation. The primary fix is the handoff schema explicitly carrying prior-credit information so the billing agent has immediate visibility; the ledger query is a backup sanity check.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Document-Level Retrieval Mismatch Pulls Wrong Billing-Dispute Template](failures/document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template.md) | Embedding-similarity retrieval surfaces a billing-dispute article for a different tier/region/product than the customer's, because articles use overlapping category language and tier metadata is not pre-filtered |
| [Multi-Agent Handoff Drops Partial-Credit-Already-Issued Flag Between Triage and Billing Agent](failures/multi-agent-handoff-drops-partial-credit-already-issued-between-triage-and-billing-agent.md) | Triage agent records that a customer already received $15 partial credit, but this detail is lost in the structured handoff to billing agent, leading to a full refund approval on top of the existing credit |

**Total: 2 patterns**

## Related Goals

- [Conversation Resolution](../conversation-resolution/) — the same escalation, clarification, and tone concerns as general support conversation, applied to financial-risk disputes
- [Proactive Retention Outreach](../proactive-retention-outreach/) — proactive agent reaching out to at-risk customers, versus reactive support handling billing disputes
