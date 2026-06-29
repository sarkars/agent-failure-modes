# Embedding Retrieval Applies Wrong Jurisdiction's Disclosure Template by Name Similarity

## Issue: A Compliance Agent Assembling a Required Regulatory Disclosure for a Filing Retrieves the Applicable Disclosure Template From a Multi-Jurisdiction Template Library Using Semantic Similarity Over the Regulation's Name and Subject Matter, Rather Than Matching on the Controlling Jurisdiction Itself, and Pulls a Template Built for a Differently Named but Substantively Different Regulatory Regime in Another Jurisdiction That Happens to Share Closely Overlapping Terminology

**Frequency**: Occasional

**Symptoms**
- Filed disclosure uses required language, section headings, or thresholds from a different jurisdiction's regulation than the one actually controlling the filing
- The retrieved template's regulation name is lexically very close to the correct one (e.g., a state-level "data breach notification" template retrieved for a filing actually governed by a similarly named but substantively different federal or sister-state breach-notification regime), so a quick read does not reveal the mismatch
- Compliance review catches the error only when a reviewer cross-checks the template's citation against the specific statute or rule actually controlling the filing's jurisdiction, rather than during initial drafting
- Re-running the retrieval restricted to templates pre-filtered by controlling jurisdiction (rather than free-text similarity over regulation name and subject matter) correctly returns the applicable template, isolating retrieval as the failure point
- The same near-miss recurs across regulation families with closely parallel naming conventions across jurisdictions (privacy notices, breach notifications, beneficial-ownership disclosures), since those are the families most likely to share dense overlapping vocabulary across jurisdictions

**Root Cause**
The compliance agent's retrieval step ranks candidate disclosure templates by embedding similarity over the regulation's name, subject-matter description, and surrounding boilerplate language, rather than by a deterministic match on the controlling jurisdiction recorded for the filing. Regulatory regimes that address the same general topic across different jurisdictions are typically named and described using closely overlapping vocabulary -- "data breach notification," "beneficial ownership disclosure," "consumer privacy notice" -- precisely because they regulate the same underlying activity, which is the structural condition under which similarity-based retrieval reliably confuses jurisdiction-distinct but topically identical source documents.

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

1. **Jurisdiction-First Deterministic Filter**: Restrict candidate templates to the filing's actual controlling jurisdiction via a deterministic lookup before any similarity-based ranking over regulation name or subject matter is applied
2. **Surface Jurisdiction and Statute Citation as Required Fields**: Require the retrieved template's jurisdiction and exact statute/rule citation to be displayed alongside the filing's own recorded controlling jurisdiction so a mismatch is visually checkable before the draft proceeds
3. **Cross-Jurisdiction Near-Duplicate Audit**: Periodically scan the template library for templates with closely overlapping names or subject-matter descriptions across different jurisdictions, and flag those clusters for mandatory deterministic jurisdiction-based routing
4. **Citation Cross-Check Gate**: Require an automated, non-LLM verification step confirming the template's statute citation matches a citation actually associated with the filing's recorded controlling jurisdiction before the disclosure is finalized

### Metrics
- Rate of filed disclosures where the template's jurisdiction does not match the filing's recorded controlling jurisdiction, sampled via review
- Count of cross-jurisdiction near-duplicate template clusters identified in the library without a deterministic-routing rule in place
- Time between filing and detection of a wrong-jurisdiction template error, by detection method

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Jurisdiction citation mismatch | Retrieved template's statute citation does not match filing's recorded controlling jurisdiction | P1 | Block filing; route to compliance review for correct-jurisdiction template |
| Cross-jurisdiction near-duplicate detected | New template added to library creates a near-duplicate naming cluster with an existing template from a different jurisdiction | P3 | Add deterministic jurisdiction-routing rule for the cluster |
| Recurring mismatch on same regulation family | Multiple wrong-jurisdiction errors traced to the same regulation family (e.g., breach notification, beneficial ownership) | P2 | Audit retrieval configuration for that regulation family |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
