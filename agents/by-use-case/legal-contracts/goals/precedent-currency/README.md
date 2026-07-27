# What Are the Most Common Precedent-Currency Failures in AI Agents?

**Precedent-currency failures happen when a legal research agent cites a case as controlling law without checking whether it has been overruled, when a research agent identifies an overruled status in its own analysis but never communicates that status to a downstream drafting agent through the structured handoff schema, or when a legal research agent fails to surface contrary authority across multiple circuits or jurisdictions despite knowing a circuit split exists on the cited proposition.** Precedent-currency failures are particularly damaging because they make a brief or memo's foundation of authority appear sound when the cited cases are in fact superseded, limited, or contradicted by later decisions that the research step could have retrieved but didn't. Because LLM research agents have access to legal-research databases and citator services but operate without explicit post-generation verification, superseded authority can appear in filed documents without detection until opposing counsel flags it, at which point the filing's credibility is irreparably harmed and strategic position is compromised.

## Key Takeaways

- 3 patterns are documented here: superseded-case-law citation (overruled authority cited as good law), circuit-split blindness (contrary authority exists but is not surfaced), and multi-agent handoff loss (overruled status identified by research agent but never reaches drafting agent).
- Reliance on outdated or invalidated case law is one of the most consequential and reputationally damaging failure modes in legal-AI literature, with documented instances of AI-assisted filings citing non-existent or invalidated cases and drawing court sanctions.
- Citator services (Shepard's, KeyCite) exist precisely because static reference corpora lag behind published decisions, and legal AI survey research identifies live citator integration as a distinct mitigation from corpus-freshness alone, yet many legal-research agents either lack citator access or apply it post-hoc rather than pre-generation.
- Circuit-split awareness requires more than retrieval: it requires identifying research questions that are known to have split authority, either via a pre-built circuit-split registry or through an explicit secondary search path for contrary authority that mirrors the primary topical search.

## Scope

- **Superseded Authority** — [Superseded Case-Law Citation](failures/superseded-case-law-citation.md). A case cited as controlling precedent has been overruled, vacated, or limited on appeal or by later decision without the agent detecting the status change.
- **Circuit-Split Blindness** — [Circuit Split Blindness in Citation Selection](failures/circuit-split-blindness-in-citation-selection.md). Contrary authority exists across multiple circuits or jurisdictions but is not surfaced in the research output, leaving the brief to present a holding as settled law when a split actually exists.
- **Multi-Agent Handoff** — [Multi-Agent Handoff Drops Overruled-Citation Flag Between Research and Drafting Agent](failures/multi-agent-handoff-drops-overruled-citation-flag-between-research-and-drafting-agent.md). Research agent identifies overruled status in its analysis but structured citation-list schema has no validity-status field, so drafting agent cites the case as good law.

## When Precedent-Currency Matters

- A brief or memo is being drafted citing case law, and the underlying research was conducted against a reference corpus or training data with a knowledge cutoff
- A matter involves multiple jurisdictions or circuits with the possibility of conflicting authority on the same legal question
- Research and drafting are performed by separate agents communicating through a structured citation list rather than the research agent's full analysis

## Cross-Pattern Insight

Precedent-currency failures are failures of independent verification at the output stage. The superseded-authority pattern stops after retrieving a case without checking current citator status. The circuit-split pattern ranks results by topical relevance without requiring an explicit search for contrary authority. The handoff pattern relies on a citation list with no validity-status field to capture nuance the research agent identified. The fix recurs across all three patterns: add a mandatory verification layer that doesn't trust the generation step's own confidence or schema. Run live citator checks before output, implement dual-path research (primary + explicit contrary-authority search), enforce structured validity fields with reconciliation before handoff.

## Frequently Asked Questions

### How do you verify a citation's current legal status before using it in a filing?
Implement a real-time citator-check gate before output: after the research agent generates candidate citations, pass all citations through a live citator service (Shepard's, KeyCite, LexisNexis) to check for overruling, limiting, or negative treatment. Capture the citator status (good law, overruled, limited, questioned) and include it in the output. If citator is unavailable, mark as UNVERIFIED and require attorney confirmation before use — see [Superseded Case-Law Citation](failures/superseded-case-law-citation.md).

### How do you find and surface contrary authority in a circuit-split situation?
Implement dual-path research: Path 1 does primary topical search ranked by relevance; Path 2 runs explicit contrary-authority queries using negation terms and opposite-holding indicators. Cross-reference results against a Circuit-Split Registry of known splits. For any citation on a question with known splits, output must explicitly disclose the split, list all known split positions, and specify which jurisdiction's rule is binding and which are persuasive — see [Circuit Split Blindness in Citation Selection](failures/circuit-split-blindness-in-citation-selection.md).

### How do you prevent a research agent from identifying overruled status that never reaches a drafting agent?
Extend the citation-list handoff schema to include point-specific validity fields: {case_id, citation, original_holding, validity_status: {overall_status, point_specificity: [{proposition, validity_on_point, overruling_authority}]}}.  Validation gate: if research analysis contains validity-limitation language, require population of all point_specificity entries before handoff. Reconciliation check: scan research analysis for validity keywords; if found, verify corresponding entries in schema. If mismatch, escalate for correction — see [Multi-Agent Handoff Drops Overruled-Citation Flag Between Research and Drafting Agent](failures/multi-agent-handoff-drops-overruled-citation-flag-between-research-and-drafting-agent.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Circuit Split Blindness in Citation Selection](failures/circuit-split-blindness-in-citation-selection.md) | Contrary authority across multiple circuits exists but research does not surface it; brief presents holding as settled law when split actually exists |
| [Multi-Agent Handoff Drops Overruled-Citation Flag Between Research and Drafting Agent](failures/multi-agent-handoff-drops-overruled-citation-flag-between-research-and-drafting-agent.md) | Research agent identifies overruled status in analysis but structured citation-list schema has no validity field; drafting agent cites case as good law |
| [Superseded Case-Law Citation](failures/superseded-case-law-citation.md) | Case cited as controlling precedent has been overruled, vacated, limited, or superseded without agent detecting current legal status |

**Total: 3 patterns**

## Related Goals

- [Compliance](../compliance/) — where temporal staleness (regulatory updates) produces similar "stale authority" failures
- [Litigation Support](../litigation-support/) — where deposition summaries and discovery classifications can omit material admissions or evidence due to similar verification gaps
