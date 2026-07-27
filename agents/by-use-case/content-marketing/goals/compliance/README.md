# What Are the Most Common Compliance Failures in AI Agents?

**Compliance fails when marketing copy contains an unsubstantiated comparative claim, a missing legally-required disclaimer, a region-specific condition required by regulation, or a disclosure requirement determined by an outdated rule — not because the agent lacks capability to enforce them, but because compliance checks are structured to catch pattern-matched violations (prohibited words, missing required phrases) and miss substantive determinations (does a substantiation source actually exist, does it support this specific claim, has it expired).** Compliance failures concentrate on the determinations a rule-based checker cannot make alone: whether a claim is actually substantiated, whether a condition is actually satisfied, whether a source's scope actually matches the claim being made.

## Key Takeaways

- 4 patterns are documented, all involving substantiation, disclosure, or region-specific requirements that require cross-referencing against external data or live tools, not just pattern-matching text.
- [Missing substantiation for comparative claims](failures/missing-substantiation-for-comparative-claims.md) shows that LLM-generated content can produce plausible-sounding comparative figures without any actual grounding in data, and a compliance review that scans for prohibited terms misses fabricated claims unless a dedicated substantiation-verification step is added.
- [Multi-agent handoff drops region-specific disclaimer requirement](failures/multi-agent-handoff-drops-region-specific-disclaimer-requirement-before-publishing.md) documents a structural handoff gap: the legal-review agent approves conditionally ("only if EU disclaimer is included") but the binary handoff schema has no field for conditions, so a real regulatory requirement is dropped silently.
- [Stale training-corpus disclosure-placement rule overrides updated regulatory guidance](failures/stale-training-corpus-disclosure-placement-rule-overrides-updated-regulatory-guidance.md) and [embedding-retrieval matches legally distinct substantiation source](failures/embedding-retrieval-matches-legally-distinct-substantiation-source.md) together show that compliance determinations require live, current tool calls — a model's parametric memory of an old regulation is not equivalent to querying the current source.

## Scope

- **Substantiation and Source Matching** — [missing-substantiation-for-comparative-claims](failures/missing-substantiation-for-comparative-claims.md), [embedding-retrieval-matches-legally-distinct-substantiation-source](failures/embedding-retrieval-matches-legally-distinct-substantiation-source.md). Both require verification that a source exists and that it actually supports the specific claim as written, distinctions a similarity-ranked retrieval or general LLM fluency cannot make alone.
- **Disclosure and Regulatory Requirements** — [multi-agent-handoff-drops-region-specific-disclaimer-requirement-before-publishing](failures/multi-agent-handoff-drops-region-specific-disclaimer-requirement-before-publishing.md), [stale-training-corpus-disclosure-placement-rule-overrides-updated-regulatory-guidance](failures/stale-training-corpus-disclosure-placement-rule-overrides-updated-regulatory-guidance.md). Both involve requirements that exist in an external source (regulatory guidance, a region-specific law) and must be checked against that source via a tool call, not derived from a model's static knowledge.

## When Compliance Matters

- Regulated industries (health, financial services, insurance, advertising-regulated categories) where substantiation standards and disclosure requirements are enforced by regulators and carry material penalties for non-compliance
- Multi-agent workflows where a legal-review or compliance agent produces free-text notes containing a condition or caveat, but that condition is not represented in the structured handoff schema passed to a publishing agent
- Content generation pipelines that use retrieval-augmented generation (RAG) to ground claims in substantiation sources, where a similarity-ranked retriever can surface a scope-mismatched source confidently

## Cross-Pattern Insight

All four compliance failures pivot on the same gap: compliance is treated as a text-pattern check (prohibited terms, required phrases) when it is actually a cross-reference problem (does this claim match a real substantiation, does a required disclaimer's scope match the content's actual distribution region, does a disclosure rule apply to this content type). Pattern-matching catches straightforward violations; cross-reference checking catches the more dangerous ones where the compliance risk is hidden in semantic details (a correct-sounding substantiation that actually covers a different population, a legally-correct-sounding disclosure that was written for a rule that changed, a comparative claim that is fluent but fabricated). The mitigation that recurs across all four patterns is explicit verification: substantiation sources must be cross-checked for scope-match, regulatory-guidance must be queried live before approving a disclosure approach, and handoff schemas must carry conditional requirements (not just binary approve/reject), with human review gating on condition mismatches.

## Frequently Asked Questions

### Is a substantiation-verification step always required for comparative claims?
Yes. [Missing substantiation for comparative claims](failures/missing-substantiation-for-comparative-claims.md) documents that LLM-generated content produces plausible-sounding comparative figures without any real backing, and general compliance review that scans for prohibited terms misses fabricated claims. Regulated industries apply a substantiation standard: the advertiser bears the burden of proof for "established" claims at the time of publication, not only if challenged. A dedicated substantiation-verification gate is required to discharge that burden.

### Can embedding-based source retrieval be fixed, or does it require moving to a different retrieval approach?
Embedding-based retrieval can be improved but requires architectural changes. [Embedding retrieval matches legally distinct substantiation source](failures/embedding-retrieval-matches-legally-distinct-substantiation-source.md) shows the failure is retrieval selecting a topically similar but scope-mismatched document. The fix is multi-layered: pre-filter the candidate set by scope metadata (population, time period, product variant) before similarity ranking, surface the retrieved source's limitations section explicitly, and require a deterministic scope-match step (not just similarity) before approving the source as adequate substantiation.

### If a regulator updates disclosure guidance mid-campaign, does every in-flight piece need re-verification?
Yes. [Stale training-corpus disclosure-placement rule overrides updated regulatory guidance](failures/stale-training-corpus-disclosure-placement-rule-overrides-updated-regulatory-guidance.md) argues for a triggered re-verification sweep when regulatory guidance changes: flag all in-flight and recently approved content in the affected category for mandatory re-verification before publication, rather than waiting for the next scheduled compliance review cycle. The cost of a missed update is regulatory action; the cost of re-verifying a few extra pieces is trivial.

### What should happen when a compliance approval has a condition (e.g., "approved if disclaimer X is included") but the publishing agent never sees that condition?
[Multi-agent handoff drops region-specific disclaimer requirement before publishing](failures/multi-agent-handoff-drops-region-specific-disclaimer-requirement-before-publishing.md) documents this exact failure. The fix requires extending the handoff schema to carry conditional requirements explicitly, not just a binary approve/reject status. A human compliance lead should review any handoff with a populated "condition" field before the publishing agent proceeds; conditional approvals should not be auto-resolved by downstream agents.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Missing Substantiation for Comparative Claims](failures/missing-substantiation-for-comparative-claims.md) | Comparative claim is approved without verifying an adequate substantiation source exists and actually supports the claim as stated |
| [Embedding Retrieval Matches Legally Distinct Substantiation Source](failures/embedding-retrieval-matches-legally-distinct-substantiation-source.md) | Source is topically similar but covers different population/product/region; retrieved source's scope is narrower than the claim, but similarity matching treats them as equivalent |
| [Multi-Agent Handoff Drops Region-Specific Disclaimer Requirement Before Publishing](failures/multi-agent-handoff-drops-region-specific-disclaimer-requirement-before-publishing.md) | Legal review approves conditionally ("only with EU disclaimer") but the handoff schema has no field for conditions, so requirement is dropped at the boundary |
| [Stale Training-Corpus Disclosure-Placement Rule Overrides Updated Regulatory Guidance](failures/stale-training-corpus-disclosure-placement-rule-overrides-updated-regulatory-guidance.md) | Agent answers disclosure-placement questions from parametric knowledge rather than calling a live regulatory-guidance tool, applying rules the guidance has since updated |

**Total: 4 patterns**

## Related Goals

- [Brand Consistency](../brand-consistency/) — consistency supports compliance, but is distinct from regulatory requirements
- [Quality Control](../quality-control/) — factual accuracy and compliance are both quality concerns but operate at different levels (QC checks internal consistency, compliance checks against external regulations)
