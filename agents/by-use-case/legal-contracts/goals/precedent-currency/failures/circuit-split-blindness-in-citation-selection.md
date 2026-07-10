# Circuit Split Blindness in Citation Selection

## Issue: Legal Research Agent Cites a Precedent as Settled Law Without Flagging That a Circuit Split (or Equivalent Jurisdictional Disagreement) Exists, Leading to a Brief That Misrepresents the Strength of the Authority

**Frequency**: Common

**Symptoms**
- Agent cites a single appellate decision in support of a legal proposition without noting that one or more other circuits/jurisdictions have reached the opposite conclusion on the same question
- Drafted briefs or memos present a holding as "the rule" rather than "the rule in this circuit, with a contrary rule in others," understating the actual litigation risk
- Opposing counsel's response brief cites the contrary-circuit authority that the agent's research never surfaced, catching the legal team off guard
- Research memos generated for multi-jurisdiction matters fail to differentiate which circuit's rule applies to which entity or transaction in the matter
- Citation-checking review finds that the agent's underlying retrieval ranks decisions by semantic relevance to the query, not by circuit-split awareness, so contrary authority is retrievable but never surfaced unless explicitly searched for

**Root Cause**
Legal research agents built on semantic retrieval over case law typically rank and return the most topically relevant decisions for a query, but "topically relevant" does not equate to "represents the full landscape of authority on this question." Without an explicit step that checks whether other circuits or jurisdictions have addressed the identical question and reached a different conclusion -- a step that requires structured awareness of circuit splits, not just semantic similarity -- the agent will confidently present a single jurisdiction's holding as if it were uncontested law.

**Example**
```
Research question: "Is a clickwrap arbitration clause enforceable without affirmative assent beyond browsing?"
Agent cites: Ninth Circuit decision finding such clauses unenforceable absent conspicuous notice and affirmative action
Agent's brief language: "Courts have held that browsewrap-style arbitration clauses are unenforceable without affirmative assent."
Missing: Second and Seventh Circuit decisions enforcing materially similar clauses under a constructive-notice standard
Outcome: brief overstates the strength of the unenforceability argument in a matter that may ultimately be litigated in a circuit following the contrary rule
```

**Key Statistics**
- Surveys of LLMs in legal applications report that hallucinated or incomplete citation -- including omission of contrary authority -- remains one of the most consistently observed failure categories even in retrieval-augmented legal research tools
- Legal AI evaluation research notes that retrieval-based legal research tools, when evaluated specifically for split-authority awareness rather than topical relevance, show materially lower recall of contrary-jurisdiction holdings than of same-conclusion holdings on the same question
- Practitioner-facing legal AI benchmarking work emphasizes that citation completeness (not just citation accuracy) is a distinct and under-tested dimension of legal AI reliability

**Contributing Factors**
- Retrieval ranks by semantic similarity to the query, not by an explicit "does contrary authority exist" check
- No structured circuit-split database integrated into the research pipeline
- Drafting step does not require the agent to affirmatively state "no contrary authority identified" as a checkable claim, leaving omission undetectable until opposing counsel responds

---

## Mitigation Strategies

### Prevention

1. **Dual-path research pipeline with dedicated contrary-authority search**: Restructure legal research: (a) Path 1 (Primary Authority): Semantic search over case law for topically relevant decisions on the legal question, ranked by relevance, (b) Path 2 (Contrary-Authority Check): Run explicit contra-search queries ("opposite", "disagreed", "contrary", "rejected") to identify holdings reaching opposite conclusion on same legal question, (c) Cross-reference both paths against Circuit-Split Registry (below), (d) For any legal proposition with known splits, output must include: authority_position {circuit, jurisdiction, holding_side (pro/contra)}, known_split_status {split_exists: Y/N, split_summary, other_circuits_position}, disclosure_required (Y/N). Root cause: Ensures contrary authority is actively searched for, not omitted by relevance ranking.

2. **Integrated circuit-split registry with query-time checking**: Maintain authoritative database: {legal_question_id, jurisdiction, holding_authority_list (circuit, date, outcome), split_exists, split_summary, last_updated}. Sample entries: "Enforceability of clickwrap arbitration clauses", "Burden of proof in trade secret misappropriation", "Scope of CFAA computer access liability". On any research output, check if cited legal_question matches registry. If match found: (a) auto-flag all known split positions, (b) verify output includes disclosure language for each split position, (c) require output to explicitly state jurisdiction applicability. Root cause: Prevents citation presentation as universal when splits are known.

3. **Mandatory split-aware disclosure language with jurisdiction-specific caveats**: For any cited holding, require output language that includes: "{Holding} [Authority: {Circuit/Jurisdiction}, Date] [Jurisdiction: Binding in {listing}, Persuasive in {listing}] [Circuit Split Status: {Split exists with {list of contrary circuits}. In those jurisdictions, contrary authority follows {split_position}}]". Block generation of phrase "the law is" or "courts have held" unless output explicitly restricts scope to specific jurisdiction(s). For multi-jurisdiction matters, maintain jurisdiction-applicability matrix: {legal_question, jurisdiction_A_rule, jurisdiction_B_rule} so parties/transactions are explicitly mapped to applicable rule.

### Detection & Response

1. **Citation-audit logging with split-awareness tracking**: For each citation in a draft research product, log: {citation_id, case_id, circuit/jurisdiction, legal_question_id, legal_question_matches_registry (Y/N), split_status_at_research_time (split_exists: Y/N), split_disclosed_in_output (Y/N), disclosure_quality (adequate|incomplete|missing)}. Weekly audit: sample 20% of cited holdings, verify: (a) if legal_question in registry, confirm split status disclosed, (b) if split exists and undisclosed, investigate why contra-search failed, (c) for multi-jurisdiction matters, verify jurisdiction-applicability matrix used. Alert if: >5% of sampled citations with known splits are not disclosed.

2. **Opposing-counsel-citation tracking and research-completeness audit**: When opposing counsel cites authority not surfaced in internal research, log: {opposing_counsel_citation, our_research_product, retrieval_step_that_should_have_found_it (primary search | contra search), search_query_gap_root_cause}. Quarterly: compile report "Citations We Missed That Opposing Counsel Found" and analyze for patterns (underutilization of contra-search? registry gaps? jurisdiction-specific databases not searched?). Use findings to improve search queries and registry coverage.

### Architecture Patterns

1. **Dual-Path Research Engine with Contrary-Authority Detector**: Legal question → Path 1: Semantic search for topically relevant holdings → Path 2: Explicit contra-authority queries (negation terms, opposite holding indicators) → Cross-check both paths against Circuit-Split Registry → Output combined authority set with split-status metadata. For each cited holding, include jurisdiction, split_status, and required disclosure language.

2. **Circuit-Split Registry with Query-Time Validation**: Authoritative database: {legal_question_key, all_known_holdings_by_jurisdiction, split_exists, split_summary, last_updated, sources_for_split_documentation}. Query-time: when research output generated, check if any cited legal_question in registry; if match, auto-append split-disclosure language + require output to include caveats.

3. **Jurisdiction-Applicability Matrix for Multi-Jurisdiction Matters**: Maps {transaction/party, governing_jurisdiction, applicable_legal_rules, applicable_circuits}. On research output for multi-jurisdiction matter, dynamically generate jurisdiction-specific appendices: "Rule in Jurisdiction A: {X}. Rule in Jurisdiction B: {Y}. Parties affected by each: [list]." Prevents universal-rule presentation when jurisdiction-specific rules apply.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Circuit-Split Disclosure Rate | 100% | <99% | # of research outputs citing holdings with known splits that include split-status disclosure / total research outputs with split-applicable citations |
| Contrary-Authority Discovery Rate | >95% | <90% | # of known contrary holdings in same-question searches that agent's contra-search step surfaces / total known contrary holdings (validated via registry/manual audit) |
| Citation-Completeness Audit Pass Rate | >99% | <98% | # of audited research outputs where all citations with known splits included split-status disclosure / total audited citations with split-applicable questions |
| Undisclosed-Split Incident Rate | 0% | >0.5% | # of times opposing counsel cites contrary authority that internal research did not surface / total research outputs (audited post-opposition-response) |
| Multi-Jurisdiction Rule-Clarity Rate | 100% | <98% | # of multi-jurisdiction research outputs with explicit jurisdiction-applicability matrix or per-jurisdiction caveats / total multi-jurisdiction research products |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Split-Known Citation Without Disclosure | Research output cites holding on legal question with known circuit split, but split-status and contrary authority not disclosed | CRITICAL | Block research output from use; escalate to attorney; require revision with split-aware disclosure language; may require amendment of any work product relying on original output |
| Contra-Search Returns Zero on Split Question | Contrary-authority search returns no results for legal question flagged in registry as split-existing | HIGH | Investigate search-query effectiveness; manually audit database; verify registry completeness; may indicate search tool misconfiguration |
| Opposing Counsel Cites Unfound Authority | Post-opposition, discover opposing counsel cited contrary authority that firm's research tool could have retrieved but draft research did not surface | HIGH | Audit all research outputs from that matter; investigate whether contra-search step was skipped or queries insufficient; may require supplemental briefing or position revision |
| Multi-Jurisdiction Rule Ambiguity | Multi-jurisdiction research output fails to explicitly map rules to parties/transactions; presents one jurisdiction's rule as universal | MEDIUM | Escalate to substantive attorney; require jurisdiction-applicability matrix or per-jurisdiction caveats before output is shared with client; may require client communication clarifying actual rule positions |

---

## References

- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881)
