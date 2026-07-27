# What Are the Most Common Compliance Failures in AI Agents?

**Compliance failures happen when a compliance agent reasons from a stale or mismatched snapshot of the law or the contract instead of its current, jurisdiction-correct state** — an amendment that was never consolidated into the analyzed document, a regulation that was amended after the model's training cutoff, a disclosure template pulled from the wrong jurisdiction by lexical similarity, or a jurisdiction-specific exception that a review agent identified in prose but never reached the filing agent's structured checklist. Every compliance pattern documented here produces output that reads as confident and well-formed, because the error is an omission or a substitution rather than a visible malfunction — the review is internally consistent, just wrong about what currently governs the filing.

## Key Takeaways

- 4 patterns are documented here, split evenly between temporal-staleness failures (analyzing an outdated contract or regulatory text) and structural failures (wrong-jurisdiction retrieval, dropped exceptions at a multi-agent handoff).
- Contracts with amendments are common — an estimated 50-70% of long-term agreements have at least one — yet 30-50% of models analyzing amended contracts reason from the original document alone, per the amendment-tracking-failure pattern's cited estimate.
- Retrieval-based template selection is measurably unreliable across jurisdictions: document-level retrieval mismatch rates exceeding 95% have been observed on structurally standardized legal document sets, because regulatory regimes addressing the same topic across jurisdictions share dense, near-identical vocabulary.
- Regulatory update lag is structural, not incidental: an LLM agent has no inherent mechanism to know a regulation was amended after its training cutoff unless the current text is explicitly retrieved at inference time, so parametric-knowledge-only compliance review is exposed to material staleness within months of deployment.

## Scope

- **Temporal Staleness** — [Amendment Tracking Failure](failures/amendment-tracking-failure.md), [Regulatory Update Lag](failures/regulatory-update-lag.md). Both patterns come from the same root condition: the agent reasons from a fixed snapshot in time (the original contract, or a training-time understanding of a regulation) with no mechanism to detect that the snapshot has since been superseded by an amendment or a regulatory change.
- **Retrieval Mismatch** — [Embedding Retrieval Applies Wrong Jurisdiction's Disclosure Template by Name Similarity](failures/embedding-retrieval-applies-wrong-jurisdictions-disclosure-template-by-name-similarity.md). A similarity-ranked retrieval step confuses two jurisdictions' regulatory regimes because they regulate the same underlying activity using closely overlapping vocabulary.
- **Multi-Agent Handoff Loss** — [Multi-Agent Handoff Drops Jurisdiction-Specific Exception Between Compliance-Review and Filing Agent](failures/multi-agent-handoff-drops-jurisdiction-specific-exception-between-compliance-review-and-filing-agent.md). A compliance-review agent's narrative determination that an exception applies never reaches the filing agent because the structured checklist schema between the two agents has no field for it.

## When Compliance Matters

- A compliance or filing agent generates a regulatory disclosure, notice, or certification across multiple jurisdictions with closely named but substantively different regimes (breach notification, beneficial-ownership disclosure, privacy notices)
- A contract under a long-term relationship has been modified by one or more amendments that exist in separate documents from the original agreement
- A compliance-review stage and a filing/execution stage are implemented as separate agents communicating through a fixed structured schema rather than the review agent's full analysis

## Cross-Pattern Insight

All 4 compliance patterns share a single structural gap: nothing in the pipeline forces a deterministic check against the current, correctly-scoped source of truth before output is produced or filed. Amendment tracking and regulatory update lag both let the agent substitute a static snapshot for the current state; the retrieval-mismatch pattern lets similarity substitute for a jurisdiction-keyed lookup; the handoff-loss pattern lets a fixed checklist schema substitute for the review agent's actual reasoning. The fix in every documented mitigation is the same shape — replace an implicit trust in "what I already have" (a cached document, a training-time fact, a top similarity match, a boolean checklist field) with an explicit, gated verification against a dated, jurisdiction-scoped, or fully-reconciled source before the compliance determination is treated as final.

## Frequently Asked Questions

### What causes a compliance agent to apply an outdated regulatory requirement?
A training-data cutoff combined with no retrieval step against a current, authoritative regulatory text source. The compliance agent has no inherent signal that a regulation was amended after that cutoff, so it applies a stale threshold or deadline with the same confidence as a current one — see [Regulatory Update Lag](failures/regulatory-update-lag.md).

### How do you detect that a contract amendment was missed before it causes a billing or compliance dispute?
Consolidate the original contract and all discoverable amendments into a single "current state" document before analysis, tag each clause with its amendment-origin and effective date, and fail safe by flagging incomplete amendment discovery rather than proceeding silently — the mitigation detailed in [Amendment Tracking Failure](failures/amendment-tracking-failure.md).

### Can jurisdiction metadata alone prevent embedding-retrieval template mismatches?
No — metadata that exists in the template library but isn't used as a mandatory pre-filter doesn't stop similarity ranking from surfacing a wrong-jurisdiction template first. The reliable fix filters candidate templates to the filing's controlling jurisdiction before any similarity ranking runs at all, per [Embedding Retrieval Applies Wrong Jurisdiction's Disclosure Template by Name Similarity](failures/embedding-retrieval-applies-wrong-jurisdictions-disclosure-template-by-name-similarity.md).

### Does a multi-agent compliance pipeline need to expose the review agent's full reasoning to the filing agent?
Yes, whenever the review agent's determination doesn't map onto an existing structured field. A boolean or fixed-schema checklist cannot represent a jurisdiction-specific exception it was never designed to hold, so the exception exists only in narrative form and never reaches the filing agent — see [Multi-Agent Handoff Drops Jurisdiction-Specific Exception Between Compliance-Review and Filing Agent](failures/multi-agent-handoff-drops-jurisdiction-specific-exception-between-compliance-review-and-filing-agent.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Amendment Tracking Failure](failures/amendment-tracking-failure.md) | Model analyzes the original contract while separately filed amendments go unconsolidated and unread |
| [Embedding Retrieval Applies Wrong Jurisdiction's Disclosure Template by Name Similarity](failures/embedding-retrieval-applies-wrong-jurisdictions-disclosure-template-by-name-similarity.md) | Similarity ranking over regulation name/subject matter surfaces a lexically close but wrong-jurisdiction disclosure template |
| [Multi-Agent Handoff Drops Jurisdiction-Specific Exception Between Compliance-Review and Filing Agent](failures/multi-agent-handoff-drops-jurisdiction-specific-exception-between-compliance-review-and-filing-agent.md) | A checklist schema has no field for an exception the review agent identified only in narrative analysis |
| [Regulatory Update Lag](failures/regulatory-update-lag.md) | Parametric training-time knowledge of a regulation is applied without retrieving whether it has since been amended |

**Total: 4 patterns**

## Related Goals

- [Jurisdiction Handling](../jurisdiction-handling/) — the drafting-side counterpart, where the same wrong-jurisdiction retrieval and law-mismatch mechanisms apply to clause insertion rather than regulatory filings
- [Precedent Currency](../precedent-currency/) — the analogous staleness problem applied to case law citations instead of regulatory text
- [Risk Detection](../risk-detection/) — clause-level risk misses that compound with a compliance failure once a contract is executed under a wrong assumption
