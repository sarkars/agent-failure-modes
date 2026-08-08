# Embedding Retrieval Applies Wrong Jurisdiction's Clause Template by Name Similarity

## Issue: A Drafting Agent Asked to Insert a Jurisdiction-Specific Clause (a Non-Compete, a Consumer-Arbitration Provision, a Statutory Notice) for a Contract Governed by One State or Country's Law Retrieves the Clause From a Multi-Jurisdiction Template Library Using Semantic Similarity Over the Clause's General Subject Matter, Rather Than Matching Strictly on Governing Jurisdiction, and Pulls a Differently-Jurisdictioned Template That Is Lexically Almost Identical but Legally Ineffective or Unenforceable Under the Contract's Actual Governing Law

**Frequency**: Common

**Symptoms**
- The inserted clause is topically correct and well-formed — it's a real template for the right general provision type — but its enforceability conditions, required statutory language, or permitted scope belong to a jurisdiction other than the one governing the contract
- The clause types most prone to this are exactly the ones with the most jurisdiction-to-jurisdiction vocabulary overlap: non-compete enforceability standards, consumer-arbitration opt-out language, data-breach notice triggers — topics where many jurisdictions' statutes are worded similarly enough that embedding similarity can't separate them
- Retrieval carries no jurisdiction pre-filter; it ranks every clause template in the library by similarity to the query's subject matter and returns the top match regardless of which jurisdiction that match happens to be drafted for
- The error surfaces only at legal review or in opposing counsel's redline, after the contract has already been drafted or issued — retrieval itself produces no signal distinguishing this case from a correct match
- Because the same template library and the same retrieval logic serve every jurisdiction-specific clause request, the failure isn't confined to one clause type or one contract — any clause family with cross-jurisdictional vocabulary overlap is equally exposed

**Root Cause**
When the drafting agent needs a jurisdiction-specific clause, it queries the template library with the clause's subject matter (non-compete, arbitration, statutory notice) and takes the top embedding-similarity match, with no separate filter step that first narrows candidates to the contract's actual governing-law jurisdiction. Because many jurisdictions regulate the same general topic and clause drafters tend to reuse similar statutory phrasing and structure across jurisdictions when writing these provisions, the vocabulary overlap between a correct-jurisdiction template and a wrong-jurisdiction template is often as high as the overlap between two genuinely different clause types within the same jurisdiction — so similarity search, which cannot distinguish "same topic, wrong jurisdiction" from "same topic, right jurisdiction," has no signal telling it which of several plausible matches is the one that's actually enforceable here.

**Example**
```
Drafting agent is asked to insert a non-compete clause into an employment agreement governed by the law of State A
Clause-template library holds non-compete templates for many states, including State A and several others with similarly structured (but substantively different) enforceability standards -- some impose salary thresholds, some ban non-competes outright for certain worker classes, some allow broader geographic scope than State A permits
Agent's retrieval, ranking by similarity to "non-compete clause for employment agreement," surfaces a template from a different state whose clause language is over 90% lexically identical to State A's template but omits a mandatory consideration-and-notice requirement that State A's statute requires for enforceability
Drafted agreement is executed with the wrong-jurisdiction non-compete language; the clause is later found unenforceable in litigation because it lacks the consideration disclosure State A's statute requires, a defect traceable directly to the wrong template having been retrieved
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrievers in legal RAG systems frequently select content from the wrong source document because legal text addressing the same subject matter across different jurisdictions shares dense, structurally similar vocabulary that confuses similarity-based ranking | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Document-Level Retrieval Mismatch rates exceeding 95% were observed on structurally standardized legal document sets, attributed to linguistic homogeneity across near-identical but substantively distinct source documents | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Surveys of LLM evaluation in legal applications note that legal tasks span multiple jurisdictions with materially different substantive rules, and that benchmark and deployment methodologies must account for jurisdiction as a first-class variable rather than treating legal text as a single undifferentiated domain | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |

**Contributing Factors**
- Template library is organized and searched primarily by clause type and subject matter rather than indexed first by governing jurisdiction
- No deterministic pre-filter restricts candidate templates to the contract's actual governing-law jurisdiction before similarity ranking over clause text is applied
- Jurisdiction metadata is present on each template but not surfaced as a high-salience, checkable field in the agent's retrieval context, so the model has no strong signal to prefer it over topical similarity
- Clause types regulated similarly-but-differently across many jurisdictions (non-competes, arbitration, statutory notices) are common enough that this retrieval confusion is structural rather than a rare edge case

---

## Mitigation Strategies

### Prevention

1. **Jurisdiction-first deterministic filter with mandatory pre-filter gating**: Modify retrieval pipeline: (a) extract contract's governing-law jurisdiction, (b) pre-filter clause library: "Show only templates tagged with jurisdiction=X", (c) search within jurisdiction-filtered pool only by similarity, (d) never perform open-ended cross-jurisdiction similarity search. Enforce gating: if governing-law jurisdiction not found in template, flag as missing. Fail-safe: retrieve error if jurisdiction-filtered templates unavailable. Root cause: Prevents similarity ranking across jurisdictions by restricting candidate pool first.

2. **Governing-law metadata surfacing with mandatory field display**: Require retrieved clause to display: {contract_governing_law: X, template_jurisdiction: Y, template_statutory_citation: Z}. If contract_governing_law ≠ template_jurisdiction, display mismatch prominently: "JURISDICTION MISMATCH: Contract governed by NY; template from NJ." Require explicit human confirmation before inserting mismatched template. Root cause: Makes jurisdiction mismatch visually obvious.

3. **Enforceability cross-check gate with substantive-requirement validation**: Before clause finalized, run automated check: (a) extract clause's governing-law jurisdiction and statutory citation, (b) query enforceability database: "Is this statute's non-compete enforceable in this jurisdiction? Requirements: [list]", (c) scan clause for compliance with requirements (notice language, consideration disclosure, geographic scope), (d) flag if clause text doesn't match requirements, (e) block finalization. Root cause: Adds independent verification that clause meets actual jurisdiction's substantive requirements.

### Detection & Response

1. **Clause retrieval audit logging with jurisdiction-match tracking**: For every drafted contract, log: (a) clause type requested, (b) contract's governing-law jurisdiction, (c) template retrieved and its jurisdiction, (d) jurisdiction match status (match/mismatch), (e) enforceability check result (pass/fail). Measure: jurisdiction_match_rate, enforceability_check_pass_rate.

2. **Retroactive enforceability audit on clause challenge**: When clause enforceability challenged in litigation or redline, trace to original retrieval. Was correct jurisdiction selected? Does clause meet jurisdiction's substantive requirements? Update enforceability database and retrieval logic based on findings.

### Architecture Patterns

1. **Jurisdiction-First Clause Retriever**: (1) Extract governing-law jurisdiction, (2) Pre-filter templates by jurisdiction, (3) Rank within filtered set by similarity, (4) Surface metadata prominently.

2. **Enforceability Validator**: (1) Extract clause's jurisdiction and statutory citation, (2) Query enforceability database, (3) Check clause text against requirement rules, (4) Flag non-compliance.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|-------------------|
| Jurisdiction Pre-Filter Success Rate | >95% | <90% | # of clause requests successfully fulfilled via jurisdiction-filtered pool / total requests |
| Jurisdiction Match Rate | 100% | <99% | # of clauses where template jurisdiction matches contract's governing-law jurisdiction / total clauses |
| Enforceability Check Pass Rate | 100% | <98% | # of clauses passing automated enforceability requirements check / total clauses checked |
| Wrong-Jurisdiction Detection Rate | 100% | <99% | # of cross-jurisdiction clause mismatches detected and blocked before draft finalized / total mismatches present |
| Post-Deployment Enforceability Challenge Rate | 0 | >0 | # of deployed clauses challenged as unenforceable due to wrong jurisdiction / total deployed clauses |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Jurisdiction Pre-Filter Unavailable | No templates found for contract's governing-law jurisdiction; unable to retrieve jurisdiction-first | CRITICAL | Escalate to template library team; add templates for missing jurisdiction; do not proceed with cross-jurisdiction fallback without explicit approval |
| Jurisdiction Mismatch Detected | Retrieved clause from different jurisdiction than contract's governing-law | CRITICAL | Block finalization; escalate to legal; retrieve correct-jurisdiction template; if mismatch override needed, document justification |
| Enforceability Check Failed | Clause fails automated enforceability validation; doesn't comply with governing-law requirements | HIGH | Block finalization; escalate to legal; may require clause revision to meet jurisdiction requirements |
| Recurring Wrong-Jurisdiction Pattern | Multiple wrong-jurisdiction errors on same clause type (e.g., 3+ non-competes from wrong jurisdictions) | HIGH | Audit retrieval configuration; enhance jurisdiction-first filtering; add routing rules for high-risk clause types |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Jurisdiction-Specific Clause Retrieval and Enforceability in Legal Drafting Systems](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3896342)
