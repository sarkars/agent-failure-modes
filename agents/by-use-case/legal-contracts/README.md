# What Are the Most Common Legal-Contracts Failures in AI Agents?

**Legal-contracts agents fail when they reason from stale information (outdated amendments, changed regulations), when they substitute similarity matching for jurisdiction-specific or legal-effect matching (wrong template retrieved, wrong jurisdiction's rule applied), when they fail to verify that downstream agents actually received and acted on critical information (exceptions lost between agents, overruled citations cited as good law, negotiated values never reach the final draft), and when they stop short of cross-validating across related clauses and obligations (caps without evaluating carve-outs, presence-checking without scope evaluation, multi-party obligations tracked ambiguously).** Legal-contracts failures are particularly consequential because the output of contract work is the contract document itself, which becomes binding and enforceable. Errors in agent analysis do not surface as obviously as model hallucinations — the contract reads as well-drafted and internally consistent, the risk assessment looks thorough, the compliance determination appears authoritative — until a dispute arises, a counterparty redlines, or a post-closing issue forces a re-read of what the agent missed or misunderstood.

## Key Takeaways

- 8 goals and 32 total patterns are documented here, spanning contract assembly (drafting, compliance), contract review (due diligence, risk detection), contract use (IP-rights, jurisdiction handling), and litigation support (discovery, depositions, privilege).
- The largest single failure cluster is temporal staleness and legal currency (amendments, regulatory updates, superseded case law, stale templates, outdated disclosures) — 9 patterns across 4 goals document the same root condition: an agent reasoning from a fixed snapshot in time without a mechanism to detect that the snapshot has been superseded.
- Multi-agent handoff failures are the second-largest cluster: 8 patterns across 5 goals document how a determination or limitation identified by an upstream agent (jurisdiction-specific exception, negotiated value, field-of-use restriction, risk flag, overruled citation status) never reaches a downstream agent because the structured interchange schema has no field to carry it.
- Retrieval-substitution failures (wrong-jurisdiction template, wrong-effect template, wrong-version clause, wrong-subsidiary entity, stale regulatory template) recur across 6 goals — the recurring root condition is similarity-based ranking applied without jurisdiction, legal-effect, or canonicality filtering as a mandatory pre-filter.

## Legal-Contracts Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Compliance](goals/compliance/) | Amendment tracking, regulatory update lag, wrong-jurisdiction disclosure templates, jurisdiction-specific exceptions | 4 |
| [Contract Drafting](goals/contract-drafting/) | Boilerplate-negotiation conflicts, wrong-version clause retrieval, negotiated value loss at redline-assembly handoff, export verification | 4 |
| [Due Diligence](goals/due-diligence/) | Change-of-control omission, correlation-as-causation in risk memos, unrelated-entity matching, risk-flag loss at review-summary handoff | 4 |
| [IP-Rights](goals/ip-rights/) | Mechanism-category-jurisdiction mismatch in assignment clauses, OSS-license vs. assignment confusion, field-of-use scope loss at handoff, unverified clearance citations | 4 |
| [Jurisdiction Handling](goals/jurisdiction-handling/) | Governing-law misapplication, wrong-jurisdiction clause retrieval, cross-border data-transfer mechanism gaps | 3 |
| [Litigation Support](goals/litigation-support/) | Discovery vocabulary mismatch, positional bias in deposition summaries, privilege misidentification | 3 |
| [Precedent Currency](goals/precedent-currency/) | Superseded case-law citations, circuit-split blindness, overruled-status loss at research-drafting handoff | 3 |
| [Risk Detection](goals/risk-detection/) | Ambiguity misses, indemnification cap blindness, liability exposure blindness, multi-party obligation confusion, termination-clause misinterpretation | 5 |

**Total: 32 patterns**

## How the Goals Relate

Legal-contracts goals span the full contract lifecycle and operate at two distinct layers. At the assembly and analysis layer, contracts are written, reviewed, and analyzed for compliance and risk: Drafting creates contracts from templates and negotiated terms; Compliance verifies filings against regulatory requirements; Due Diligence assesses target companies and risk; Risk Detection identifies obligations and exposure in existing contracts. At the usage layer, assembled or analyzed contracts are put into effect: IP-Rights and Jurisdiction Handling verify that contract terms are enforced as written; Litigation Support handles evidentiary and procedural aspects when disputes arise; Precedent Currency ensures legal reasoning stands on current authority. 

To troubleshoot an error by symptom: if a contract contains wrong terms or conflicting boilerplate → [Contract Drafting](goals/contract-drafting/); if regulatory filing is non-compliant or uses wrong jurisdiction's template → [Compliance](goals/compliance/); if deal risk is understated or material risks are missed → [Risk Detection](goals/risk-detection/) or [Due Diligence](goals/due-diligence/); if a dispute surfaces an overlooked amendment or misapplied legal rule → [Jurisdiction Handling](goals/jurisdiction-handling/); if IP rights are unclear or usage unauthorized → [IP-Rights](goals/ip-rights/); if litigation discovery is incomplete or privilege was waived → [Litigation Support](goals/litigation-support/); if a brief relies on bad authority → [Precedent Currency](goals/precedent-currency/).

## Frequently Asked Questions

### What do amendment tracking, regulatory updates, and superseded case law have in common?
All three are temporal-staleness failures where an agent reasons from a fixed snapshot in time (original contract, training-data knowledge, published case law) without a mechanism to detect that the snapshot has been superseded (by an amendment, a regulatory change, or an overruling decision). The structural fix is the same for all three: add mandatory verification against a current, dated source before treating the determination as final.

### How do multi-agent handoff failures recur across so many different goals?
Handoff failures happen when a schema-constrained interchange (a checklist, a structured citation list, a findings summary) has no field to capture a nuanced determination an upstream agent identified. The fix is the same across all: add required fields to the handoff schema for any determination that is material and requires downstream action (exceptions, scope limitations, overruled status, risk flags). Validate that all schema fields are populated before handoff.

### What causes retrieval-based template selection to fail so consistently?
Retrieval by similarity works well when the candidate pool is homogeneous, but legal templates differ by jurisdiction and legal effect while sharing dense overlapping vocabulary. Similarity ranking surfaces "similar to my query" not "has the intended legal effect for my controlling jurisdiction." The fix is mandatory pre-filtering: filter candidates by jurisdiction or legal effect before similarity ranking, never after.

### How many of the 32 patterns would be caught by a more powerful LLM?
Very few. Most patterns are not reasoning errors but verification gaps: the agent could reason correctly if it had the right inputs (current amendments, current regulations, current citator status, correct template version, jurisdiction-filtered candidates), but it has no mechanism to verify those inputs are current or correct. Model capacity is not the limiting factor; verification architecture is.

## Patterns by Failure Mechanism

**Temporal Staleness (9 patterns):** [Amendment Tracking Failure](goals/compliance/failures/amendment-tracking-failure.md), [Regulatory Update Lag](goals/compliance/failures/regulatory-update-lag.md), [Superseded Case-Law Citation](goals/precedent-currency/failures/superseded-case-law-citation.md), [Clause Version Mismatch](goals/contract-drafting/failures/embedding-retrieval-pulls-wrong-clause-version-from-template-library.md), [Disclosure Template from Wrong Jurisdiction](goals/compliance/failures/embedding-retrieval-applies-wrong-jurisdictions-disclosure-template-by-name-similarity.md), [Jurisdiction Clause Mismatch](goals/jurisdiction-handling/failures/embedding-retrieval-applies-wrong-jurisdictions-clause-template-by-name-similarity.md), [OSS License vs. Assignment](goals/ip-rights/failures/embedding-retrieval-pulls-generic-oss-license-as-ip-assignment-template.md), [Unverified Clearance Citation](goals/ip-rights/failures/unverified-clearance-opinion-filed-without-checking-cited-clause-against-source-agreement.md), [Rendered Export Mismatch](goals/contract-drafting/failures/rendered-export-not-verified-against-edited-clause-text.md).

**Multi-Agent Handoff Loss (8 patterns):** [Jurisdiction Exception Drop](goals/compliance/failures/multi-agent-handoff-drops-jurisdiction-specific-exception-between-compliance-review-and-filing-agent.md), [Negotiated Value Drop](goals/contract-drafting/failures/multi-agent-handoff-drops-negotiated-deviation-between-redline-and-assembly-agent.md), [Risk Flag Drop](goals/due-diligence/failures/multi-agent-handoff-drops-flagged-risk-between-review-and-summary-agent.md), [Field-of-Use Scope Drop](goals/ip-rights/failures/multi-agent-handoff-drops-field-of-use-limitation-between-clearance-and-licensing-agent.md), [Overruled Citation Drop](goals/precedent-currency/failures/multi-agent-handoff-drops-overruled-citation-flag-between-research-and-drafting-agent.md), [Change-of-Control Risk Miss](goals/due-diligence/failures/change-of-control-clause-omission.md), [Vocabulary Mismatch in Discovery](goals/litigation-support/failures/discovery-document-relevance-misclassification.md), [Privilege-by-Reference Miss](goals/litigation-support/failures/privilege-waiver-risk.md).

**Cross-Clause Interaction (7 patterns):** [Boilerplate-Negotiation Conflict](goals/contract-drafting/failures/boilerplate-clause-misapplication.md), [Indemnification Cap Blindness](goals/risk-detection/failures/indemnification-cap-blindness.md), [Liability Exposure Blindness](goals/risk-detection/failures/liability-clause-blindness.md), [Termination-Renewal Interaction](goals/risk-detection/failures/termination-clause-misinterpretation.md), [Contract Ambiguity Miss](goals/risk-detection/failures/contract-ambiguity-misses.md), [Correlation as Causation](goals/due-diligence/failures/correlation-narrated-as-causation-in-financial-risk-memo.md), [Entity Matching Mismatch](goals/due-diligence/failures/embedding-retrieval-surfaces-similarly-named-unrelated-subsidiary-in-corporate-structure-chart.md).

**Reasoning Scope (8 patterns):** [Multi-Party Obligation Confusion](goals/risk-detection/failures/multi-party-obligation-tracking.md), [Jurisdictional Application Error](goals/jurisdiction-handling/failures/choice-of-law-mishandling.md), [Data-Transfer Mechanism Gap](goals/jurisdiction-handling/failures/cross-border-data-transfer-clause-miss.md), [Positional Bias](goals/litigation-support/failures/positional-bias-omits-mid-document-admission-in-deposition-summary.md), [Circuit Split Blindness](goals/precedent-currency/failures/circuit-split-blindness-in-citation-selection.md), [IP Mechanism-Category Mismatch](goals/ip-rights/failures/ip-assignment-gap-in-contractor-agreements.md).

## Related Categories

- [Document Processing](../document-processing/) — the upstream problem of turning legal documents into usable text without OCR, layout, or extraction errors that feed into contract analysis
- [Knowledge Retrieval](../knowledge-retrieval/) — the cross-cutting RAG and retrieval problem that recurs across legal and all other domains
- [Reasoning and Thought](../reasoning-and-thought/) — model degradation, version drift, and confidence miscalibration that compound with legal-domain-specific failures
