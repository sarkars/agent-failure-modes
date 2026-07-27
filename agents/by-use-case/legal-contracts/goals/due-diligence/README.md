# What Are the Most Common Due-Diligence Failures in AI Agents?

**Due-diligence failures happen when an agent reasoning over disclosed financial facts or contract terms constructs a causal or correlational narrative that drifts from the supporting evidence, when entity matching across heterogeneous sources (SEC filings, registry data, UCC liens) substitutes name similarity for identifier-based confirmation, or when a review-stage agent identifies a material risk only in its own annotation but that risk never propagates to the downstream summary agent because the structured handoff schema has no field to carry it.** Financial due-diligence memos narrating correlations as causal facts are the most visible manifestation — they read as expert analysis, backed by selective fact-picking, yet the causal links they assert lack transaction-level evidence. At the same time, corporate-structure errors (a coincidentally similar-named unrelated entity merged into the target's ownership chart) and multi-stage handoff failures (a change-of-control risk identified and then silently dropped between review and memo stages) are equally material yet invisible because the assembled outputs are internally self-consistent.

## Key Takeaways

- 4 patterns span three distinct failure types: narrative synthesis (correlation claimed as causation), entity matching (name similarity masquerading as verified identity), and multi-agent handoff (identified risks lost in structured-field gaps).
- Causal reasoning in LLM narrative synthesis is a documented behavioral failure distinct from factual accuracy: models systematically convert temporally adjacent or correlational relationships into confident causal claims, particularly when asked to write connected prose explaining numbers rather than to list facts or compute statistics.
- Entity matching across heterogeneous legal and financial data sources (SEC EDGAR, foreign registries, UCC databases) by name similarity achieves mismatch rates so high (>10% in documented benchmarks for high-collision contexts) that identifier-based verification (registration number, tax ID, LEI) is mandatory, not optional, for reliable corporate-structure mapping.
- Multi-agent handoff losses at the review-to-summary boundary occur precisely because review agents are empowered to note risks freely in annotation prose while summary agents are constrained to consume structured findings — a schema gap that review agents do not fill proactively because the annotation feels complete from the review agent's perspective even when the schema remains unfilled.

## Scope

- **Narrative Synthesis** — [Correlation Narrated as Causation in Financial Due-Diligence Risk Memo](failures/correlation-narrated-as-causation-in-financial-risk-memo.md). Two disclosed facts co-occurring temporally are connected by causal language ("driven by," "resulted from") without transaction-level evidence supporting the causal link.
- **Entity Matching** — [Embedding Retrieval Surfaces Similarly Named, Unrelated Subsidiary in Corporate-Structure Chart](failures/embedding-retrieval-surfaces-similarly-named-unrelated-subsidiary-in-corporate-structure-chart.md). Name similarity drives entity matching across sources, merging an unrelated company into the target's ownership chart because their names are coincidentally similar.
- **Structural Risk Omission** — [Change-of-Control Clause Omission in M&A Due Diligence](failures/change-of-control-clause-omission.md) and [Multi-Agent Handoff Drops Flagged Risk Between Review and Summary Agent](failures/multi-agent-handoff-drops-flagged-risk-between-review-and-summary-agent.md). Material risks flagged in explicit language (change-of-control triggers phrased as indirect assignment clauses, or risks identified only in annotation prose) are not captured in structured findings or not surfaced in the final memo.

## When Due-Diligence Matters

- An M&A team is building a risk memo or corporate-structure chart from heterogeneous source documents (SEC filings, foreign registries, contract databases) where entity names are shared across unrelated companies or where material contracts have been modified by amendment
- A due-diligence pipeline separates a document-review stage (which generates free-text annotations) from a memo-synthesis stage (which consumes structured findings), and reviewed documents have material risks that exist only in narrative form
- A financial risk memo is being synthesized from disclosed facts with no independent transaction-level corroboration requirement for any causal relationships asserted in the narrative

## Cross-Pattern Insight

All 4 due-diligence patterns are failures of independent verification at the point of output. The narrative-synthesis pattern generates a causal claim based on the fluency of the prose connecting two facts, not based on evidence — no separate verification step requires tracing the causal claim back to a specific transaction-level data point. The entity-matching pattern substitutes name similarity for identifier lookup — no separate verification step requires confirming the matched entity's registration number or tax ID against the target. The risk-omission patterns let risks exist only in narrative form or annotation prose without requiring explicit mapping into a structured field that downstream agents actually read. The mitigation shape recurs across all four patterns: add an independent, mandatory verification layer that doesn't trust the generation step's own confidence or completeness — trace every causal claim to transaction-level evidence, verify every entity match by identifier, enforce structured risk fields and reconcile annotation against structure before handoff.

## Frequently Asked Questions

### How do you distinguish a correlational relationship from a causal one in disclosed financial facts?
Require every causal claim (driven by, caused by, resulted from) to cite a specific transaction-level or documentary source establishing that link, not just temporal proximity. A separate fact-listing pass followed by a causal-claim verification pass can flag any causal connection introduced in synthesis prose that lacks underlying evidence — see [Correlation Narrated as Causation in Financial Due-Diligence Risk Memo](failures/correlation-narrated-as-causation-in-financial-risk-memo.md).

### Can identifier-based entity matching eliminate false positives from name-similarity matching?
Yes — enforce a mandatory pre-filter: all entity matches must first attempt lookup via registration number, tax ID, or LEI against authoritative registries. Only if no identifier match is found should similarity-based matching be used as a fallback, always with explicit confidence flags and mandatory human verification before chart inclusion — see [Embedding Retrieval Surfaces Similarly Named, Unrelated Subsidiary in Corporate-Structure Chart](failures/embedding-retrieval-surfaces-similarly-named-unrelated-subsidiary-in-corporate-structure-chart.md).

### How do you prevent a change-of-control risk from going undetected during a due-diligence review?
Scan for both explicit change-of-control language ("change of control," "change in ownership") and functionally equivalent implicit triggers (assignment-clause language like "any transfer of ownership without consent"). Build a consolidated change-of-control risk register mapping each identified trigger to its consent deadlines and termination risks, crossed against the deal closing timeline — see [Change-of-Control Clause Omission in M&A Due Diligence](failures/change-of-control-clause-omission.md).

### What prevents a material risk identified during document review from disappearing between review and memo stages?
Require the review agent to populate mandatory structured risk-flag fields with material risks it identifies. Before the memo is published, run a reconciliation: check whether every risk flag from the review stage appears somewhere in the memo. Any flagged risk not mentioned in the memo must be explicitly acknowledged by the deal team before memo release — see [Multi-Agent Handoff Drops Flagged Risk Between Review and Summary Agent](failures/multi-agent-handoff-drops-flagged-risk-between-review-and-summary-agent.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Change-of-Control Clause Omission in M&A Due Diligence](failures/change-of-control-clause-omission.md) | Change-of-control triggers phrased indirectly (as assignment clauses) are not recognized as functionally equivalent to explicit change-of-control language |
| [Correlation Narrated as Causation in Financial Due-Diligence Risk Memo](failures/correlation-narrated-as-causation-in-financial-risk-memo.md) | Temporal adjacency between two disclosed facts drives causal narrative language without transaction-level evidence supporting the causal link |
| [Embedding Retrieval Surfaces Similarly Named, Unrelated Subsidiary in Corporate-Structure Chart](failures/embedding-retrieval-surfaces-similarly-named-unrelated-subsidiary-in-corporate-structure-chart.md) | Name similarity across heterogeneous sources (SEC filings, foreign registries) merges an unrelated entity into the target's structure chart |
| [Multi-Agent Handoff Drops Flagged Risk Between Review and Summary Agent](failures/multi-agent-handoff-drops-flagged-risk-between-review-and-summary-agent.md) | Material risk identified in review-stage annotation prose never reaches structured findings list that memo-synthesis agent consumes |

**Total: 4 patterns**

## Related Goals

- [Risk Detection](../risk-detection/) — similar failures at the clause-review level (missing indemnification caps, liability exposure) that compound with due-diligence omissions once a contract is executed
- [Compliance](../compliance/) — the parallel multi-agent handoff failure where exceptions identified by a compliance-review agent never reach a filing agent's structured checklist
- [Contract Drafting](../contract-drafting/) — where similar multi-agent handoff failures occur between redline-negotiation and assembly stages
