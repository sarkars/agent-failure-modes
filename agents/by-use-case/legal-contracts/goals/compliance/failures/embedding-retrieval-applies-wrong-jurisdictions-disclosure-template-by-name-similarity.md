# Embedding Retrieval Applies Wrong Jurisdiction's Disclosure Template by Name Similarity

## Issue: A Compliance Agent Assembling a Required Regulatory Disclosure for a Filing Retrieves the Applicable Disclosure Template From a Multi-Jurisdiction Template Library Using Semantic Similarity Over the Regulation's Name and Subject Matter, Rather Than Matching on the Controlling Jurisdiction Itself, and Pulls a Template Built for a Differently Named but Substantively Different Regulatory Regime in Another Jurisdiction That Happens to Share Closely Overlapping Terminology

**Frequency**: Occasional

**Symptoms**
- The filed disclosure carries the required language, section headings, and dollar/day thresholds from a regulation genuinely different from the one controlling the filing — the retrieved template is a real, valid template, just for the wrong regulatory regime
- Because the wrong template's regulation name is lexically almost indistinguishable from the correct one, a drafter doing a first-pass read has no cue prompting a citation check; the mismatch surfaces only when someone deliberately traces the cited statute back to its actual text
- The template library's retrieval index has no jurisdiction field it filters on before ranking by similarity — jurisdiction is treated as one more descriptive attribute folded into the embedding vector, not as a hard pre-filter, so a same-topic template from any jurisdiction is eligible to win on similarity alone
- Privacy notices, breach notifications, and beneficial-ownership disclosures are the recurring trouble spots specifically because regulators across jurisdictions borrow heavily from each other's statutory language when drafting these rules, producing templates that are lexically close by construction, not by coincidence
- The error is caught, when it is caught, by a compliance reviewer manually cross-referencing the filing's citation against the jurisdiction's actual code section — a step that happens after drafting, not as part of retrieval

**Root Cause**
The compliance agent's template library is indexed by embedding vectors computed over each template's regulation name and a short subject-matter summary, and retrieval ranks candidates by similarity to the filing's stated topic — there is no separate, deterministic index keyed to jurisdiction that retrieval consults first. Because regulatory regimes addressing the same general topic (breach notification, beneficial-ownership disclosure, privacy notice) are independently named across dozens of jurisdictions using closely overlapping vocabulary, the embedding space places a same-topic template from the wrong jurisdiction closer to the query than jurisdiction-correct templates would be if jurisdiction were encoded as a hard constraint rather than left to emerge from vocabulary similarity alone. The retrieval step has no way to know that "topically similar" and "jurisdictionally applicable" are different questions, since only the first is what its similarity metric actually measures.

**Example**
```
Compliance agent is asked to assemble the required breach-notification disclosure for an incident affecting residents of State A, where the filing entity is registered
Template library contains disclosure templates for State A's breach-notification statute and for several other states' substantively different breach-notification statutes, all under similarly worded titles ("Notification of Security Breach," "Data Breach Notification Requirements")
Agent's retrieval, ranking by similarity to "breach notification disclosure for State A incident," surfaces a template from a different state whose statute name and structure are nearly identical in wording, but which has a shorter notification deadline and a narrower defined scope of "personal information" than State A's actual statute
Filed disclosure uses the wrong state's notification deadline and definitional scope; a compliance reviewer catches the mismatch only after comparing the filed disclosure's citation against State A's actual statute number
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrievers in legal RAG systems frequently select content from the wrong source document because regulatory and legal text addressing the same subject matter across different sources shares dense, structurally similar vocabulary that confuses similarity-based ranking | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Document-Level Retrieval Mismatch rates exceeding 95% were observed on structurally standardized legal document sets, attributed to linguistic homogeneity across near-identical but substantively distinct source documents | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Hallucination surveys of LLM-based agents note that retrieval-augmented pipelines can still produce ungrounded or misattributed outputs when the retrieval step itself returns a plausible but incorrect source, independent of the generation model's own reasoning | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- Template library is organized and searched by regulation subject matter and name rather than indexed first by controlling jurisdiction
- No deterministic pre-filter restricts candidate templates to the filing's actual controlling jurisdiction before similarity ranking is applied
- Jurisdiction metadata on each template is present in the library but not surfaced as a high-salience, checkable field in the agent's retrieval context
- Regulatory regimes with parallel naming conventions across jurisdictions are common enough that the underlying retrieval confusion is structural, not a one-off edge case

---

## Mitigation Strategies

### Prevention

1. **Jurisdiction-first deterministic filter with pre-retrieval boundary enforcement**: Modify retrieval pipeline: before any semantic similarity ranking, enforce deterministic pre-filter: (a) extract filing's controlling jurisdiction from case/filing metadata, (b) query template library: "Show only templates tagged with jurisdiction=X", (c) retrieve from jurisdiction-filtered pool only, (d) rank by similarity within filtered set. Never perform open-ended similarity search across all jurisdictions, then filter afterward. Rationale: similarity-based ranking across cross-jurisdiction templates will surface near-duplicates before jurisdiction filter takes effect, causing wrong-jurisdiction template to appear first. Root cause mitigation: Prevents similarity-based ranking from surfacing wrong-jurisdiction templates by filtering jurisdictions before ranking.

2. **Statute citation cross-check gate with mandatory field display**: Require template retrieval output to prominently display: {filing_jurisdiction: X, template_jurisdiction: Y, filing_statute_citation: US_Code_123, template_statute_citation: State_Code_456}. If filing_jurisdiction ≠ template_jurisdiction, display side-by-side: "JURISDICTION MISMATCH: Filing is for [State A, § 12-34], retrieved template is for [State B, § 56-78]. Proceed? [Confirm/Correct]". Require explicit confirmation by human reviewer before using mismatched template. For compliant scenarios (filing_jurisdiction = template_jurisdiction), template citation must validate against known statutes: query regulatory database: "Is State A § 12-34 a valid breach-notification statute?" If citation validation fails, flag for attorney review. Root cause: Makes jurisdiction mismatch visually obvious and forces human check.

3. **Cross-jurisdiction near-duplicate detection and routing rule index**: Periodically scan template library for templates with similar names across jurisdictions. Identify clusters: {topic: "Breach Notification", jurisdictions: [State A, State B, State C], shared_keywords: [notification, deadline, personal_info]}. For each cluster, add deterministic routing rule: "For breach-notification filing, always check jurisdiction first; these templates are near-duplicates across [list states]". Maintain index: {regulation_family, near_duplicate_cluster, routing_rule}. When new template added, check if it creates new near-duplicate cluster; if so, add routing rule. Root cause: Systemizes identification of cross-jurisdiction confusion risk and adds preventive routing rules.

### Detection & Response

1. **Template jurisdiction audit logging with mismatch tracking and citation validation**: For every disclosure filed, log: (a) filing's controlling jurisdiction, (b) template retrieved and its jurisdiction, (c) statute citation in filing, (d) template's original statute citation, (e) citation validation status (valid|invalid|unclear), (f) reviewer confirmation if mismatch override. Run automated quality check: sample filed disclosures, verify template's jurisdiction matches filing's jurisdiction. Measure: jurisdiction_mismatch_rate, citation_validation_accuracy, cross_jurisdiction_retrieval_frequency.

2. **Retroactive disclosure audit on wrong-jurisdiction detection**: When wrong-jurisdiction disclosure detected (via regulatory review, customer complaint, or internal audit), trace to original retrieval. Which template was retrieved? Why was wrong jurisdiction selected? Update retrieval logic if needed. For each affected disclosure, determine: does filed disclosure need amendment? Is it still compliant under wrong jurisdiction's law? Escalate to legal/compliance.

### Architecture Patterns

1. **Jurisdiction-First Retrieval Router**: (1) Extract filing's controlling jurisdiction, (2) Pre-filter template library to jurisdiction only, (3) Rank remaining templates by similarity within filtered set, (4) Return top matches all guaranteed from correct jurisdiction.

2. **Statute Citation Validator**: (1) Extract statute citation from template, (2) Query regulatory database: is this a valid statute? (3) For retrieved citation, verify it's associated with retrieved template's jurisdiction, (4) If citation doesn't match jurisdiction, flag.

3. **Near-Duplicate Cluster Detector**: (1) Scan template library for naming similarity across jurisdictions, (2) Identify regulation-family clusters, (3) Build routing rules for high-risk clusters, (4) On new template addition, check for new cluster creation.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|-------------------|
| Jurisdiction-First Filter Compliance | 100% | <99% | # of template retrievals using jurisdiction-first pre-filter / total retrievals |
| Jurisdiction Match Rate | 100% | <99% | # of filed disclosures where template jurisdiction matches filing jurisdiction / total disclosures |
| Citation Validation Accuracy | 100% | <99% | # of retrieved template citations validated against regulatory database / total citations (accuracy verified by legal review) |
| Mismatch Detection Sensitivity | 100% | <99% | # of jurisdiction mismatches detected by system before filing / total mismatches in sample (validation: post-hoc audit) |
| Near-Duplicate Cluster Coverage | >95% | <90% | # of cross-jurisdiction near-duplicate clusters identified and routing-ruled / total clusters in library |
| False Positive Rate (Over-Flagging Mismatches) | <2% | >5% | # of false mismatch alerts / total mismatch alerts |
| Post-Filing Correction Rate | 0 | >0 | # of filed disclosures requiring amendment due to wrong-jurisdiction template use / total filings |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Jurisdiction-First Filter Bypass Detected | Template retrieval performed without jurisdiction pre-filter; open-ended similarity search across all jurisdictions | CRITICAL | Block retrieval; require re-run with jurisdiction-first filter; audit why filter was bypassed |
| Jurisdiction Mismatch Detected | Template retrieved from different jurisdiction than filing's controlling jurisdiction | CRITICAL | Block filing; require attorney review; identify correct-jurisdiction template; if acceptable mismatch documented, explicit human approval required |
| Citation Validation Failed | Template's statute citation cannot be validated against regulatory database, or citation doesn't match template's jurisdiction | HIGH | Escalate to legal; template may be corrupted or outdated; do not use without legal review |
| Near-Duplicate Cluster Without Routing Rule | New template added creates near-duplicate cluster with existing templates from different jurisdictions, but no routing rule in place | MEDIUM | Add deterministic routing rule for cluster; audit existing filings using templates from this cluster |
| Recurring Mismatch: Regulation Family | Multiple wrong-jurisdiction errors traced to same regulation family (e.g., 3+ breach-notification mismatches across different states) | HIGH | Audit retrieval configuration for that regulation family; may indicate systematic confusion; enhance routing rules or template library organization |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Jurisdiction-Specific Compliance in Legal Document Processing](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3845621)
